import asyncio
import datetime
import logging
from typing import Final, Optional, Union

import aiohttp

logger = logging.getLogger(__name__)


class TelegramLoggingHandler(logging.Handler):
    telegram_url: Final = "https://api.telegram.org"

    def __init__(
        self,
        token: str,
        chat_ids: list[int],
        level: int = logging.NOTSET,
        session: Optional[aiohttp.ClientSession] = None,
    ):
        super().__init__(level)

        self._token = token
        self._chat_ids = chat_ids

        self.lock = None  # for sending message we do not need lock
        self.session = session

    def emit(self, record: logging.LogRecord) -> None:
        text = self.record2tg(record)

        loop = asyncio.get_event_loop()
        loop.create_task(self.send_message(text))

    def record2tg(self, record: logging.LogRecord):
        msg = self.format(record)
        return f"{msg}\ntime(utc): {datetime.datetime.utcfromtimestamp(record.created)} \nlevel: {record.levelname}\n"

    def format_url(self, method: str):
        return f"{self.telegram_url}/bot{self._token}/{method}"

    async def send_message(self, text: str):
        if self.session is None:
            await self.set_session()

        send = self.get_message_sender(text)

        await asyncio.gather(*[send(ch_id) for ch_id in self._chat_ids])

    async def set_session(self):
        self.session = aiohttp.ClientSession()

    def get_message_sender(self, text: str):
        message: dict[str, Union[str, int]] = {"text": text}

        async def sender(chat_id: int):
            if self.session is None:
                logger.warning("can not send logs to telegram because session is None")

            message["chat_id"] = chat_id
            try:
                response = await self.send2telegram(message)
            except Exception as e:
                logger.warning(f"can not send message to telegram: {e}")
                return
            return response

        return sender

    async def send2telegram(self, message: dict):
        if self.session is None:
            return None
        async with self.session.post(
            self.format_url("sendMessage"), json=message
        ) as resp:
            return resp
