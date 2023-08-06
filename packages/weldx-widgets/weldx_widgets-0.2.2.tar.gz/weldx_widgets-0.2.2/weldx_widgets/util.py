import asyncio
from contextlib import contextmanager


@contextmanager
def matplotlib_backend(backend):
    from IPython import get_ipython

    ipy = get_ipython()
    if ipy:
        old = ipy.run_line_magic("matplotlib", "")
        ipy.run_line_magic("matplotlib", "ipympl")

        yield

        print("restoring")
        ipy.run_line_magic("matplotlib", old)


from time import time


class Timer:
    def __init__(self, timeout, callback):
        self._timeout = timeout
        self._callback = callback

    async def _job(self):
        await asyncio.sleep(self._timeout)
        self._callback()

    def start(self):
        self._task = asyncio.ensure_future(self._job())

    def cancel(self):
        self._task.cancel()


def throttle(wait):
    """Decorator that prevents a function from being called
    more than once every wait period."""

    def decorator(fn):
        time_of_last_call = 0
        scheduled, timer = False, None
        new_args, new_kwargs = None, None

        def throttled(*args, **kwargs):
            nonlocal new_args, new_kwargs, time_of_last_call, scheduled, timer

            def call_it():
                nonlocal new_args, new_kwargs, time_of_last_call, scheduled, timer
                time_of_last_call = time()
                fn(*new_args, **new_kwargs)
                scheduled = False

            time_since_last_call = time() - time_of_last_call
            new_args, new_kwargs = args, kwargs
            if not scheduled:
                scheduled = True
                new_wait = max(0, wait - time_since_last_call)
                timer = Timer(new_wait, call_it)
                timer.start()

        return throttled

    return decorator
