# Copyright 2021 ONDEWO GmbH
#
# Licensed under the Apache License, Version 2.0 (the License);
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an AS IS BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import functools
from abc import ABCMeta, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, Callable, List, Optional

import grpc
import regex as re
from ondewo.logging.decorators import Timer
from ondewo.logging.logger import logger_console
from ondewo.nlu import session_pb2, intent_pb2, user_pb2, context_pb2
from ondewo.nlu.client import Client as NLUClient
from ondewo.nlu.session_pb2 import TextInput

from ondewo_bpi.autocoded.agent_grpc_autocode import AutoAgentsServicer
from ondewo_bpi.autocoded.aiservices_grpc_autocode import AutoAiServicesServicer
from ondewo_bpi.autocoded.context_grpc_autocode import AutoContextsServicer
from ondewo_bpi.autocoded.entity_type_grpc_autocode import AutoEntityTypesServicer
from ondewo_bpi.autocoded.intent_grpc_autocode import AutoIntentsServicer
from ondewo_bpi.autocoded.project_role_grpc_autocode import AutoProjectRolesServicer
from ondewo_bpi.autocoded.session_grpc_autocode import AutoSessionsServicer
from ondewo_bpi.autocoded.user_grpc_autocode import AutoUsersServicer
from ondewo_bpi.config import SENTENCE_TRUNCATION
from ondewo_bpi.constants import SipTriggers, QueryTriggers
from ondewo_bpi.helpers import get_session_from_response
from ondewo_bpi.message_handler import MessageHandler, SingleMessageHandler


@dataclass()
class IntentCallbackAssignor:
    """Class for keeping track of the intents and their handlers"""
    sort_index: int = field(init=False, repr=False)
    intent_pattern: str
    handlers: List[Callable]

    def __gt__(self, other: 'IntentCallbackAssignor') -> bool:
        return self.sort_index > other.sort_index

    def __lt__(self, other: 'IntentCallbackAssignor') -> bool:
        return self.sort_index < other.sort_index

    def __post_init__(self):
        object.__setattr__(self, 'sort_index', len(self.intent_pattern))


class BpiSessionsServices(AutoSessionsServicer):
    __metaclass__ = ABCMeta

    @property
    @abstractmethod
    def client(self) -> NLUClient:
        pass

    def __init__(self) -> None:
        self.intent_handlers: List[IntentCallbackAssignor] = list()
        self.trigger_handlers: Dict[str, Callable] = {
            i.value: self.trigger_function_not_implemented for i in [*SipTriggers, *QueryTriggers]
        }

    def register_intent_handler(self, intent_pattern: str, handlers: List[Callable]) -> None:
        intent_handler: IntentCallbackAssignor = IntentCallbackAssignor(intent_pattern=intent_pattern,
                                                                        handlers=handlers)
        self.intent_handlers.append(intent_handler)
        self.intent_handlers = sorted(self.intent_handlers, reverse=True)

    def register_trigger_handler(self, trigger: str, handler: Callable) -> None:
        self.trigger_handlers[trigger] = handler

    def trigger_function_not_implemented(
            self,
            response: session_pb2.DetectIntentResponse,
            message: intent_pb2.Intent.Message,
            trigger: str,
            found_triggers: Dict[str, List[str]],
    ) -> None:
        logger_console.warning(
            {
                "message": f"no function for the trigger {trigger}, please subclass and implement",
                "trigger": trigger,
                "content": found_triggers[trigger],
            }
        )

    def DetectIntent(
            self, request: session_pb2.DetectIntentRequest, context: grpc.ServicerContext
    ) -> session_pb2.DetectIntentResponse:
        try:
            if len(request.query_input.text.text) > SENTENCE_TRUNCATION:
                logger_console.warning(f'The received text is too long, it will be truncated '
                                       f'to {SENTENCE_TRUNCATION} characters!')
            truncated_text: TextInput = TextInput(text=request.query_input.text.text[:SENTENCE_TRUNCATION])
            request.query_input.text.CopyFrom(truncated_text)
            text = request.query_input.text.text
        except Exception as e:
            logger_console.exception(f"An issue was encountered in BPI:\n"
                                     f"\tSeems like the request query_input data was not properly formatted\n"
                                     f"\tDetails: {e}")
            text = "error"
        logger_console.debug(
            {
                "message": f"CAI-DetectIntentRequest to CAI, text input: {text}",
                "content": text,
                "text": text,
                "tags": ["text"],
            }
        )
        cai_response = self.perform_detect_intent(request)
        intent_name = cai_response.query_result.intent.display_name
        logger_console.debug(
            {
                "message": f"CAI-DetectIntentResponse from CAI, intent_name: {intent_name}",
                "content": intent_name,
                "intent_name": intent_name,
                "session_id": get_session_from_response(cai_response),
                "tags": ["text"],
            }
        )

        cai_response = self.process_messages(cai_response)
        return self.process_intent_handler(cai_response)

    @Timer(log_arguments=False, recursive=True)
    def perform_detect_intent(self,
                              request: session_pb2.DetectIntentRequest, ) -> session_pb2.DetectIntentResponse:
        return self.client.services.sessions.detect_intent(request)

    @Timer(log_arguments=False, recursive=True)
    def process_messages(self,
                         response: session_pb2.DetectIntentResponse, ) -> session_pb2.DetectIntentResponse:
        for j, message in enumerate(response.query_result.fulfillment_messages):
            found_triggers = MessageHandler.get_triggers(message, get_session_from_response(response))

            for found_trigger in found_triggers:
                new_response: Optional[session_pb2.DetectIntentResponse] = \
                    self.trigger_handlers[found_trigger](response, message, found_trigger, found_triggers)

                if new_response:
                    if not new_response.response_id == response.response_id:
                        return new_response

            for found_trigger in found_triggers:
                SingleMessageHandler.substitute_pattern_in_message(message, found_trigger, "")

            self.quicksend_to_api(response, message, j)
        if not len(response.query_result.fulfillment_messages):
            self.quicksend_to_api(response, None, 0)
        return response

    def quicksend_to_api(
            self, response: session_pb2.DetectIntentResponse, message: Optional[intent_pb2.Intent.Message],
            count: int
    ) -> None:
        logger_console.warning({"message": "quicksend_to_api not written, please subclass and implement"})

    @Timer(log_arguments=False, recursive=True)
    def process_intent_handler(
            self, cai_response: session_pb2.DetectIntentResponse
    ) -> session_pb2.DetectIntentResponse:
        # Create an ordered dictionary by key value length
        intent_name = cai_response.query_result.intent.display_name
        handlers: List[Callable] = self._get_handlers_for_intent(intent_name, self.intent_handlers)
        for handler in handlers:
            cai_response = handler(cai_response, self.client)
            text = [i.text.text for i in cai_response.query_result.fulfillment_messages]
            logger_console.info(
                {
                    "message": f"BPI-DetectIntentResponse from BPI with text: {text}",
                    "content": text,
                    "text": text,
                    "tags": ["text", "clean"],
                }
            )
        return cai_response

    def _get_handlers_for_intent(self, intent_name: str,
                                 assignors: List[IntentCallbackAssignor]) -> List[Callable]:
        for assignor in assignors:
            if re.match(assignor.intent_pattern, intent_name):
                return assignor.handlers
        return []


class BpiUsersServices(AutoUsersServicer):
    __metaclass__ = ABCMeta

    @property
    @abstractmethod
    def client(self) -> NLUClient:
        pass

    def Login(self, request: user_pb2.LoginRequest, context: grpc.ServicerContext) -> user_pb2.LoginResponse:
        logger_console.info(f'Login request handled by bpi\n'
                            f'Login user: {request.user_email}')
        return super().Login(request, context)


class BpiContextServices(AutoContextsServicer):
    __metaclass__ = ABCMeta

    @property
    @abstractmethod
    def client(self) -> NLUClient:
        pass

    def CreateContext(
            self, request: context_pb2.CreateContextRequest, context: grpc.ServicerContext
    ) -> context_pb2.Context:
        logger_console.info("passing create context request on to CAI")
        return self.client.services.contexts.create_context(request=request)


class BpiAgentsServices(AutoAgentsServicer):
    __metaclass__ = ABCMeta

    @property
    @abstractmethod
    def client(self) -> NLUClient:
        pass


class BpiEntityTypeServices(AutoEntityTypesServicer):
    __metaclass__ = ABCMeta

    @property
    @abstractmethod
    def client(self) -> NLUClient:
        pass


class BpiAiServicesServices(AutoAiServicesServicer):
    __metaclass__ = ABCMeta

    @property
    @abstractmethod
    def client(self) -> NLUClient:
        pass


class BpiIntentsServices(AutoIntentsServicer):
    __metaclass__ = ABCMeta

    @property
    @abstractmethod
    def client(self) -> NLUClient:
        pass


class BpiProjectRolesServices(AutoProjectRolesServicer):
    __metaclass__ = ABCMeta

    @property
    @abstractmethod
    def client(self) -> NLUClient:
        pass
