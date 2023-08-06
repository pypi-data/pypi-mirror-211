"""
Copyright (c) 2022 Inqana Ltd.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from __future__ import annotations

import json
import math
from datetime import datetime
from importlib import resources
from typing import TYPE_CHECKING, Dict, List, Type

import pytz
import telegram
from nqsdk.abstract.channel import Channel
from nqsdk.abstract.provider import Provider
from nqsdk.exceptions import QuotaExceededException
from telegram.error import RetryAfter

from .message import TelegramBotSentMeta
from .quotas import PerSecondQuota, RetryAfterQuota

if TYPE_CHECKING:  # pragma: no cover
    from nqsdk.abstract.message import Message
    from nqsdk.abstract.quotas import ProviderQuota


class TelegramBotProvider(Provider):
    label = "Telegram Bot provider"

    @classmethod
    def get_channels(cls) -> List[Type[Channel]]:
        return [Channel.create(label="telegram")]

    @classmethod
    def get_config_schema(cls) -> Dict:
        return json.loads(
            resources.files("nqtgbot").joinpath("resources/config_schema.json").read_text()
        )

    @classmethod
    def get_quotas(cls) -> List[ProviderQuota]:
        return [PerSecondQuota()]

    def send(self, *, message: Message) -> TelegramBotSentMeta:
        bot = telegram.Bot(token=self.config["token"])

        try:
            bot_message = bot.send_message(
                chat_id=message.get_recipient_id(), text=message.get_content()
            )
        except RetryAfter as e:
            raise QuotaExceededException(e, quota=RetryAfterQuota(delay=math.ceil(e.retry_after)))

        return TelegramBotSentMeta(
            attempt_uid=message.attempt_uid,
            ext_id=bot_message.message_id,
            dt_sent=datetime.now(tz=pytz.timezone("UTC")),
        )
