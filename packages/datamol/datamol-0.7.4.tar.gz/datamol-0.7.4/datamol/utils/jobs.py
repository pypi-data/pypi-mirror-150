from typing import Iterable
from typing import Sequence
from typing import Callable
from typing import Optional
from typing import Any

import contextlib

import joblib
from joblib import Parallel, delayed

from tqdm.auto import tqdm


class JobRunner:
    def __init__(
        self,
        n_jobs: Optional[int] = -1,
        batch_size: Optional[int] = None,
        prefer: Optional[str] = None,
        progress: bool = False,
        total: Optional[int] = None,
        tqdm_kwargs: Optional[dict] = None,
        **job_kwargs,
    ):
        """
        JobRunner with sequential/parallel regimes. The multiprocessing backend use joblib which
        allows taking advantage of its features, while the progress bar use tqdm

        Args:
            n_jobs: Number of process. Use 0 or None to force sequential.
                Use -1 to use all the available processors. For details see
                https://joblib.readthedocs.io/en/latest/parallel.html#parallel-reference-documentation
            batch_size: Whether to  batch `inputs_list`. You can specify batch_size when the length
                of `inputs_list` is very large (>100k elements). By default, the auto batching of joblib is used.
            prefer: Choose from ['processes', 'threads'] or None. Default to None.
                Soft hint to choose the default backend if no specific backend
                was selected with the parallel_backend context manager. The
                default process-based backend is 'loky' and the default
                thread-based backend is 'threading'. Ignored if the ``backend``
                parameter is specified.
            progress: whether to display progress bar
            total: The number of elements in the iterator. Only used when `progress` is True.
            tqdm_kwargs: Any additional arguments supported by the `tqdm` progress bar.
            job_kwargs: Any additional arguments supported by `joblib.Parallel`.

        Example:

        ```python
        import datamol as dm
        runner = dm.JobRunner(n_jobs=4, progress=True, prefer="threads")
        results = runner(lambda x: x**2, [1, 2, 3, 4])
        ```
        """

        self.n_jobs = n_jobs
        self.batch_size = batch_size or "auto"
        self.prefer = prefer
        self.job_kwargs = job_kwargs
        self.job_kwargs.update(n_jobs=self.n_jobs, prefer=self.prefer, batch_size=self.batch_size)
        self.no_progress = not progress
        self.total = total
        self.tqdm_kwargs = tqdm_kwargs or {}

    @property
    def is_sequential(self):
        """Check whether the job is sequential or parallel"""
        return (self.n_jobs is None) or (self.n_jobs in [0, 1])

    @staticmethod
    def wrap_fn(fn: Callable, arg_type: Optional[str] = None, **fn_kwargs):
        """Small wrapper around a callable to properly format it's argument"""

        def _run(args: Any):
            if arg_type == "kwargs":
                fn_kwargs.update(**args)
                return fn(**fn_kwargs)
            elif arg_type == "args":
                return fn(*args, **fn_kwargs)
            return fn(args, **fn_kwargs)

        return _run

    def sequential(
        self,
        callable_fn: Callable,
        data: Iterable[Any],
        arg_type: Optional[str] = None,
        **fn_kwargs,
    ):
        """
        Run job in sequential version

        Args:
            callable_fn (callable): function to call
            data (iterable): input data
            arg_type (str, optional): function argument type ('arg'/None or 'args' or 'kwargs')
            fn_kwargs (dict, optional): optional keyword argument to pass to the callable funciton
        """
        total_length = JobRunner.get_iterator_length(data)

        if self.total is not None:
            self.tqdm_kwargs["total"] = self.total
        elif "total" not in self.tqdm_kwargs:
            self.tqdm_kwargs["total"] = total_length

        if "disable" not in self.tqdm_kwargs:
            self.tqdm_kwargs["disable"] = self.no_progress

        results = [
            JobRunner.wrap_fn(callable_fn, arg_type, **fn_kwargs)(dt)
            for dt in tqdm(data, **self.tqdm_kwargs)
        ]
        return results

    def parallel(
        self,
        callable_fn: Callable,
        data: Iterable[Any],
        arg_type: Optional[str] = None,
        **fn_kwargs,
    ):
        """
        Run job in parallel

        Args:
            callable_fn (callable): function to call
            data (iterable): input data
            arg_type (str, optional): function argument type ('arg'/None or 'args' or 'kwargs')
            fn_kwargs (dict, optional): optional keyword argument to pass to the callable funciton
        """

        total_length = JobRunner.get_iterator_length(data)

        if self.total is not None:
            self.tqdm_kwargs["total"] = self.total
        elif "total" not in self.tqdm_kwargs:
            self.tqdm_kwargs["total"] = total_length

        if "disable" not in self.tqdm_kwargs:
            self.tqdm_kwargs["disable"] = self.no_progress

        runner = JobRunner._parallel_helper(**self.job_kwargs)
        results = runner(**self.tqdm_kwargs)(
            delayed(JobRunner.wrap_fn(callable_fn, arg_type, **fn_kwargs))(dt) for dt in data
        )

        return results

    def __call__(self, *args, **kwargs):
        """
        Run job using the n_jobs attribute to determine regime
        """
        if self.is_sequential:
            return self.sequential(*args, **kwargs)
        return self.parallel(*args, **kwargs)

    @staticmethod
    def _parallel_helper(**joblib_args):
        r"""
        Parallel helper function for joblib with tqdm support
        """

        def run(**tq_args):
            def tmp(op_iter):
                with _tqdm_callback(tqdm(**tq_args)):
                    return Parallel(**joblib_args)(op_iter)

            return tmp

        return run

    @staticmethod
    def get_iterator_length(data):
        """Attempt to get the length of an iterator"""
        total_length = None
        try:
            total_length = len(data)
        except TypeError:
            # most likely a generator, ignore
            pass
        return total_length


@contextlib.contextmanager
def _tqdm_callback(pbar):
    """Report tqdm update on job completion"""

    class _CompletionCallBack(joblib.parallel.BatchCompletionCallBack):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def __call__(self, *args, **kwargs):
            pbar.update(n=self.batch_size)
            return super().__call__(*args, **kwargs)

    jlib_callback = joblib.parallel.BatchCompletionCallBack
    joblib.parallel.BatchCompletionCallBack = _CompletionCallBack
    try:
        yield pbar
    finally:
        joblib.parallel.BatchCompletionCallBack = jlib_callback
        pbar.close()


def parallelized(
    fn: Callable,
    inputs_list: Iterable[Any],
    scheduler: str = "processes",
    n_jobs: Optional[int] = -1,
    batch_size: Optional[int] = None,
    progress: bool = False,
    arg_type: str = "arg",
    total: Optional[int] = None,
    tqdm_kwargs: Optional[dict] = None,
    **job_kwargs,
) -> Sequence[Optional[Any]]:
    """Run a function in parallel.

    Args:
        fn: The function to run in parallel.
        inputs_list: List of inputs to pass to `fn`.
        scheduler: Choose between ["processes", "threads"]. Defaults
            to None which uses the default joblib "loky" scheduler.
        n_jobs: Number of process. Use 0 or None to force sequential.
                Use -1 to use all the available processors. For details see
                https://joblib.readthedocs.io/en/latest/parallel.html#parallel-reference-documentation
        batch_size: Whether to automatically batch `inputs_list`. You should only use it when the length
            of `inputs_list` is very large (>100k elements). The length of `inputs_list` must also be
            defined.
        progress: Display a progress bar. Defaults to False.
        arg_type: One of ["arg", "args", "kwargs]:
            - "arg": the input is passed as an argument: `fn(arg)` (default).
            - "args": the input is passed as a list: `fn(*args)`.
            - "kwargs": the input is passed as a map: `fn(**kwargs)`.
        total: The number of elements in the iterator. Only used when `progress` is True.
        tqdm_kwargs: Any additional arguments supported by the `tqdm` progress bar.
        job_kwargs: Any additional arguments supported by `joblib.Parallel`.

    Returns:
        The results of the execution as a list.
    """

    runner = JobRunner(
        n_jobs=n_jobs,
        batch_size=batch_size,
        progress=progress,
        prefer=scheduler,
        total=total,
        tqdm_kwargs=tqdm_kwargs,
        **job_kwargs,
    )
    return runner(fn, inputs_list, arg_type=arg_type)
