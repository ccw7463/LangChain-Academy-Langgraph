import os
import uuid
import time
from dotenv import load_dotenv
from functools import wraps
import argparse
from ml_collections import ConfigDict
from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver
from langgraph.store.memory import InMemoryStore
from langgraph.store.base import BaseStore
from langchain_openai import ChatOpenAI
from langchain_huggingface import HuggingFaceEndpoint
from langchain_huggingface import ChatHuggingFace
from langchain_core.runnables import RunnableConfig
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage, RemoveMessage
from dotenv import load_dotenv
load_dotenv()

RESET = "\033[0m"        # Reset to default
RED = "\033[91m"         # Bright Red
BLUE = "\033[94m"        # Bright Blue
GREEN = "\033[92m"        # Bright Green
YELLOW = "\033[93m"       # Bright Yellow
PINK = "\033[95m"         # Bright Pink

def trace_function(enable_print=True, only_func_name=False):
    def wrapper(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            if enable_print:
                if only_func_name:
                    print(f"\n... Passing Through [{func.__name__}] ...")
                else:
                    print(f"\n... Passing Through [{func.__name__}] ...")
                    print(f"{RED}#### [Input State]{RESET}")
                    print(f"  args: {args}")
                    print(f"  kwargs: {kwargs}")
            result = func(*args, **kwargs)  # 원본 함수 호출
            if enable_print:
                if only_func_name:
                    pass
                else:
                    print(f"\n{BLUE}#### [Output State]{RESET}")
                    print(f"  result: {result}")
            return result
        return wrapped
    return wrapper

class ToolConversation:
    def __init__(self, llm):
        self.system_prompt = "You are a helpful assistant tasked with performing arithmetic on a set of inputs."
        self.tools = [self._tool_add]
        self.llm = llm
        self.llm_with_tools = self.llm.bind_tools(self.tools)
        self._build_graph()

    def __call__(self,
                 messages):
        return self._call_graph(messages)

    def _call_graph(self, 
                    messages):
        """
            Des:
                그래프 호출 함수
        """
        return self.graph.invoke({"messages": messages})

    def _build_graph(self):
        """
            Des:
                그래프 생성함수
        """
        builder = StateGraph(MessagesState)
        builder.add_node("_node_assistant", self._node_assistant)
        builder.add_node("tools", ToolNode(self.tools))
        builder.add_edge(START, "_node_assistant")
        builder.add_conditional_edges("_node_assistant", tools_condition)
        builder.add_edge("tools", "_node_assistant")
        self.graph = builder.compile()

    @trace_function(enable_print=True, only_func_name=True)
    def _node_assistant(self, state:MessagesState):
        return {"messages": [self.llm_with_tools.invoke([SystemMessage(content=self.system_prompt)] + state["messages"])]}

    @trace_function(enable_print=True, only_func_name=True)
    def _tool_add(self,
                  a: int, 
                  b: int) -> int:
        """Adds a and b.

        Args:
            a: first int
            b: second int
        """
        return a + b
    
class ConversationTest:
    def __init__(self, llm):
        self.LIMIT_LENGTH = 6
        self.ShortTermMemory = MemorySaver()
        self.LongTermMemory = InMemoryStore()
        self.system_prompt = "당신은 사용자 요청에 답변하는 유용한 챗봇입니다."
        self.llm = llm
        self._set_config()
        self._build_graph()

    def __call__(self,
                 messages:list[str]):
        return self._call_graph(messages)

    def _call_graph(self, 
                    messages):
        """
            Des:
                그래프 호출 함수
        """
        return self.graph.invoke({"messages": messages}, config=self.config)
        
    def _build_graph(self):
        """
            Des:
                그래프 생성함수
        """
        builder = StateGraph(MessagesState)
        builder.add_node("_node_answer", self._node_answer)
        builder.add_edge(START, "_node_answer")
        builder.add_edge("_node_answer", END)
        self.graph = builder.compile(checkpointer=self.ShortTermMemory)

    @trace_function(enable_print=True, only_func_name=True)
    def _node_answer(self, 
                    state: MessagesState):
        """
            Des:
                사용자 메시지를 인식하고, 답변을 생성하는 노드
        """
        prompt = [SystemMessage(content=self.system_prompt)] + state["messages"]
        response = self.llm.invoke(prompt)
        return {"messages": response}
    
    def _generate_session_id(self):
        session_id = str(uuid.uuid4())
        return session_id
        
    def _set_config(self,
                    session_id:str="test_session_id",
                    user_id:str="test_user_id"):
        session_id = self._generate_session_id()
        self.config = {"configurable": {"thread_id": session_id,
                                        "user_id": user_id}}


def main(args):
    if args.model_type == "huggingface":
        llm_endpoint = HuggingFaceEndpoint(
            endpoint_url=args.endpoint_url, # Endpoint 주소 (TGI 사용)
            huggingfacehub_api_token=os.getenv("HF_API_TOKEN"), # HuggingFace API 토큰
            max_new_tokens=4096,
            top_k=1,
            top_p=0.001,
            temperature=0.001,
            repetition_penalty=1.03,
            stop_sequences=['<end_of_turn>','<eos>']
        )
        llm = ChatHuggingFace(
            llm=llm_endpoint,
            model_id="rtzr/ko-gemma-2-9b-it",
            stream_mode=True
        ).bind(max_tokens=4096)
    else:
        os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
        llm = ChatOpenAI(model="gpt-4o")
    
    tool_test(llm)
    chat_test(llm)

def tool_test(llm):
    tool_conversation = ToolConversation(llm)
    print(f"{GREEN}=========================================={RESET}")
    print(f"{GREEN}  [Langgraph 기반 툴 테스트를 시작합니다]{RESET}")
    print(f"{GREEN}=========================================={RESET}")
    messages = "Add 3 and 4"
    print(f" {YELLOW}[요청 메시지] : {messages}{RESET}")
    messages = tool_conversation(messages)
    for message in messages['messages']:
        if type(message).__name__ == "ToolMessage":
            print(f"\n{BLUE}### [중간 계산 결과] :\n {message.content}{RESET}\n")
    print(f"{BLUE}### [답변 메시지] :\n {messages['messages'][-1].content.strip()}{RESET}\n")
    
def chat_test(llm):
    conversation = ConversationTest(llm)
    print(f"{GREEN}=========================================={RESET}")
    print(f"{GREEN} [Langgraph 기반 채팅 테스트를 시작합니다]{RESET}")
    print(f"{GREEN}=========================================={RESET}")
    messages_lst = [
        "안녕하세요, 구글에 대해 알려주세요.",
        "요약해서 다시 설명해주세요.",
        "요약한 내용을 이해하기 쉽게 HTML 형태로 정리해주세요.",
    ]
    for message in messages_lst:
        print(f"{YELLOW}### [요청 메시지] : {message}{RESET}")
        convs = conversation(message)
        print(f"\n{BLUE}### [답변 메시지] :\n {convs['messages'][-1].content.strip()}{RESET}\n")
    
if __name__ == "__main__":    
    start_time = time.time()
    parser = argparse.ArgumentParser()
    parser.add_argument("--endpoint_url", type=str, default="http://192.168.1.21:11980")
    parser.add_argument("--model_type", type=str, default="gpt")
    args = parser.parse_args()
    main(args)
    end_time = time.time()
    print(f"\n{RED}[테스트 종료] 실행 시간: {end_time - start_time}초{RESET}")