from datetime import datetime, timedelta, timezone
from typing import Any, Dict

import jwt


def generate_token(public_key: str, secret: str) -> str:

    encoded_jwt: str = jwt.encode(
        {
            "sub": public_key,
            "exp": datetime.now(tz=timezone.utc) + timedelta(seconds=600),
        },
        secret,
        algorithm="HS256",
    )

    return encoded_jwt


def decode_token(token: str, secret: str) -> Dict[str, Any]:
    decoded: Dict[str, Any] = jwt.decode(token, secret, algorithms=["HS256"])
    return decoded
