from fastapi import (
    APIRouter,
    Path,
    UploadFile,
    Depends,
    WebSocket,
    WebSocketDisconnect,
    HTTPException,
)
from fastapi.responses import JSONResponse
from typing import Annotated
from qdrant_client.models import Filter, FieldCondition, MatchValue
from qdrant_client.http import models
from ...dependencies import (
    FileValidator,
    get_current_user,
    get_current_user_for_websocket,
)
from ...helpers import load_document, split_doc, WebsocketConnectionManager
from ...services import vector_store, graph, client
from ...utils import logger, connect_to_database
from ..authentication.model import User
from .model import Chat
from fastapi.security import HTTPAuthorizationCredentials
from motor.motor_asyncio import AsyncIOMotorClient
from uuid import uuid4
import json

rag = APIRouter(prefix="/api/v1/chats", tags=["Rag"])


@rag.post("/upload")
def upload_pdf(
    init_database: Annotated[AsyncIOMotorClient, Depends(connect_to_database)],
    current_user: Annotated[HTTPAuthorizationCredentials, Depends(get_current_user)],
    file: UploadFile,
    validate_file: Annotated[bool, Depends(FileValidator)],
):
    docs = load_document(file)
    splits = split_doc(docs)

    doc_id = str(uuid4())
    user_id = str(current_user.id)

    for doc in splits:
        doc.metadata.update({"user_id": user_id, "doc_id": doc_id})

    vector_store.add_documents(
        documents=splits,
    )

    return JSONResponse(
        content={"data": {"doc_id": doc_id}},
        status_code=201,
    )


"""
WebSocket endpoint for handling real-time chat interactions.

This endpoint manages WebSocket connections for a specific document ID,
allowing users to send and receive chat messages in real-time. It retrieves
existing chats for the document, sends them to the client, and processes
incoming messages to generate AI responses. The responses are streamed back
to the client and stored in the database.

Parameters:
    doc_id (str): The document ID for which the chat is associated.
    current_user (User): The current authenticated user obtained from the
        WebSocket connection.
    websocket (WebSocket): The WebSocket connection instance.

Raises:
    WebSocketDisconnect: If the WebSocket connection is interrupted.
"""

manager = WebsocketConnectionManager()


@rag.websocket("/ws/{doc_id}")
async def websocket_endpoint(
    doc_id: Annotated[str, Path()],
    current_user: Annotated[User, Depends(get_current_user_for_websocket)],
    websocket: WebSocket,
):
    await manager.connect(websocket)
    try:
        while True:
            chats = await Chat.find(Chat.doc_id == doc_id).to_list()
            await manager.send_message(
                json.dumps([chat.model_dump(mode="json") for chat in chats]),
                websocket,
            )

            data = await websocket.receive_text()

            streamed_ai_responses = []
            for message_chunk, metadata in graph.stream(
                {
                    "question": data,
                    "doc_id": doc_id,
                    "user_id": str(current_user.id),
                },
                stream_mode="messages",
            ):
                streamed_ai_responses.append(message_chunk.content)
                await manager.send_message(message_chunk.content, websocket)

            new_chat = Chat(
                prompt=data,
                ai_response=" ".join(streamed_ai_responses),
                recipient=current_user.id,
                doc_id=doc_id,
            )

            await new_chat.insert()
    except WebSocketDisconnect as e:
        logger.error(e)
        manager.disconnect(websocket)
        raise





@rag.delete("/{doc_id}")
async def delete_chat_and_pdf(
    init_database: Annotated[AsyncIOMotorClient, Depends(connect_to_database)],
    current_user: Annotated[HTTPAuthorizationCredentials, Depends(get_current_user)],
    doc_id: Annotated[str, Path()],
):
    chat = await Chat.find(Chat.doc_id == doc_id).delete()
    if chat.deleted_count == 0:
        raise HTTPException(
            status_code=404, detail={"message": "Document does not exist"}
        )

    client.delete(
        collection_name="chatpdf",
        points_selector=models.FilterSelector(
            filter=models.Filter(
                must=[
                    models.FieldCondition(
                        key="metadata.doc_id", match=models.MatchValue(value=doc_id)
                    )
                ]
            )
        ),
    )

    return JSONResponse(
        content={"message": "Chat and related vectors deleted"}, status_code=200
    )
