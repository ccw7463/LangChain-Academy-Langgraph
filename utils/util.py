import os
from dotenv import load_dotenv
from functools import wraps

RESET = "\033[0m"        # Reset to default
RED = "\033[91m"         # Bright Red
BLUE = "\033[94m"        # Bright Blue
GREEN = "\033[92m"        # Bright Green
YELLOW = "\033[93m"       # Bright Yellow
PINK = "\033[95m"         # Bright Pink

def set_env():
    load_dotenv()
    os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
    os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
    os.environ["LANGCHAIN_TRACING_V2"] = "true"
    os.environ["LANGCHAIN_PROJECT"] = "langchain-academy"

def trace_function(enable_print=True):
    def wrapper(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if enable_print:
                print(f"\n{GREEN}🚀 Passing Through [{func.__name__}] ..{RESET}")
                print(f"\n{RED}#### [Input State]{RESET}")
                print(f"  args: {args}")
                print(f"  kwargs: {kwargs}")
            result = func(*args, **kwargs)
            if enable_print:
                print(f"\n{BLUE}#### [Output State]{RESET}")
                print(f"  result: {result}")
            return result
        return wrapper
    return wrapper