# Copyright (c) 2023 Inqana Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import annotations

import json
from datetime import datetime
from importlib import resources
from typing import TYPE_CHECKING

import pytz
from pydantic import ValidationError
from rest_framework.status import HTTP_204_NO_CONTENT
from whatsapp_api_client_python import API

from nqsdk.abstract.channel import Channel
from nqsdk.abstract.provider import Provider, StaticCallbackHandleMixin
from nqsdk.enums import CallbackEvent, CallbackStatus
from nqsdk.exceptions import (
    CallbackHandlingException,
    SentException,
    UnsupportedCallbackEventException,
)

from .callback import GreenApiCallbackResponse
from .message import GreenApiExtIdCallbackMeta, GreenApiSentMeta
from .serializers import OutgoingMessageStatusModel
from .utils import flatten_errors

if TYPE_CHECKING:  # pragma: no cover
    from rest_framework.request import Request

    from nqsdk.abstract.message import Message

    from .callback import CallbackResponse
    from .message import ExtIdCallbackMeta


class GreenApiProvider(StaticCallbackHandleMixin, Provider):
    label = "Green Api provider"

    WEBHOOK_TYPE_MAP = {"outgoingMessageStatus": "outgoing_message_status"}

    @classmethod
    def get_config_schema(cls) -> dict:
        return json.loads(
            resources.files("nqgreenapi").joinpath("resources/config_schema.json").read_text()
        )

    @classmethod
    def get_channels(cls) -> list[type[Channel]]:
        return [Channel.create(label="whatsapp", is_ack_supported=True, is_delivery_supported=True)]

    def send(self, *, message: Message) -> GreenApiSentMeta:
        green_api = API.GreenApi(self.config["id_instance"], self.config["api_token_instance"])

        result = green_api.sending.sendMessage(
            chatId=f"{message.get_recipient_id()}@c.us", message=message.get_content()
        )

        if result.error:
            raise SentException(result.error)

        return GreenApiSentMeta(
            attempt_uid=message.attempt_uid,
            ext_id=result.data["idMessage"],
            dt_sent=datetime.now(tz=pytz.timezone("UTC")),
        )

    def handle_static_callback(
        self, *, request: Request
    ) -> tuple[CallbackResponse, ExtIdCallbackMeta]:
        data = request.data
        webhook = data.get("typeWebhook")
        if webhook in self.WEBHOOK_TYPE_MAP:
            method = getattr(self, f"_handle_{self.WEBHOOK_TYPE_MAP[webhook]}_webhook")
            return method(data)
        else:
            raise UnsupportedCallbackEventException(code=HTTP_204_NO_CONTENT)

    def _handle_outgoing_message_status_webhook(
        self, data: dict
    ) -> tuple[CallbackResponse, ExtIdCallbackMeta]:
        try:
            model = OutgoingMessageStatusModel(**data)
        except ValidationError as e:
            raise CallbackHandlingException(
                response=GreenApiCallbackResponse(
                    status=CallbackStatus.FAILED, error=flatten_errors(e.errors())
                )
            )

        status = model.status
        if status == "delivered":
            event = CallbackEvent.DELIVERY
        elif status == "read":
            event = CallbackEvent.ACK
        else:
            raise UnsupportedCallbackEventException(code=HTTP_204_NO_CONTENT)

        ext_id = model.idMessage
        dt_updated = datetime.fromtimestamp(model.timestamp, tz=pytz.UTC)

        return GreenApiCallbackResponse(
            status=CallbackStatus.OK, ext_id=ext_id
        ), GreenApiExtIdCallbackMeta(dt_updated=dt_updated, event=event, ext_id=ext_id)
