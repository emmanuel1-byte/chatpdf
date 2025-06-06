# ChatPDF

ChatPDF is an intelligent API that allows users to upload PDF documents and engage in interactive conversations with their contents. Built with FastAPI, Langchain, LangGraph, MongoDB, Qdrant, and WebSockets, the system supports authenticated multi-user access and real-time querying through natural language. It leverages vector search and document embedding to provide accurate and contextual answers.

---

## Features

* **PDF Upload**: Upload and process PDF documents.
* **Chat with Documents**: Interact with the content of your PDF using natural language.
* **Authentication**: Secure user management and multi-user support.
* **Real-time Communication**: WebSocket-based real-time chat interface.
* **Filtering**: User-based filtering to ensure data isolation.
* **Langchain & LangGraph**: For orchestrating LLM-driven interactions.
* **Qdrant**: High-performance vector database for similarity search.
* **MongoDB**: Stores metadata and user information.
* **Poetry**: Used for dependency management and packaging.

---

## Tech Stack

* **Backend Framework**: FastAPI
* **LLM Integration**: Langchain, LangGraph
* **Database**: MongoDB
* **Vector Store**: Qdrant
* **Authentication**: Token-based authentication (e.g., JWT)
* **Real-time Layer**: WebSocket
* **Dependency Management**: Poetry

---

## Getting Started

### Prerequisites

* Python 3.10+
* [Poetry](https://python-poetry.org/docs/#installation)
* Qdrant
* MongoDB instance (local or cloud)

### Installation

1. **Clone the repository**:

```bash
git clone https://github.com/emmanuel1-byte/chatpdf.git
cd chatpdf
```

2. **Install dependencies using Poetry**:

```bash
poetry install
```

3. **Activate the virtual environment**:

```bash
poetry env activate
```

4. **Set up environment variables**:

Create a `.env` file in the root directory with the following variables:

```env
DATABASE_URI=
GOOGLE_API_KEY=
QDRANT_API_KEY=
PLUNK_SECRET_KEY=
JWT_SECRET=
```

5. **Run the application**:

```bash
fastapi run
```
---

## How It Works

1. User registers and logs in to receive an auth token.
2. User uploads a PDF.
3. The system parses and chunks the PDF, embeds the text, and stores it in Qdrant.
4. The user initiates a chat session via WebSocket.
5. Langchain orchestrates queries against the vector store.
6. Contextual responses are returned in real-time.


