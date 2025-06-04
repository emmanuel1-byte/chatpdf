from fastapi import WebSocket


"""
Manages WebSocket connections, allowing for connection, disconnection, 
and message sending to active WebSocket clients.

Attributes:
    active_connections (list[WebSocket]): A list of currently active WebSocket connections.

Methods:
    connect(websocket: WebSocket):
        Accepts a new WebSocket connection and adds it to the active connections list.
    disconnect(websocket: WebSocket):
        Removes a WebSocket connection from the active connections list.
    send_message(message: str, websocket: WebSocket):
        Sends a text message to a specified WebSocket connection.
"""
class WebsocketConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)
        
