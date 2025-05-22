import inspect
import logging
from functools import wraps

def log_exception(level=logging.ERROR):
    def decorator(func):
        is_async = inspect.iscoroutinefunction(func)

        def log_exception(e: Exception):
            logging.log(
                level=level,
                msg=f"Exception in {func.__name__}: {str(e)}",
                exc_info=True
            )

        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                log_exception(e)
                raise

        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                log_exception(e)
                raise

        return async_wrapper if is_async else sync_wrapper
    
    return decorator