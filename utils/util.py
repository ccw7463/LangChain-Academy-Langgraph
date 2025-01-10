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

def trace_function(enable_print=True, only_func_name=False):
    def wrapper(func):
        @wraps(func)
        def wrapped(*args, **kwargs):  # 이름을 "wrapped"로 변경하여 구분
            if enable_print:
                if only_func_name:
                    print(f"{GREEN}\n🚀 Passing Through [{func.__name__}] ..{RESET}")
                else:
                    print(f"{GREEN}\n🚀 Passing Through [{func.__name__}] ..{RESET}")
                    print(f"{RED}\n#### [Input State]{RESET}")
                    print(f"  args: {args}")
                    print(f"  kwargs: {kwargs}")
            result = func(*args, **kwargs)  # 원본 함수 호출
            if enable_print:
                if only_func_name:
                    pass
                else:
                    print(f"{BLUE}\n#### [Output State]{RESET}")
                    print(f"  result: {result}")
            return result
        return wrapped
    return wrapper