import os
from dotenv import load_dotenv
from functools import wraps
import json

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
    os.environ["TAVILY_API_KEY"] = os.getenv("TAVILY_API_KEY")

def serialize(obj):
    """
        Des:
            직렬화 불가능한 객체를 string 또는 dict 형태로 변환하는 함수
    """
    try:
        if hasattr(obj, "__dict__"):  # object에 __dict__ 속성이 있는지 판단
            return obj.__dict__
        elif isinstance(obj, (list, tuple, set)):  # object가 list, tuple, set 중 하나인지 판단
            return [serialize(o) for o in obj]  # 내부에 serialize가 불가능한 object가 있을수도 있으므로, 재귀적으로 호출
        elif isinstance(obj, dict):  # object가 dict인지 판단
            return {k: serialize(v) for k, v in obj.items()} # dict의 각 요소에 대해 serialize 재귀적으로 호출
        else:
            return str(obj)  # 기본적으로 string으로 변환
    except Exception as e:
        return f"<non-serializable: {str(obj)}>"  # 예외 발생

def trace_function(only_func_name=True,
                   print_json_format=False,
                   print_kwargs=False):
    """
        Des:
            랭그래프 입출력확인 위한 데코레이터
        Args:
            only_func_name: 함수 이름만 출력할지 여부
            print_json_format: 출력 형식을 json으로 할지 여부
            print_kwargs: kwargs 인자 출력 여부
    """
    def remove_keys(data, 
                    keys_to_remove:list=["usage_metadata","response_metadata"]):
        """
            Des:
                재귀적으로 데이터를 순회하며 지정된 키를 제거하는 함수.
                    - 출력값에 metadata 제거하기 위함.
            Args:
                data: 순회할 데이터 (딕셔너리 또는 리스트).
                keys_to_remove: 제거할 키들의 리스트.
            Returns:
                키가 제거된 데이터.
        """
        if isinstance(data, dict):
            return {key: remove_keys(value, keys_to_remove) 
                    for key, value in data.items() if key not in keys_to_remove}
        elif isinstance(data, list):
            return [remove_keys(item, keys_to_remove) for item in data]
        else:
            return data
        
    def wrapper(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            if only_func_name and (print_json_format or print_kwargs):
                print(f"{YELLOW}⚠️ Warning: 'only_func_name=True' 설정 시 "
                      f"'print_json_format'과 'print_kwargs' 옵션은 무시됩니다.{RESET}")
            if only_func_name:
                print(f"{GREEN}\n🚀 Passing Through [{func.__name__}] ..{RESET}")
            else:
                print(f"{GREEN}\n🚀 Passing Through [{func.__name__}] ..{RESET}")
                print(f"{RED}\n#### [Input State]{RESET}")
                if print_json_format:
                    serialized_args = [serialize(arg) for arg in args]
                    serialized_args = json.dumps(serialized_args, indent=4, ensure_ascii=False)
                    serialized_args = json.dumps(remove_keys(json.loads(serialized_args)), indent=4, ensure_ascii=False)
                    print(f"args: {serialized_args}")
                    if print_kwargs:
                        serialized_kwargs = {k: serialize(v) for k, v in kwargs.items()}
                        serialized_kwargs = json.dumps(serialized_kwargs, indent=4, ensure_ascii=False)
                        print(f"kwargs: {serialized_kwargs}")
                else:
                    print(f"args: {args}")
                    if print_kwargs:
                        print(f"kwargs: {kwargs}")
            result = func(*args, **kwargs)
            if only_func_name:
                pass
            else:
                print(f"{BLUE}\n#### [Output State]{RESET}")
                if print_json_format:
                    serialized_result = serialize(result)
                    serialized_result = json.dumps(serialized_result, indent=4, ensure_ascii=False)
                    serialized_result = json.dumps(remove_keys(json.loads(serialized_result)), indent=4, ensure_ascii=False)
                    print(f"result: {serialized_result}")
                else:
                    print(f"result: {result}")
            return result
        return wrapped
    return wrapper