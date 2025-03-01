import re
from langchain_text_splitters import RecursiveCharacterTextSplitter, SentenceTransformersTokenTextSplitter
import spacy
from typing import List
from bertopic import BERTopic
from bertopic.representation import PartOfSpeech, MaximalMarginalRelevance, KeyBERTInspired
from sklearn.feature_extraction.text import CountVectorizer
from umap import UMAP
from hdbscan import HDBSCAN
from scipy.cluster import hierarchy as sch



nlp = spacy.load("en_core_web_trf")
nlp.max_length = 1500000


from sklearn.feature_extraction.text import TfidfVectorizer

# Preprocess text
def preprocess_text(text: str) -> str:
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'-\s+', '', text)
    return text.lower().strip()

# Split text into chunks
def split_pdf_text(pdf_data: str) -> List[str]:
    pdf_data = preprocess_text(pdf_data)
    if len(pdf_data) < 5000:  # Small notes or short PDFs
        return RecursiveCharacterTextSplitter(
            chunk_size=200, chunk_overlap=50  # Smaller chunks for dense text
        ).split_text(pdf_data)
    else:  # Large books or lengthy PDFs
        return SentenceTransformersTokenTextSplitter(
            model_name="all-mpnet-base-v2",
            chunk_size=400,  # Slightly larger chunks for general text
            chunk_overlap=100
        ).split_text(pdf_data)

# Create hierarchical topic model
def create_hierarchical_topic_model():
    umap_model = UMAP(
        n_neighbors=10,  
        n_components=5, 
        min_dist=0.08,
        metric="euclidean",
        random_state=42
    )
    
    vectorizer_model = TfidfVectorizer(
        ngram_range=(1,2),
        stop_words=None,
        token_pattern=r'\b[a-zA-Z0-9]{3,}\b',
        max_df=0.85,
        min_df=3
    )

    # Fine-tuned HDBSCAN clustering
    hdbscan_model = HDBSCAN(
        min_cluster_size=6,
        min_samples=4,
        metric='euclidean',
        cluster_selection_method='eom',
        prediction_data=True
    )

    mmr_model = MaximalMarginalRelevance(diversity=0.2, top_n_words=5)
    keybert_model = KeyBERTInspired()

    representation_models = [mmr_model, keybert_model]

    topic_model = BERTopic(
        umap_model=umap_model,
        vectorizer_model=vectorizer_model,
        hdbscan_model=hdbscan_model,
        representation_model=representation_models,
        calculate_probabilities=False,
        min_topic_size=10,
    )
    return topic_model

# Extract topics and keywords
def extract_topics_and_keywords(documents, topic_model):
    topics, _ = topic_model.fit_transform(documents)

    topic_keywords = topic_model.get_topic_info()

    keywords_per_topic = {
        row["Topic"]: row["Representation"][:5]
        for _, row in topic_keywords.iterrows() if row["Topic"] != -1
    }

    return keywords_per_topic

# Extract hierarchical topics
def extract_hierarchical_topics(documents, topic_model):
    """
    Fit BERTopic and extract hierarchical topics using optimal clustering.
    """
    topics, _ = topic_model.fit_transform(documents)
    linkage_function = lambda x: sch.linkage(x, method='ward')
    topics_df = topic_model.hierarchical_topics(documents, linkage_function=linkage_function)
    return topics_df


def process_pdf_text(pdf_data):
    documents = split_pdf_text(pdf_data)
    print(len(documents))
    topic_model = create_hierarchical_topic_model()
    keywords_per_topic = extract_topics_and_keywords(documents, topic_model)
    hierarchical_topics = extract_hierarchical_topics(documents, topic_model)
    print(keywords_per_topic)
    print(hierarchical_topics)
    return {
        "keywords": keywords_per_topic,
        "hierarchical_topics": hierarchical_topics
    }