import json
from sentence_transformers import SentenceTransformer, util
from neo4j import GraphDatabase

from app.models.graph import GraphData, GraphEdge, GraphNode

# Load Sentence Transformer model
embedding_model = SentenceTransformer("all-mpnet-base-v2")

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


def create_topic_and_subtopic_nodes(topics):
    """
    Create nodes for both Topics and their Subtopics in Neo4j.
    'topics' is a list of dicts with keys: 'topic', 'description', 'category', 'subtopics'.
    """
    with driver.session() as session:
        for topic in topics:
            print(topic.keys())
            title = topic.get("topic")
            description = topic.get("description")
            category = topic.get("category")
            subtopics = topic.get("subtopics", [])

            # Create Parent Topic Node
            session.run(
                """
                MERGE (t:Topic {title: $title})
                SET t.description = $description,
                    t.category = $category,
                    t.type = $type
                """,
                title=title,
                description=description,
                category=category,
                type="topic"
            )

            # Create Subtopic Nodes and Link to Parent
            for subtopic in subtopics:
                session.run(
                    """
                    MERGE (st:Subtopic {title: $subtopic})
                    SET st.type = $type
                    WITH st
                    MATCH (t:Topic {title: $parent_title})
                    MERGE (t)-[:HAS_SUBTOPIC]->(st)
                    """,
                    subtopic=subtopic,
                    parent_title=title,
                    type="subtopic"
                )
    print("New topic and subtopic nodes created.")


def link_similar_topics(new_topics, threshold=0.7):
    """
    Interlink similar topics across different PDFs using semantic similarity.
    """
    # Compute embeddings for new topics
    new_embeddings = {
        topic.get("topic"): embedding_model.encode(
            f"{topic.get('topic')} {topic.get('description')}", convert_to_tensor=True
        )
        for topic in new_topics
    }

    # Retrieve all existing topics from Neo4j
    with driver.session() as session:
        result = session.run("MATCH (t:Topic) RETURN t.title AS title, t.description AS description")
        existing_topics = [{"title": record.get("title"), "description": record.get("description")} for record in result]

    # Compute embeddings for existing topics
    existing_embeddings = {
        topic.get("title"): embedding_model.encode(f"{topic.get('title')} {topic.get('description')}", convert_to_tensor=True)
        for topic in existing_topics
    }

    # Link new topics with existing topics if similarity exceeds threshold
    with driver.session() as session:
        for new_topic in new_topics:
            new_title = new_topic.get("topic")
            new_emb = new_embeddings[new_title]
            for existing_topic in existing_topics:
                existing_title = existing_topic.get("title")
                # Skip linking a topic with itself if it's already in the new list.
                if new_title == existing_title:
                    continue
                similarity = util.cos_sim(new_emb, existing_embeddings[existing_title]).item()
                if similarity >= threshold:
                    session.run(
                        """
                        MATCH (t1:Topic {title: $new_title}), (t2:Topic {title: $existing_title})
                        MERGE (t1)-[r:SIMILAR_TO]-(t2)
                        SET r.similarity = $similarity
                        """,
                        new_title=new_title,
                        existing_title=existing_title,
                        similarity=similarity,
                    )
                    print(f"Linked '{new_title}' with '{existing_title}' (Similarity: {similarity:.2f})")
    print("Topic interlinking complete.")


def fetch_graph_data(mode):
    """
    Fetch graph data including Topics, Subtopics, and their relationships.
    """
    with driver.session() as session:
        # Retrieve all Topic nodes
        nodes_result = session.run(
            "MATCH (t:Topic) RETURN t.title AS title, t.description AS description, t.category AS category, t.type AS type"
        )
        nodes = {
            record["title"]: {
                "title": record["title"],
                "description": record["description"],
                "category": record["category"],
                "type": record["type"]
            }
            for record in nodes_result
        }

        # Retrieve all SIMILAR_TO relationships (undirected)
        edges_result = session.run(
            "MATCH (t1:Topic)-[r:SIMILAR_TO]-(t2:Topic) RETURN t1.title AS source, t2.title AS target, r.similarity AS similarity"
        )
        edges = []
        interlinked_topics = set()
        seen = set()
        for record in edges_result:
            source = record["source"]
            target = record["target"]
            key = tuple(sorted([source, target]))
            if key in seen:
                continue
            seen.add(key)
            edges.append({
                "source": source,
                "target": target,
                "similarity": record["similarity"]
            })
            # Mark topics as interlinked
            interlinked_topics.add(source)
            interlinked_topics.add(target)

        # Retrieve all Subtopic nodes and their relationships
        subtopic_edges_result = session.run(
            "MATCH (t:Topic)-[:HAS_SUBTOPIC]->(st:Subtopic) RETURN t.title AS topic, st.title AS subtopic"
        )
        for record in subtopic_edges_result:
            edges.append({
                "source": record["topic"],
                "target": record["subtopic"],
                "similarity": None
            })

        # Filter topics based on mode
        if mode == "interlinked":
            nodes = {key: val for key, val in nodes.items() if key in interlinked_topics}
            edges = [edge for edge in edges if edge["source"] in interlinked_topics and edge["target"] in interlinked_topics]

    
    return {"nodes": list(nodes.values()), "edges": edges}


def fetch_subtopics(topic):
    print(topic)
    with driver.session() as session:
        result = session.run("MATCH (t:Topic {title: $title})-[:HAS_SUBTOPIC]->(st:Subtopic) RETURN st.title AS subtopic", title=topic)
        print(result)
        return {"topic": topic, "subtopics": [record['subtopic'] for record in result]}
