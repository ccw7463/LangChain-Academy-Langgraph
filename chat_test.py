from modules.base import *

class ConversationTest:
    def __init__(self):
        self.LIMIT_LENGTH = 6
        self.ShortTermMemory = MemorySaver()
        self.LongTermMemory = InMemoryStore()
        self.system_prompt = "당신은 사용자 요청에 답변하는 유용한 챗봇입니다."
        self.answer_prompt = """당신은 [사용자 정보]를 통해 답변하는 유용한 챗봇입니다.
[사용자 정보]:
{memory}"""
        self.create_memory_prompt ="""당신은 사용자의 응답을 개인화하기 위해 사용자에 대한 정보를 수집하고 있습니다.
[현재 사용자 정보]:
{memory}

지침:
1. 아래의 채팅 기록을 주의 깊게 검토하세요.
2. 사용자에 대한 새로운 정보를 식별하세요. 예를 들면:
- 개인 정보 (이름, 위치 등)
- 선호 사항 (좋아하는 것, 싫어하는 것 등)
- 관심사와 취미
- 과거 경험
- 목표나 미래 계획   
3. 새로운 정보를 기존 메모리와 병합하세요.
4. 메모리는 명확한 불릿 리스트 형식으로 작성하세요.
5. 새로운 정보가 기존 메모리와 충돌할 경우, 가장 최근 정보를 유지하세요.
6. 만약 새로운 정보가 없다면 [현재 사용자 정보] 부분의 내용을 그대로 출력하세요.
7. 기존 정보를 유지할경우 [현재 사용자 정보] 부분의 내용을 그대로 출력하세요.

기억하세요: 사용자가 직접적으로 언급한 사실적인 정보만 포함해야 합니다. 추측이나 추론을 하지 마세요.

아래의 채팅 기록을 바탕으로 사용자 정보를 업데이트하세요:

출력 양식은 반드시 아래를 따르세요.

- 정보 종류 : 정보 내용
- 정보 종류 : 정보 내용
...
"""
        self.llm = ChatOpenAI(model="gpt-4o")
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
        builder.add_node("_node_write_memory", self._node_write_memory)
        builder.add_node("_node_optimize_memory", self._node_optimize_memory)
        builder.add_edge(START, "_node_answer")
        builder.add_edge("_node_answer", "_node_write_memory")
        builder.add_conditional_edges("_node_write_memory", self._check_memory_length)
        builder.add_edge("_node_optimize_memory", END)
        self.graph = builder.compile(checkpointer=self.ShortTermMemory,
                                     store=self.LongTermMemory)

    @trace_function(only_func_name=True)
    def _node_answer(self, 
                    state: MessagesState, 
                    config: RunnableConfig,
                    store: BaseStore):
        """
            Des:
                사용자 메시지를 인식하고, 답변을 생성하는 노드
        """
        namespace = ("memories", config["configurable"]["user_id"])
        key = "chat_user_memory"
        memory = self._get_memory(namespace=namespace, 
                                  key=key, 
                                  store=store)
        system_message = self.answer_prompt.format(memory=memory)
        prompt = [SystemMessage(content=system_message)] + state["messages"]
        # print(f"{PINK}\n{prompt[0].content}\n{RESET}")
        response = self.llm.invoke(prompt)
        return {"messages": response}

    @trace_function(only_func_name=True)
    def _node_write_memory(self,
                          state: MessagesState, 
                          config: RunnableConfig, 
                          store: BaseStore):
        """
            Des:
                사용자 메시지를 인식하고, 개인정보로 저장하는 노드
        """
        namespace = ("memories", config["configurable"]["user_id"])
        key = "chat_user_memory"
        memory = self._get_memory(namespace=namespace, 
                                  key=key, 
                                  store=store)
        system_message = self.create_memory_prompt.format(memory=memory)
        prompt = [SystemMessage(content=system_message)]+state["messages"]
        response = self.llm.invoke(prompt)
        store.put(namespace=namespace, 
                  key=key, 
                  value={"memory":response.content})
    
    @trace_function(only_func_name=True)
    def _node_optimize_memory(self,
                              state: MessagesState):
        """
            Des:
                메모리 최적화 함수
        """
        delete_messages = [RemoveMessage(id=m.id) for m in state["messages"][:self.LIMIT_LENGTH//2]]
        return {"messages": delete_messages}
    
    def _generate_session_id(self):
        session_id = str(uuid.uuid4())
        return session_id
        
    def _set_config(self,
                    session_id:str="test_session_id",
                    user_id:str="test_user_id"):
        session_id = self._generate_session_id()
        self.config = {"configurable": {"thread_id": session_id,
                                        "user_id": user_id}}

    def _check_memory_length(self,
                             state: MessagesState):
        """
            Des:
                메모리 길이 체크 함수
        """
        if len(state["messages"]) > self.LIMIT_LENGTH:
            return "_node_optimize_memory"
        else:
            return END
    
    def _get_memory(self,
                    namespace, 
                    key,
                    store:BaseStore):
        """
            Des:
                현재 저장된 사용자 정보를 가져오는 함수
        """
        existing_memory = store.get(namespace=namespace,
                                    key=key)
        return existing_memory.value.get('memory') if existing_memory else ""

def main():
    chat_test()

def chat_test():
    conversation = ConversationTest()
    print(f"{GREEN}========================================{RESET}")
    print(f"{GREEN}[Langgraph 기반 채팅 테스트를 시작합니다.]{RESET}")
    print(f"{GREEN}========================================{RESET}")
    messages_lst = ["안녕하세요, 저는 홍길동이라고 합니다.",
                    "저는 올해 25살이고, 한국대학교에서 재학중이에요.",
                    "제 전공은 인공지능이고 요즘 LLM 분야에 관심이 많아요.",
                    "제가 제일 좋아하는 음식은 돼지고기이고, 싫어하는 음식은 딱히없어요.",
                    "저에 대해 아시는게 있나요?"]

    for message in messages_lst:
        convs = conversation(message)
        print(f"\n{YELLOW}요청 메시지 : {message}{RESET}")
        print(f"\n{BLUE}답변 메시지 : {convs['messages'][-1].content}{RESET}\n")
    print(f"{GREEN}========================================{RESET}")
    print(f"{GREEN}        [대화가 종료되었습니다.]{RESET}")
    print(f"{GREEN}========================================{RESET}")

    print(f"{RED}\n사용자와의 대화로부터 추출한 정보는 다음과 같습니다.\n{RESET}")
    namespace = ("memories", conversation.config["configurable"]["user_id"])
    key = "chat_user_memory"
    memory = conversation._get_memory(namespace=namespace, 
                                    key=key, 
                                    store=conversation.LongTermMemory)
    print(f"{RED}{memory}{RESET}")
    
if __name__ == "__main__":  
    import time  
    start_time = time.time()
    main()
    end_time = time.time()
    print(f"\n\n{PINK}🎉 [테스트 종료] 실행 시간: {end_time - start_time}초{RESET}")