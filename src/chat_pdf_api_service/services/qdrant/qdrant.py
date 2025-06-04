from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.models import PayloadSchemaType, VectorParams, Distance
import getpass
import os
from dotenv import load_dotenv


load_dotenv()

if not os.environ.get("GOOGLE_API_KEY"):
    os.environ["GOOGLE_API_KEY"] = getpass.getpass("Enter API key for Google Gemini: ")

from langchain_google_genai import GoogleGenerativeAIEmbeddings


"""
Initializes a Qdrant client and creates payload indices for a collection named 'chatpdf'.
Sets up a vector store using Google Generative AI embeddings for the specified collection.

- Initializes the `GoogleGenerativeAIEmbeddings` model for embedding generation.
- Configures a `QdrantClient` with a specified URL, API key, and timeout.
- Creates payload indices for 'metadata.user_id' and 'metadata.doc_id' fields in the 'chatpdf' collection.
- Establishes a `QdrantVectorStore` with the client, collection name, and embedding model.
"""

embedding_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
client = QdrantClient(
    url="https://311331ed-bc57-427a-bfcd-58d2f6082356.eu-west-1-0.aws.cloud.qdrant.io:6333",
    api_key=os.getenv("QDRANT_API_KEY"),
    timeout=30.0,
)

client.create_payload_index(
    collection_name="chatpdf",
    field_name="metadata.user_id",
    field_type=PayloadSchemaType.KEYWORD,
)

client.create_payload_index(
    collection_name="chatpdf",
    field_name="metadata.doc_id",
    field_type=PayloadSchemaType.KEYWORD,
)
vector_store = QdrantVectorStore(
    client=client,
    collection_name="chatpdf",
    embedding=embedding_model,
)
