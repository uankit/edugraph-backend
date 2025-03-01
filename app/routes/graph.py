from fastapi import APIRouter, Query
from neo4j import GraphDatabase
from app.models.graph import GraphData, GraphDataSubtopics, GraphEdge, GraphNode
from app.services.graph import fetch_graph_data, fetch_subtopics


router = APIRouter(
    prefix="/api/graph",
    tags=["List graph"]
)

# Connect to Neo4j database
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "edugraph@123"

try:
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    with driver.session() as session:
        session.run("RETURN 1")
    print("Connected to Neo4j successfully.")
except Exception as e:
    print(f"Failed to connect to Neo4j: {e}")
    raise

@router.get("/", response_model=GraphData)
async def get_graph(mode: str = Query(default="interlinked")):
    return fetch_graph_data(mode)

@router.get("/subtopics", response_model=GraphDataSubtopics)
async def get_graph_subtopics(topic : str = Query(...)):
    print(f"Received topic: {topic}")
    return fetch_subtopics(topic)