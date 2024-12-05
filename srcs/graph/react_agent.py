import os
from langchain_community.tools import DuckDuckGoSearchRun, WikipediaQueryRun, PubmedQueryRun
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper, WikipediaAPIWrapper, PubMedAPIWrapper
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolExecutor
from langchain_core.messages import HumanMessage, AIMessage
from typing import TypedDict, Annotated, Sequence
import operator
import json

# 상태 정의
class AgentState(TypedDict):
    messages: Annotated[Sequence[dict], operator.add]

# 도구 정의
tools = [
    DuckDuckGoSearchRun(api_wrapper=DuckDuckGoSearchAPIWrapper(max_results=10, region="en-en")),
    WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper()),
    PubmedQueryRun(api_wrapper=PubMedAPIWrapper())
]
tool_executor = ToolExecutor(tools)

# 모델 설정
model = ChatOpenAI(temperature=0, streaming=True)

# 노드 함수 정의
def process_input(state):
    user_message = state['messages'][-1]
    return {"messages": [{"type": "user", "content": user_message}]}

def agent_action(state):
    user_message = state['messages'][-1]["content"]
    response = model.invoke([HumanMessage(content=user_message)])
    return {"messages": [response]}

def execute_tool(state):
    tool_request = state['messages'][-1]
    action = {
        "tool": tool_request.get("tool_name"),
        "input": json.loads(tool_request.get("tool_arguments"))
    }
    tool_response = tool_executor.invoke(action)
    return {"messages": [{"type": "tool", "content": str(tool_response)}]}

def should_continue(state):
    last_message = state['messages'][-1]
    if "tool_name" in last_message:
        return "execute_tool"
    else:
        return "end"

# 그래프 정의
workflow = StateGraph(AgentState)

# 노드 추가
workflow.add_node("process_input", process_input)
workflow.add_node("agent_action", agent_action)
workflow.add_node("execute_tool", execute_tool)

# 엣지 추가
workflow.set_entry_point("process_input")
workflow.add_edge("process_input", "agent_action")
workflow.add_conditional_edges("agent_action", should_continue, {"execute_tool": "execute_tool", "end": END})
workflow.add_edge("execute_tool", "agent_action")

# 컴파일
app = workflow.compile()