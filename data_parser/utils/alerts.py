import json
import time
from typing import Callable

from httpx import AsyncClient


async def send_alert_to_tg_bot(func_name: str, exception: Exception, comment: str | None = None):
    data = {
        "chat_id": 222249912,
        "service": "cosm-report-bot",
        "time": int(time.time()),
        "message": f"\n"
                   f"Exception: {exception.__repr__()}\n"
                   f"Function: {func_name}",
    }
    if comment:
        data["message"] += f"\nComment: {comment}"
    async with AsyncClient() as ac:
        await ac.post("http://alert-bot:8080/alert", json=data)