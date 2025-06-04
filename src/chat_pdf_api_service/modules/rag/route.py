from fastapi import APIRouter, Path, UploadFile, Depends, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse
from typing import Annotated
from ...dependencies import FileValidator, get_current_user, get_current_user_for_websocket
from ...helpers import load_document, split_doc, WebsocketConnectionManager
from ...services import vector_store, graph
from ...utils import logger, connect_to_database
from ..authentication.model import User
from fastapi.security import HTTPAuthorizationCredentials
from motor.motor_asyncio import AsyncIOMotorClient
from uuid import uuid4

rag = APIRouter(prefix="/api/v1/chat", tags=["Rag"])


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
    user_id = current_user.model_dump(mode="json").get("id")

    for doc in splits:
        doc.metadata.update({"user_id": user_id, "doc_id": doc_id})

    vector_store.add_documents(
        documents=splits,
    )

    return JSONResponse(
        content={
            "message": f"Successfully uploaded document {doc_id} for user {user_id}"
        },
        status_code=201,
    )



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
            data = await websocket.receive_text()
            for message_chunk, metadata in graph.stream(
                {
                    "question": data,
                    "doc_id": doc_id,
                    "user_id": current_user.model_dump(mode="json").get("id"),
                },
                stream_mode="messages",
            ):
                await manager.send_message(message_chunk.content, websocket)
    except WebSocketDisconnect as e:
        logger.error(e)
        manager.disconnect(websocket)
        raise
