import os
from dotenv import load_dotenv
RESET = "\033[0m"        # Reset to default
RED = "\033[91m"         # Bright Red
BLUE = "\033[94m"        # Bright Blue
GREEN = "\033[92m"        # Bright Green
YELLOW = "\033[93m"       # Bright Yellow

def set_env():
    load_dotenv()
    os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
    os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
    os.environ["LANGCHAIN_TRACING_V2"] = "true"
    os.environ["LANGCHAIN_PROJECT"] = "langchain-academy"
    
import inspect


# TODO : 로깅위한 데코레이터 만들기
def auto_log_and_state(func):
    def wrapper(*args, **kwargs):
        # Print function name
        print(f"\n🚀 Executing Node: [{func.__name__}]")

        # Get the function signature
        sig = inspect.signature(func)
        bound_args = None
        try:
            # Attempt to bind arguments
            bound_args = sig.bind(*args, **kwargs)
            bound_args.apply_defaults()  # Apply default values
        except TypeError as e:
            print(f"❌ Error in binding arguments for function '{func.__name__}': {e}")
            raise

        # Log input arguments
        print("\n📥 Inputs:")
        for name, value in bound_args.arguments.items():
            print(f"  - {name}: {value}")

        # Execute the function
        try:
            result = func(*args, **kwargs)
        except Exception as e:
            print(f"❌ Error while executing function '{func.__name__}': {e}")
            raise

        # Log output results
        print("\n📤 Outputs:")
        if isinstance(result, dict):  # Check if result is a dictionary
            for key, value in result.items():
                print(f"  - {key}: {value}")
        else:
            print(f"  - {result}")

        # Return the function result
        return result

    return wrapper




# def print_state(state, 
#                 type):

#     if type == "input":
#         print(f"\n{RED}#### [Input State]{RESET}")
#     elif type == "output":
#         print(f"\n{BLUE}#### [Output State]{RESET}")
        
#     if hasattr(state, "dict"):  # Check if object has dictionary (processing for Pydantic object)
#         state = state.dict()

#     if "messages" in state:
#         for msg in state["messages"]:

#             # Handle Pydantic objects like HumanMessage
#             if isinstance(msg, dict):
#                 msg_type = msg.get("type", "UNKNOWN").upper()
#                 content = msg.get("content", "N/A")
#                 additional_kwargs = msg.get("additional_kwargs", {})
#             elif hasattr(msg, "type"):  # For HumanMessage-like objects
#                 msg_type = getattr(msg, "type", "UNKNOWN").upper()
#                 content = getattr(msg, "content", "N/A")
#                 additional_kwargs = getattr(msg, "additional_kwargs", {})

#             # Process messages
#             if msg_type == "AI" and content == "":
#                 tool_calls = additional_kwargs.get("tool_calls", [])
#                 if tool_calls:
#                     func = tool_calls[0]
#                     print(f"[{msg_type}] : Tool Call")
#                     print(f"  - Function Name: {func.get('function', {}).get('name', 'N/A')}")
#                     print(f"  - Function Arguments: {func.get('function', {}).get('arguments', 'N/A')}")
#                 else:
#                     print(f"[{msg_type}] : Tool Call Details Not Found")
#             else:
#                 print(f"[{msg_type}] : {content}")
    
#     for key, value in state.items():
#         if key != "messages":
#             print(f"{key} : {value}")

# def auto_log_and_state(func):
#     def wrapper(*args, **kwargs):
#         # Get state and print
#         state = None
#         for arg in args:
#             if hasattr(arg, "dict"):  # Check if it's a Pydantic object
#                 state = arg.dict()  # Convert Pydantic object to dictionary
#                 break
#             if isinstance(arg, dict):  # If already a dictionary
#                 state = arg
#                 break
#         if state is None:
#             state = kwargs.get("state")
#             if hasattr(state, "dict"):  # Check if state in kwargs is Pydantic
#                 state = state.dict()

#         print(f"\n{GREEN}🚀 Passing Through [{func.__name__}] ..{RESET}")
#         if state:
#             print_state(state, "input")
#         else:
#             print("\n⚠️ No state found in input.")

#         # Execute function
#         result = func(*args, **kwargs)
#         if hasattr(result, "dict"):  # Check if result is Pydantic
#             print_state(result.dict(), "output")
#         elif isinstance(result, dict):  # Ensure result is a dictionary
#             print_state(result, "output")
#         else:
#             print("\n⚠️ Output is not a valid state. Output can be routing or other:", f"[{result}]")

#         return result
#     return wrapper
