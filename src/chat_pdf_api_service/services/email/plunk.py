import requests
from ...utils import logger
import os
from dotenv import load_dotenv

load_dotenv()


def send_verification_email(email: str, first_name, code: str):
    response = requests.post(
        "https://api.useplunk.com/v1/track",
        json={
            "event": "user-signup",
            "email": email,
            "data": {
                "OTP": {
                    "value": code,
                    "persistent": False,
                },
                "firstName": {
                    "value": first_name,
                    "persistent": False,
                },
            },
        },
        headers={"Authorization": f"Bearer {os.getenv('PLUNK_SECRET_KEY')}"},
    )
    if response.status_code == 200:
        logger.info(f"Email sent: { response.json()}")
    response.raise_for_status()




def send_password_reset_email(email: str, first_name, code: str):
    response = requests.post(
        "https://api.useplunk.com/v1/track",
        json={
            "event": "reset-password",
            "email": email,
            "data": {
                "OTP": {
                    "value": code,
                    "persistent": False,
                },
                "firstName": {
                    "value": first_name,
                    "persistent": False,
                },
            },
        },
        headers={"Authorization": f"Bearer {os.getenv('PLUNK_SECRET_KEY')}"},
    )
    if response.status_code == 200:
        logger.info(f"Email sent: { response.json()}")
    response.raise_for_status()
