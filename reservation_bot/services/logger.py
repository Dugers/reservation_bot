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

def log_args_returns(args_level=logging.DEBUG, return_level=logging.INFO):
    def decorator(func):
        is_async = inspect.iscoroutinefunction(func)
        
        def log_args(*args, **kwargs):
            sig = inspect.signature(func)
            bound_args = sig.bind(*args, **kwargs)
            bound_args.apply_defaults()
            
            args_str = []
            for name, value in bound_args.arguments.items():
                args_str.append(f"{name}={repr(value)}")
            
            logging.log(
                level=args_level,
                msg=f"Calling {func.__name__} with args: {', '.join(args_str)}"
            )

        def log_return(value):
            logging.log(
                level=return_level,
                msg=f"Function {func.__name__} returned: {repr(value)}"
            )

        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            log_args(*args, **kwargs)
            try:
                result = func(*args, **kwargs)
                log_return(result)
                return result
            except Exception as e:
                raise

        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            log_args(*args, **kwargs)
            try:
                result = await func(*args, **kwargs)
                log_return(result)
                return result
            except Exception as e:
                raise

        return async_wrapper if is_async else sync_wrapper
    
    return decorator

def combined_logger(args_level=logging.DEBUG, return_level=logging.INFO, exception_level=logging.ERROR):
    def decorator(func):
        func_with_args_log = log_args_returns(args_level, return_level)(func)
        func_with_all_logs = log_exception(exception_level)(func_with_args_log)
        
        return wraps(func)(func_with_all_logs)
    
    return decorator

__all__ = [
    "log_exception",
    "log_args_returns",
    "combined_logger"
]