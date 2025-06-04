import requests
from ...utils import logger
import os
from dotenv import load_dotenv

load_dotenv()


"""
Send a verification email to a user with a one-time password (OTP).

This function sends a POST request to the Plunk API to track a user signup event,
including the user's email, first name, and a non-persistent OTP code. Logs the
response if the email is sent successfully.

Args:
    email (str): The recipient's email address.
    first_name (str): The recipient's first name.
    code (str): The OTP code to be sent.

Raises:
    HTTPError: If the request to the API fails.
"""


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
