"""
LangGraph-based ReAct search agent shared by Streamlit pages.
Replaces deprecated initialize_agent / AgentExecutor / WebResearchRetriever.
"""
from typing import Any, Optional

from langchain_community.agent_toolkits.load_tools import load_tools
from langchain_community.tools import DuckDuckGoSearchRun, PubmedQueryRun, WikipediaQueryRun
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper, PubMedAPIWrapper, WikipediaAPIWrapper
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage

# LangGraph create_react_agent: prefer prebuilt when available
try:
    from langgraph.prebuilt import create_react_agent
except ImportError:
    create_react_agent = None


def build_search_tools(
    include_arxiv: bool = True,
    ddg_max_results: int = 10,
    ddg_region_en: str = "en-en",
    ddg_region_kr: str = "kr-kr",
    ddg_time: Optional[str] = None,
) -> list:
    """Build search tools (DuckDuckGo, Wikipedia, Pubmed, optional Arxiv) for ReAct agent."""
    ddg_kwargs = {"max_results": ddg_max_results}
    if ddg_time is not None:
        ddg_kwargs["time"] = ddg_time
    tools = [
        DuckDuckGoSearchRun(
            api_wrapper=DuckDuckGoSearchAPIWrapper(region=ddg_region_en, **ddg_kwargs)
        ),
        DuckDuckGoSearchRun(
            api_wrapper=DuckDuckGoSearchAPIWrapper(region=ddg_region_kr, **ddg_kwargs)
        ),
        WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper()),
        PubmedQueryRun(api_wrapper=PubMedAPIWrapper()),
    ]
    if include_arxiv:
        tools.extend(load_tools(["arxiv"]))
    return tools


def _messages_to_langgraph(messages: list[dict[str, str]]) -> list[BaseMessage]:
    """Convert list of {'role': 'user'|'assistant'|'system', 'content': ...} to LangChain messages."""
    out = []
    for m in messages:
        role = (m.get("role") or "user").lower()
        content = m.get("content") or ""
        if role == "system":
            out.append(SystemMessage(content=content))
        elif role == "user":
            out.append(HumanMessage(content=content))
        elif role == "assistant":
            out.append(AIMessage(content=content))
    return out


def create_search_agent(model: Any, tools: list, *, checkpointer: Any = None):
    """
    Create a LangGraph ReAct agent with the given model and tools.
    Returns a compiled graph. Invoke with {"messages": [HumanMessage(...), ...]}.
    """
    if create_react_agent is None:
        raise ImportError("langgraph.prebuilt.create_react_agent is not available; install langgraph.")
    return create_react_agent(model, tools, checkpointer=checkpointer)


def invoke_agent(agent: Any, messages: list[BaseMessage] | list[dict], config: Optional[dict] = None) -> str:
    """
    Run the agent and return the final assistant text.
    messages: list of BaseMessage or list of dicts with 'role' and 'content'.
    """
    if messages and isinstance(messages[0], dict):
        messages = _messages_to_langgraph(messages)
    config = config or {"configurable": {"thread_id": "default"}}
    result = agent.invoke({"messages": messages}, config=config)
    out_messages = result.get("messages", [])
    if not out_messages:
        return ""
    last = out_messages[-1]
    if hasattr(last, "content"):
        return last.content if isinstance(last.content, str) else str(last.content)
    return str(last)
