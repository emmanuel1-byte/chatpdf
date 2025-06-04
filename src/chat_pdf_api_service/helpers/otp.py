from datetime import datetime, timezone, timedelta
import secrets

def generate_otp():
    return {
        "password": "".join(secrets.choice("0123456789") for _ in range(3)),
        "expiry_at": datetime.now(timezone.utc) + timedelta(minutes=10),
    }
