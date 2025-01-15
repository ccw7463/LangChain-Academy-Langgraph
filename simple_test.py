import uuid
import time
import argparse
from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.checkpoint.memory import MemorySaver
from langgraph.store.memory import InMemoryStore
from langchain_huggingface import HuggingFaceEndpoint
from langchain_huggingface import ChatHuggingFace
from langchain_core.messages import SystemMessage

RESET = "\033[0m"        # Reset to default
RED = "\033[91m"         # Bright Red
BLUE = "\033[94m"        # Bright Blue
GREEN = "\033[92m"        # Bright Green
YELLOW = "\033[93m"       # Bright Yellow
PINK = "\033[95m"         # Bright Pink
    
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
    llm_endpoint = HuggingFaceEndpoint(
        endpoint_url=args.endpoint_url,
        max_new_tokens=2048,
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
    ).bind(max_tokens=2048)
    
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
    args = parser.parse_args()
    main(args)
    end_time = time.time()
    print(f"\n{RED}[테스트 종료] 실행 시간: {end_time - start_time}초{RESET}")