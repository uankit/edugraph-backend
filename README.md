
# **EduGraph Backend - AI-Powered Topic Extraction & Interlinking**

EduGraph is an **AI-driven topic modeling and graph-based knowledge interlinking system** that processes **PDFs** to extract topics, subtopics, and interlinks them for a structured learning experience.

## **🚀 Setup Instructions**

### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/your-repo/edugraph.git
cd edugraph
```

### **2️⃣ Install Dependencies**
EduGraph uses **Poetry** for dependency management. Install all dependencies using:
```bash
poetry install
```

### **3️⃣ Set Up Environment Variables**
Create a **`.env`** file in the project root and add the following configurations:

```env
# AWS Configuration (For File Uploads)
AWS_ACCESS_KEY_ID=YOUR_AWS_ACCESS_KEY
AWS_SECRET_ACCESS_KEY=YOUR_AWS_SECRET_KEY
AWS_REGION=eu-north-1
AWS_BUCKET_NAME=edugraphbucket

# Neo4j Configuration (Graph Database)
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your-neo4j-password

# OpenAI API Key (For Topic Refinement)
OPENAI_API_KEY=your-openai-api-key
```

### **4️⃣ Update Service Configurations**
- **Graph Service (`graph.py`)**: Ensure **Neo4j credentials** match your `.env` file.
- **Chat Service (`chat.py`)**: Uses **OpenAI API Key** for refining topics.

---
## **📌 API Endpoints**
EduGraph provides the following endpoints:

| **Endpoint**         | **Method** | **Description** |
|----------------------|-----------|------------------------------------------------|
| `/api/upload/`      | `POST`    | Uploads a **PDF to S3**, processes it, and returns extracted topics. |
| `/api/graph/`       | `GET`     | Retrieves the **graph** with topics and their relationships from Neo4j. |
| `/api/graph/subtopics` | `GET` | Fetches **subtopics** related to a given topic node. |

---
## **💡 Motivation**
EduGraph was built as a **learning project on Topic Modeling & AI** to develop an end-to-end **PDF processing and knowledge interlinking system**.

**Tech Stack:**
- **Backend:** FastAPI, Neo4j, OpenAI API, AWS S3
- **ML Models:** BERTopic, Sentence Transformers, HDBSCAN, UMAP

## **🚀 Run the Backend**
To start the **FastAPI** backend, run:
```bash
poetry run uvicorn app.main:app --reload
```
The API will be available at **`http://localhost:8000/docs`** (Swagger UI).

---
## **👨‍💻 Hiring-Friendly Features & Career Impact**
EduGraph is designed with **scalability and AI-driven automation** in mind. Key features include:
- **Production-Ready API Design** 🚀
- **Integration with AI Models** (Topic Refinement, NLP, Knowledge Graphs) 🤖
- **Graph-Based Knowledge Mapping** 🔍
- **Optimized for Research & Learning** 📚

### **Future Enhancements:**
✅ Add support for **scanned PDFs using OCR** 📄
✅ Enhance **graph-based filtering 🎨
✅ Improve **topic refinement** with hierarchical structuring 🏗️

For **contributions or hiring inquiries**, feel free to **open a PR or reach out**! 🚀





<img width="1502" alt="Screenshot 2025-03-01 at 10 15 39 PM" src="https://github.com/user-attachments/assets/2214a5e4-e752-4ccb-8d11-b971b29ca73a" />
