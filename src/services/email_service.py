import aiohttp

from configs.config import settings
from schemas.email_schema import EmailSchema


class EmailSender:
    def __init__(self, email_data: EmailSchema) -> None:
        self.email_data = email_data

    async def send_email(self):
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"http://{settings.email_service.host}:{settings.email_service.port}/api/v1/email/",
                json=self.email_data.model_dump()
            ) as response:
                res = await response.json()
