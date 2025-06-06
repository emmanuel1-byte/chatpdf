from fastapi import APIRouter, Depends, HTTPException, Query, BackgroundTasks
from fastapi.responses import JSONResponse
from fastapi.security import HTTPAuthorizationCredentials
from .schema import (
    SignupSchema,
    LoginSchema,
    VerifyOTPSchema,
    ResendVerificationEmailSchema,
    ForgotPasswordSchema,
    ResetPasswordSchema,
)
from typing import Annotated
from ...utils import logger, connect_to_database
from ...helpers import generate_otp, generate_tokens
from motor.motor_asyncio import AsyncIOMotorClient
from .model import User
from ...dependencies import get_current_user
from ...services import send_verification_email, send_password_reset_email
from datetime import datetime, timezone
import bcrypt

authentication = APIRouter(prefix="/api/v1/auth", tags=["Authentication"])


@authentication.post("/signup")
async def signup(
    init_database: Annotated[AsyncIOMotorClient, Depends(connect_to_database)],
    validated_request: SignupSchema,
    background_tasks: BackgroundTasks,
):
    existing_user = await User.find_one(User.email == validated_request.email)
    if existing_user:
        raise HTTPException(
            status_code=409, detail={"message": "Account already exist"}
        )

    otp_data = generate_otp()
    new_user = User(**validated_request.model_dump(mode="json"), OTP_data=otp_data)
    background_tasks.add_task(
        send_verification_email,
        new_user.email,
        validated_request.fullname.split(" ")[0],
        otp_data.get("password"),
    )

    await new_user.create()

    return JSONResponse(content={"message": "Account created"}, status_code=201)


@authentication.post("/verify-OTP")
async def verify_OTP(
    init_database: Annotated[AsyncIOMotorClient, Depends(connect_to_database)],
    validated_request: VerifyOTPSchema,
):
    user = await User.find_one(User.OTP_data.password == validated_request.password)
    if user is None:
        raise HTTPException(status_code=404, detail={"message": "OTP does not exist"})

    if datetime.now(timezone.utc) > user.OTP_data.expiry_at.replace(
        tzinfo=timezone.utc
    ):
        user.OTP_data = None
        await user.save()
        raise HTTPException(status_code=400, detail={"message": "OTP has expired"})

    user.OTP_data = None
    user.verified = True
    await user.save()

    return JSONResponse(content={"message": "OTP verified"}, status_code=200)


@authentication.post("/resend-verification-email")
async def resend_verification_email(
    init_database: Annotated[AsyncIOMotorClient, Depends(connect_to_database)],
    validated_request: ResendVerificationEmailSchema,
    background_tasks: BackgroundTasks,
):
    user = await User.find_one(User.email == validated_request.email)
    if user is None:
        raise HTTPException(
            status_code=409, detail={"message": "Account already exist"}
        )

    if user.verified:
        raise HTTPException(
            status_code=409, detail={"message": "Account already verified"}
        )

    otp_data = generate_otp()
    background_tasks.add_task(
        send_verification_email,
        user.email,
        validated_request.fullname.split(" ")[0],
        otp_data.get("password"),
    )

    return JSONResponse(content={"message": "Email sent"}, status_code=200)


@authentication.post("/login")
async def login(
    init_database: Annotated[AsyncIOMotorClient, Depends(connect_to_database)],
    validated_request: LoginSchema,
):
    user = await User.find_one(User.email == validated_request.email)
    if user is None:
        raise HTTPException(
            status_code=404, detail={"message": "Account does not exist"}
        )

    compare_password = bcrypt.checkpw(
        validated_request.password.encode(),
        user.password.encode(),
    )
    if not compare_password:
        raise HTTPException(status_code=401, detail={"message": "Invalid credentials"})

    access_token, refresh_token = generate_tokens(str(user.id))

    return JSONResponse(
        content={
            "data": {
                "token": {"access_token": access_token, "refresh_token": refresh_token}
            }
        },
        status_code=200,
    )


@authentication.post("/forgot-password")
async def forgot_password(
    init_database: Annotated[AsyncIOMotorClient, Depends(connect_to_database)],
    validated_request: ForgotPasswordSchema,
    background_tasks: BackgroundTasks,
):
    user = await User.find_one(User.email == validated_request.email)
    if user is None:
        raise HTTPException(
            status_code=404, detail={"message": "Account does not exist"}
        )

    otp_data = generate_otp()
    user.OTP_data = otp_data
    await user.save()

    background_tasks.add_task(
        send_password_reset_email,
        validated_request.email,
        user.fullname.split(" ")[0],
        otp_data.get("password"),
    )

    return JSONResponse(content={"message": "Email sent"}, status_code=200)


@authentication.patch("/reset-password")
async def reset_password(
    init_database: Annotated[AsyncIOMotorClient, Depends(connect_to_database)],
    validated_request: ResetPasswordSchema,
):
    user = await User.find_one(User.OTP_data.password == validated_request.otp)
    if user is None:
        raise HTTPException(status_code=404, detail={"message": "OTP does not exist"})

    if datetime.now(timezone.utc) > user.OTP_data.expiry_at.replace(
        tzinfo=timezone.utc
    ):
        user.OTP_data = None
        await user.save()
        raise HTTPException(status_code=400, detail={"message": "OTP has expired"})

    user.password = bcrypt.hashpw(
        validated_request.password.encode(), bcrypt.gensalt()
    ).decode()
    user.OTP_data = None
    await user.save()

    return JSONResponse(
        content={"message": "Password reset successfull"}, status_code=200
    )


@authentication.post("/refresh-token")
def resfresh_tokens(
    init_database: Annotated[AsyncIOMotorClient, Depends(connect_to_database)],
    current_user: Annotated[HTTPAuthorizationCredentials, Depends(get_current_user)],
):

    access_token, refresh_token = generate_tokens(str(current_user.id))

    return JSONResponse(
        content={
            "data": {
                "token": {"access_token": access_token, "refresh_token": refresh_token}
            }
        },
        status_code=200,
    )
