import os
from dotenv import load_dotenv
def set_env():
    load_dotenv()
    os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
    os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
    os.environ["LANGCHAIN_TRACING_V2"] = "true"
    os.environ["LANGCHAIN_PROJECT"] = "langchain-academy"
    

def print_state(state, 
                type):
    if type == "input":
        print("\n#### Input State ..")
    elif type == "output":
        print("\n#### Output State ..")
    for msg in state["messages"]: #TODO : state 키값이 다른거 쓰더라도 되도록 변경필요
        msg_type = msg.type.upper()
        if msg_type == "AI" and msg.content == "":
            func = msg.additional_kwargs['tool_calls'][0]['function']
            print(f"[{msg_type}] : Tool Call")
            print(f"  - Function Name: {func['name']}")
            print(f"  - Function Arguments: {func['arguments']}")
        else:
            print(f"[{msg_type}] : {msg.content}")


def auto_log_and_state(func):
    def wrapper(*args, **kwargs):
        state = args[0] if args else None
        print(f"\n## Passing Through [{func.__name__}] ..")
        print_state(state, "input")
        result = func(*args, **kwargs)
        print_state(result, "output")
        return result
    return wrapper