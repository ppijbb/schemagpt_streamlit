import os
from langchain_community.tools import DuckDuckGoSearchRun, WikipediaQueryRun, PubmedQueryRun
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper, WikipediaAPIWrapper, PubMedAPIWrapper
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage, AIMessage

# 도구 정의
tools = [
    DuckDuckGoSearchRun(api_wrapper=DuckDuckGoSearchAPIWrapper(max_results=10, region="en-en")),
    WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper()),
    PubmedQueryRun(api_wrapper=PubMedAPIWrapper())
]

# 모델 설정
model = ChatOpenAI(temperature=0, streaming=True)

# LangGraph prebuilt ReAct agent (replaces deprecated ToolExecutor + StateGraph pattern)
app = create_react_agent(model, tools)

# Neo4j: optional; enable with USE_NEO4J=1 and install langchain-neo4j (e.g. uv sync --extra neo4j)
if os.environ.get("USE_NEO4J"):
    os.environ.setdefault("NEO4J_URI", "bolt://localhost:7687")
    os.environ.setdefault("NEO4J_USERNAME", "neo4j")
    os.environ.setdefault("NEO4J_PASSWORD", "password")
    try:
        from langchain_neo4j import Neo4jGraph
        graph = Neo4jGraph()
        movies_query = """
        LOAD CSV WITH HEADERS FROM 
        'https://raw.githubusercontent.com/tomasonjo/blog-datasets/main/movies/movies_small.csv'
        AS row
        MERGE (m:Movie {id:row.movieId})
        SET m.released = date(row.released),
            m.title = row.title,
            m.imdbRating = toFloat(row.imdbRating)
        FOREACH (director in split(row.director, '|') | 
            MERGE (p:Person {name:trim(director)})
            MERGE (p)-[:DIRECTED]->(m))
        FOREACH (actor in split(row.actors, '|') | 
            MERGE (p:Person {name:trim(actor)})
            MERGE (p)-[:ACTED_IN]->(m))
        FOREACH (genre in split(row.genres, '|') | 
            MERGE (g:Genre {name:trim(genre)})
            MERGE (m)-[:IN_GENRE]->(g))
        """
        graph.query(movies_query)
    except ImportError:
        pass