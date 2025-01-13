from modules.base import *

class ToolConversation:
    def __init__(self):
        self.system_prompt = "You are a helpful assistant tasked with performing arithmetic on a set of inputs."
        self.tools = [self._tool_divide, self._tool_add, self._tool_multiply]
        self.llm = ChatOpenAI(model="gpt-4o")
        self.llm_with_tools = self.llm.bind_tools(self.tools, parallel_tool_calls=False)
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

    @trace_function(only_func_name=True)
    def _node_assistant(self, state:MessagesState):
        return {"messages": [self.llm_with_tools.invoke([SystemMessage(content=self.system_prompt)] + state["messages"])]}

    @trace_function(only_func_name=True)
    def _tool_multiply(self,
                       a: int, 
                       b: int) -> int:
        """Multiply a and b.

        Args:
            a: first int
            b: second int
        """
        return a * b

    @trace_function(only_func_name=True)
    def _tool_add(self,
                  a: int, 
                  b: int) -> int:
        """Adds a and b.

        Args:
            a: first int
            b: second int
        """
        return a + b

    @trace_function(only_func_name=True)
    def _tool_divide(self,
                     a: int, 
                     b: int) -> float:
        """Divide a and b.

        Args:
            a: first int
            b: second int
        """
        return a / b

def main():
    tool_test()

def tool_test():
    tool_conversation = ToolConversation()
    print(f"{GREEN}========================================{RESET}")
    print(f"{GREEN} [Langgraph 기반 툴 테스트를 시작합니다.]{RESET}")
    print(f"{GREEN}========================================{RESET}")
    messages = "Add 3 and 4. Multiply the output by 2. Divide the output by 5"
    print(f" {YELLOW}요청 메시지 : {messages}{RESET}")
    messages = tool_conversation(messages)
    print(f"{GREEN}========================================{RESET}")
    print(f"{GREEN}        [대화가 종료되었습니다.]{RESET}")
    print(f"{GREEN}========================================{RESET}")
    for message in messages['messages']:
        if type(message).__name__ == "ToolMessage":
            print(f"{BLUE}중간 결과 : {message.content}{RESET}")
    print(f"{BLUE}최종 답변 메시지 : {messages['messages'][-1].content}{RESET}\n")
    
if __name__ == "__main__":  
    import time  
    start_time = time.time()
    main()
    end_time = time.time()
    print(f"\n\n{PINK}🎉 [테스트 종료] 실행 시간: {end_time - start_time}초{RESET}")