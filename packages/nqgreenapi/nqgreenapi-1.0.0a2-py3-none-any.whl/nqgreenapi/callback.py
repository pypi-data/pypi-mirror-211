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


from nqsdk.abstract.callback import CallbackResponse
from nqsdk.abstract.message import SentMeta
from nqsdk.enums import CallbackStatus


class GreenApiCallbackResponse(CallbackResponse):
    def __init__(self, *, status: CallbackStatus, ext_id: str = None, error: str = None):
        self._status = status
        self._error = error
        self._ext_id = ext_id

    @property
    def status(self) -> CallbackStatus:
        return self._status

    @property
    def meta(self) -> SentMeta | None:
        return None

    @property
    def error(self) -> str | None:
        return self._error

    @property
    def code_ok(self) -> int:
        return 200

    def get_content_type(self) -> str | None:
        if (self.status == CallbackStatus.OK and self._ext_id) or self.error:
            return "application/json"

    def get_content(self) -> dict | None:
        if self.status == CallbackStatus.OK and self._ext_id:
            return {"message_id": self._ext_id}
        else:
            if self.error:
                return {"error": self.error}
