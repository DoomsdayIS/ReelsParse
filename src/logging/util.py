import logging

from functools import wraps, partial
from typing import Callable, Any


def with_logging(func: Callable[..., Any], logger: logging.Logger) -> Callable[..., Any]:
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        logger.info(f"Calling {func.__qualname__}")
        value = func(*args, **kwargs)
        logger.info(f"Finished calling {func.__qualname__}")
        return value

    return wrapper


with_default_logging = partial(with_logging, logger=logging.getLogger('reels_parser'))
