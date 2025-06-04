from pydantic import BaseModel, EmailStr, Field


class SignupSchema(BaseModel):
    fullname: str
    email: EmailStr
    password: str = Field(min_length=9, max_length=256)

class ResendVerificationEmailSchema(BaseModel):
    email: EmailStr

class VerifyOTPSchema(BaseModel):
    password: str = Field(min_length=3, max_length=3)


class LoginSchema(BaseModel):
    email: EmailStr
    password: str = Field(min_length=9, max_length=256)
