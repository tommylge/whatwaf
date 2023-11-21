import signal
from collections.abc import Callable
from functools import wraps
from types import FrameType
from typing import Any


def timeout(seconds: int) -> Callable:
    """Throw error if function takes too much time.

    Args:
        seconds (int): Timeout in seconds.

    Returns:
        Callable: Function wrapped.
    """

    def decorator(func: Callable) -> Callable:
        """Stop function that takes too much time with this decorator.

        Args:
            func (Callable): The function where the decorator was put.

        Returns:
            Callable: The result of the function.
        """

        def _handle_timeout(signum: int, frame: FrameType | None) -> TimeoutError:
            """Throw Exception when timeout occurs.

            Args:
                signum (int): The signal number.
                frame (Optional[FrameType]): The current stack frame (None or a frame
                object; for a description of frame objects.

            Raises:
                TimeoutError: Exception when timeout occurs.
            """
            raise TimeoutError("Stopped the function")

        def wrapper(*args: list[Any], **kwargs: dict[str, Any]) -> Any:
            r"""Wrap the function with the decorator..

            Args:
                \*args: List of arguments.
                \*\*kwargs: Dict of keywords arguments.

            Returns:
                Callable: Function.
            """
            signal.signal(signal.SIGALRM, _handle_timeout)
            signal.setitimer(
                signal.ITIMER_REAL,
                seconds,
            )  # used timer instead of alarm
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)
            return result

        return wraps(func)(wrapper)

    return decorator
