import asyncio
from functools import wraps
from typing import TypeVar, Callable, Type, Tuple, Union

from nonebot import logger
from typing_extensions import ParamSpec

T = TypeVar('T')
P = ParamSpec('P')


def auto_retry(t_error: Union[Type[BaseException], Tuple[Type[BaseException]]], retry_interval: float = 5.0,
               max_retry: int = 3):
    def decorator(func: Callable[P, T]) -> Callable[P, T]:
        @wraps(func)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            err = None

            for i in range(max_retry):
                try:
                    return await func(*args, **kwargs)
                except t_error as e:
                    logger.opt(exception=e).error(f"Retrying... {i + 1}/{max_retry}")
                    err = e
                    await asyncio.sleep(retry_interval)
                except Exception as e:
                    raise e

            raise err

        return wrapper

    return decorator
