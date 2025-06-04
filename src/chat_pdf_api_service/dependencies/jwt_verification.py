import jwt
from jwt import InvalidTokenError, ExpiredSignatureError
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from typing import Annotated
from fastapi import (
    Depends,
    HTTPException,
    Query,
    WebSocketException,
)
from ..utils import connect_to_database, logger
import os
from dotenv import load_dotenv

load_dotenv()
from motor.motor_asyncio import AsyncIOMotorClient


"""
Retrieve the current user based on the provided JWT token.

This asynchronous function decodes the JWT token to extract the user
identifier and fetches the corresponding user from the database. It
raises an HTTPException if the token is missing, invalid, expired, or
if no user is found.

Parameters:
    token (Annotated[HTTPAuthorizationCredentials]): The JWT token
        extracted from the request header.
    init_database (Annotated[AsyncIOMotorClient]): The initialized
        database client.

Returns:
    User: The user object associated with the token.

Raises:
    HTTPException: If the token is missing, invalid, expired, or if
        the user does not exist.
"""

security = HTTPBearer()


async def get_current_user(
    token: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    init_database: Annotated[AsyncIOMotorClient, Depends(connect_to_database)],
):
    from ..modules import User

    if token.credentials is None:
        raise HTTPException(
            status_code=400,
            detail={"message": "Acess token required!"},
        )

    try:
        payload = jwt.decode(
            token.credentials, os.getenv("JWT_SECRET"), algorithms=["HS256"]
        )
        user = await User.get(payload.get("sub"))
        if user is None:
            raise HTTPException(
                detail={
                    "message": "Account associated with this token does not exist",
                },
                status_code=404,
            )

        return user
    except InvalidTokenError as e:
        logger.error(e)
        raise HTTPException(detail={"message": "Invalid access token"}, status_code=400)
    except ExpiredSignatureError as e:
        logger.error(e)
        raise HTTPException(detail={"message": "Token has expired!"}, status_code=401)




"""
Retrieve the current user for a WebSocket connection using a JWT token.

This asynchronous function verifies the provided JWT token from the
WebSocket query parameters, decodes it to extract the user identifier,
and retrieves the corresponding user from the database. It raises a
WebSocketException if the token is missing, invalid, expired, or if
the user does not exist.

Parameters:
    access_token (Annotated[str, Query]): The JWT token extracted from
        the WebSocket query parameters.
    init_database (Annotated[AsyncIOMotorClient, Depends]): The initialized
        database client.

Returns:
    User: The user object associated with the token.

Raises:
    WebSocketException: If the token is missing, invalid, expired, or if
        the user does not exist.
"""
async def get_current_user_for_websocket(
    access_token: Annotated[str, Query()],
    init_database: Annotated[AsyncIOMotorClient, Depends(connect_to_database)],
):
    from ..modules import User

    if access_token is None or not access_token.startswith("Bearer"):
        raise WebSocketException(code=400, reason="Access token required!")

    try:
        payload = jwt.decode(
            access_token.split(" ")[1], os.getenv("JWT_SECRET"), algorithms=["HS256"]
        )
        user = await User.get(payload.get("sub"))
        if user is None:
            raise WebSocketException(
                code=404, reason="Account associated with this token does not exist"
            )

        return user

    except InvalidTokenError as e:
        logger.error(e)
        raise WebSocketException(code=404, reason="Invalid access token")
    except ExpiredSignatureError as e:
        logger.error(e)
        raise WebSocketException(code=401, reason="Token has expired!")
