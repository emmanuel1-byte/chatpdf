import getpass
import os
from dotenv import load_dotenv
from langchain_core.documents import Document
from typing_extensions import List, TypedDict
from langchain import hub
from langgraph.graph import START, StateGraph
from ...qdrant import vector_store
from qdrant_client.models import Filter, FieldCondition, MatchValue

load_dotenv()

if not os.environ.get("GOOGLE_API_KEY"):
    os.environ["GOOGLE_API_KEY"] = getpass.getpass("Enter API key for Google Gemini: ")

from langchain.chat_models import init_chat_model



"""
Initializes a chat model and defines functions for document retrieval and response generation
using a state graph. The `retrieve` function performs a similarity search on a vector store
to find relevant documents based on a user's question and metadata filters. The `generate`
function constructs a response by invoking a language model with the retrieved documents'
content and the user's question. The state graph orchestrates the sequence of these operations.
"""

llm = init_chat_model("gemini-2.0-flash", model_provider="google_genai")
prompt = hub.pull("rlm/rag-prompt")


class State(TypedDict):
    doc_id: str
    user_id: str
    question: str
    context: List[Document]
    answer: str


def retrieve(state: State):
    retrieved_docs = vector_store.similarity_search(
        state["question"],
        k=5,
        filter=Filter(
            must=[
                FieldCondition(
                    key="metadata.doc_id", match=MatchValue(value=state["doc_id"])
                ),
                FieldCondition(
                    key="metadata.user_id", match=MatchValue(value=state["user_id"])
                ),
            ]
        ),
    )
    return {"context": retrieved_docs}


def generate(state: State):
    docs_content = "\n\n".join(doc.page_content for doc in state["context"])
    messages = prompt.invoke({"question": state["question"], "context": docs_content})
    response = llm.invoke(messages)
    return {"answer": response.content}


graph_builder = StateGraph(State).add_sequence([retrieve, generate])
graph_builder.add_edge(START, "retrieve")
graph = graph_builder.compile()
