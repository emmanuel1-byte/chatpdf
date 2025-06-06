from pydantic import BaseModel, EmailStr, Field, field_validator


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


class ForgotPasswordSchema(BaseModel):
    email: EmailStr


class ResetPasswordSchema(BaseModel):
    otp: str = Field(min_length=3, max_length=3)
    password: str = Field(min_length=9, max_length=256)
    confirm_password: str

    @field_validator("confirm_password")
    def passwords_match(cls, v, values):
        if "password" in values.data and v != values.data["password"]:
            raise ValueError("Password do not match")
        return v
