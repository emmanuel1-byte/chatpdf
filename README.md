# ChatPDF

ChatPDF is an intelligent API that allows users to upload PDF documents and engage in interactive conversations with their content. Built with FastAPI, Langchain, LangGraph, MongoDB, Qdrant, and WebSockets, the system supports authenticated multi-user access and real-time querying through natural language. It leverages vector search and document embedding to provide accurate and contextual answers.

---

## Features

* **PDF Upload**: Upload and process PDF documents.
* **Chat with Documents**: Interact with the content of your PDF using natural language queries.
* **Authentication**: Secure user authentication with multi-user support.
* **Real-time Communication**: WebSocket-based real-time chat interface.
* **Chat History**: Chats are stored in the database and can be retrieved anytime.
* **Vector Deletion**: Users can delete PDF vectors and associated data from the vector store and database.
* **User Data Isolation**: User-based filtering to ensure privacy and data security.
* **LLM Orchestration**: Powered by Langchain and LangGraph for handling language model interactions.
* **Vector Search**: Utilizes Qdrant for high-performance similarity search.
* **Database Management**: MongoDB for storing user data, metadata, and chat history.
* **Dependency Management**: Managed with Poetry for easy setup and reproducibility.

---

## Tech Stack

* **Backend Framework**: FastAPI
* **LLM Integration**: Langchain, LangGraph
* **Database**: MongoDB
* **Vector Store**: Qdrant
* **Authentication**: Token-based (JWT)
* **Real-time Communication**: WebSocket
* **Dependency Management**: Poetry

---

## Getting Started

### Prerequisites

* Python 3.10+
* [Poetry](https://python-poetry.org/docs/#installation)
* Qdrant instance (local or cloud)
* MongoDB instance (local or cloud)

### Installation

1. **Clone the repository**

```bash
git clone https://github.com/emmanuel1-byte/chatpdf.git
cd chatpdf
```

2. **Install dependencies using Poetry**

```bash
poetry install
```

3. **Activate the virtual environment**

```bash
poetry shell
```

4. **Set up environment variables**

Create a `.env` file in the root directory with the following keys:

```env
DATABASE_URI=
GOOGLE_API_KEY=
QDRANT_API_KEY=
PLUNK_SECRET_KEY=
JWT_SECRET=
```

5. **Run the application**

```bash
fastapi run
```

---

## How It Works

1. The user registers and logs in to receive an authentication token.
2. The user uploads a PDF document.
3. The system parses the PDF, splits it into manageable chunks, generates embeddings, and stores them in Qdrant.
4. The user initiates a chat session via WebSocket.
5. Queries are processed using Langchain and LangGraph, retrieving relevant context from the vector store.
6. The system returns accurate and contextual responses in real-time.
7. All chat history is saved in MongoDB and can be retrieved for future sessions.
8. Users can delete PDFs, which removes both the stored vectors from Qdrant and associated chats and metadata from MongoDB.
