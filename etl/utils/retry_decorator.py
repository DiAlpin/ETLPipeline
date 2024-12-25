
import time
from functools import wraps



def retry(max_attempts=5, delay=1, backoff_factor=2, exceptions=(ValueError,)):
    """
    Decorator for implementing exponential backoff retry mechanism.
    
    :param max_attempts: Maximum number of retry attempts
    :param delay: Initial delay between retries
    :param backoff_factor: Factor to increase delay between retries
    :param exceptions: Tuple of exceptions to catch and retry
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            current_delay = delay
            
            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    attempts += 1
                    
                    if attempts == max_attempts:
                        # logging.error(f"Max attempts reached. Final error: {e}")
                        print(f"Max attempts reached. Final error: {e}")
                        
                        raise
                    
                    # logging.warning(f"Attempt {attempts} failed: {e}. Retrying in {current_delay} seconds.")
                    print(f"Attempt {attempts} failed: {e}. Retrying in {current_delay} seconds.")
                    
                    time.sleep(current_delay)
                    current_delay *= backoff_factor
            
            return None
        return wrapper
    return decorator