from io import BytesIO
import json
import math
from fastapi import APIRouter, HTTPException, UploadFile, File
from app.services.chat import llm_map_topics
from app.services.graph import create_topic_and_subtopic_nodes, link_similar_topics
from app.services.nlp import process_pdf_text
from app.services.pdf_parser import extract_text_from_pdf, get_number_of_pages
from app.services.s3 import upload_file_to_s3
from fastapi import HTTPException

router = APIRouter(
    prefix="/api/upload",
    tags=["Upload"]
)

@router.post("/")
async def upload_file(file: UploadFile = File(...)):
    # Read file content asynchronously
    file_content = await file.read()
    file_obj = BytesIO(file_content)
    
    # Upload file to S3
    file_url = upload_file_to_s3(file_obj, file.filename)
    if not file_url:
        raise HTTPException(status_code=500, detail="Failed to upload file to S3")
    
    # Process PDF files only
    if file.content_type == "application/pdf":
        pages_text = extract_text_from_pdf(file_content)
        full_text = "\n".join(pages_text)
        data = process_pdf_text(full_text)
        response = llm_map_topics(
            {
                "keywords": json.dumps(data["keywords"]),
                "hierarchical_topics": data["hierarchical_topics"]
            }
        ) 
        try:
            create_topic_and_subtopic_nodes(response["topics"])
            link_similar_topics(response["topics"])
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Error creating topic nodes or linking similar topics: {e}"
            )
        
        return {
            "fileName": file.filename,
            "fileUrl": file_url,
            "topics": response["topics"]
        }
    else:
        raise HTTPException(status_code=400, detail="Unsupported file type")
