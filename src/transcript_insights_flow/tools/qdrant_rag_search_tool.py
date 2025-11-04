import os
import uuid
import pdfplumber
from openai import OpenAI
from dotenv import load_dotenv
from crewai_tools import QdrantVectorSearchTool 
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, Distance, VectorParams

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Extract text from PDF
def extract_text_from_pdf(pdf_path):
    text = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text.append(page_text.strip())
    return text

# Generate OpenAI embeddings
def get_openai_embedding(text):
    response = client.embeddings.create(
        input=text,
        model="text-embedding-3-large"
    )
    return response.data[0].embedding

# Store text and embeddings in Qdrant
def load_pdf_to_qdrant(pdf_path, qdrant, collection_name):
    # Extract text from PDF
    text_chunks = extract_text_from_pdf(pdf_path)

    # Create Qdrant collection
    if qdrant.collection_exists(collection_name):
        qdrant.delete_collection(collection_name)
    qdrant.create_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(size=3072, distance=Distance.COSINE)
    )

    # Store embeddings
    points = []
    for chunk in text_chunks:
        embedding = get_openai_embedding(chunk)
        points.append(PointStruct(
            id=str(uuid.uuid4()),
            vector=embedding,
            payload={"text": chunk}
        ))
    qdrant.upsert(collection_name=collection_name, points=points)

# Initialize Qdrant client and load data
qdrant = QdrantClient(
    url=os.getenv("QDRANT_URL"),
    api_key=os.getenv("QDRANT_API_KEY")
)
collection_name = "abi-training-day-2-pdf-vectors"
pdf_path = "knowledge/aula-02-principais-eticos-PV4OBc7J.pdf"
load_pdf_to_qdrant(pdf_path, qdrant, collection_name)

# Initialize Qdrant search tool

qdrant_tool = QdrantVectorSearchTool(
        client=qdrant, 
        collection_name=collection_name,
        qdrant_url=os.getenv("QDRANT_URL"),
        qdrant_api_key=os.getenv("QDRANT_API_KEY"),
        limit=3,
        score_threshold=0.35,
)

if __name__ == "__main__":
    # Example usage of the Qdrant search tool
    query = "How to set up CrewAI?"
    results = qdrant_tool._run(query)
    for idx, result in enumerate(results):
        print(f"Result {idx + 1}: {result}\n")
