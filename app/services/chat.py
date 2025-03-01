import itertools
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama
from langchain_openai import ChatOpenAI
from app.models.topics import  MapTopics



def llm_map_topics(data: str) -> ChatOllama:
    OPENAI_API_KEY=""
    map_topics_prompt = ChatPromptTemplate.from_template(
        """
    You are an advanced AI specializing in hierarchical topic extraction and interlinking. Your goal is to analyze the provided hierarchical topic data and generate human-readable topics, descriptions, categories, and subtopics.

    ## 🎯 **Your Task**
    1. **Understand the Data**: Analyze the hierarchical structure of the input data. Identify parent-child relationships and the keywords associated with each topic.
    2. **Extract Topics**: Identify the main topics from the hierarchical data. Each topic should be unique and meaningful.
    3. **Generate Descriptions**: Write concise, 2-3 sentence descriptions for each topic, explaining its purpose and relevance.
    4. **Assign Categories**: Assign each topic to a broader category (e.g., Economics, History, Technology, Politics, Geography, etc.*).
    5. **Extract Subtopics**: Identify subtopics that contribute to the main topic by analyzing the keywords and hierarchy table.

    ## 🏗 **Rules for Extraction**
    - **Topics**: Ensure each topic is unique and meaningful.
    - **Descriptions**: Avoid vague or generic explanations. Include key insights and context.
    - **Categories**: Choose the most relevant category for each topic.
    - **Subtopics**: Ensure subtopics are specific and directly related to their parent topic.

    ## **📌 Input Data**
    The hierarchical topic data is provided below:
    - **Keywords**: {keywords}
    - **Hierarchy Table**: {hierarchy_table}

    Output your result as a JSON array, where each element is an object with the keys "topic", "description", "category", and "subtopics".
    """
        )
    prompt = map_topics_prompt.invoke({"keywords": data["keywords"], "hierarchy_table": data["hierarchical_topics"]})
    llm = ChatOpenAI(temperature=0, model="gpt-4o-mini", openai_api_key=OPENAI_API_KEY, disable_streaming=True).with_structured_output(MapTopics)
    response = llm.invoke(prompt)
    print(response)
    return response.model_dump()