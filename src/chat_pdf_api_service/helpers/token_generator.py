import jwt
import os
import secrets
import string
import random
from dotenv import load_dotenv
import datetime
from datetime import timezone

load_dotenv()


def generate_tokens(user_id: str):
    access_token = jwt.encode(
        {
            "sub": user_id,
            "exp": datetime.datetime.now(tz=timezone.utc) + datetime.timedelta(days=30),
        },
        os.getenv("JWT_SECRET"),
        algorithm="HS256",
    )
    refresh_token = jwt.encode(
        {
            "sub": user_id,
            "exp": datetime.datetime.now(tz=timezone.utc) + datetime.timedelta(days=60),
        },
        os.getenv("JWT_SECRET"),
        algorithm="HS256",
    )

    return (access_token, refresh_token)


def create_shareable_token(length=6):
    characters = string.ascii_letters + string.digits
    return "".join(secrets.choice(characters) for _ in range(length))
