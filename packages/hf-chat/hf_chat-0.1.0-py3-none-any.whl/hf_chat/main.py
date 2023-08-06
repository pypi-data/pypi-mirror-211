import copy
import json
import uuid
from typing import Optional, Self, Generator

import aiohttp

from .exceptions import LoginException, InteractionFailedException, InferenceFailedException


class ChatCompletion:
    def __init__(self, email: str, password: str) -> None:
        self._session: Optional[aiohttp.ClientSession] = None
        self._current_conversation: str = ''
        self._auth_payload = {
            'username': email,
            'password': password
        }
        self._default_payload = {'inputs': '',
                                 'parameters': {'temperature': 0.9,
                                                'truncate': 1000,
                                                'max_new_tokens': 1024,
                                                'stop': ["</s>"],
                                                'top_p': 0.95,
                                                'repetition_penalty': 1.2,
                                                'top_k': 50,
                                                'return_full_text': False},
                                 'stream': True,
                                 'options': {'id': '',
                                             'response_id': '',
                                             'is_retry': False,
                                             'use_cache': False}
                                 }

    async def _login(self) -> None:
        async with self._session.post('/login', json=self._auth_payload) as resp:
            if not resp.ok:
                raise LoginException(resp.reason, status_code=resp.status)
        headers = {
            'Referer': 'https://huggingface.co/chat/login',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        async with self._session.post('/chat/login', headers=headers) as resp:
            if not resp.ok:
                raise LoginException(resp.reason, status_code=resp.status)
            location = (await resp.json())['location'][len('https://huggingface.co'):]
        async with self._session.post(url=location) as resp:
            if not resp.ok:
                raise LoginException(resp.reason, status_code=resp.status)

    def _setup_payload(self, prompt) -> dict:
        payload = copy.deepcopy(self._default_payload)
        payload['inputs'] = prompt
        payload['options']['id'] = str(uuid.uuid4())
        payload['options']['response_id'] = str(uuid.uuid4())
        return payload

    async def __aenter__(self) -> Self:
        await self.start()
        return self

    async def __aexit__(self, *args) -> None:
        await self.close()

    async def start(self) -> None:
        self._session = aiohttp.ClientSession('https://huggingface.co')
        await self._login()

    async def close(self):
        if self._session:
            await self._session.close()

    async def create_conversation(self, *, switch_to: bool = False) -> str:
        async with self._session.post('/chat/conversation',
                                      json={'model': 'OpenAssistant/oasst-sft-6-llama-30b-xor'}) as resp:
            if not resp.ok:
                raise InteractionFailedException(resp.reason, status_code=resp.status)
            conversation_id = (await resp.json())['conversationId']
            if switch_to:
                self.switch_conversation(conversation_id)
            return conversation_id

    def switch_conversation(self, conversation_id) -> None:
        self._current_conversation = conversation_id

    async def summarize_current_conversation(self) -> str:
        return await self.summarize_conversation(self._current_conversation)

    async def summarize_conversation(self, conversation_id: str) -> str:
        async with self._session.post(f'/chat/conversation/{conversation_id}/summarize') as resp:
            if not resp.ok:
                raise InteractionFailedException(resp.reason, status_code=resp.status)
            return (await resp.json())['title']

    async def ask_stream(self, prompt: str) -> Generator[str, None, None]:
        payload = self._setup_payload(prompt)
        async with self._session.post(f'/chat/conversation/{self._current_conversation}', json=payload) as resp:
            if not resp.ok:
                raise InferenceFailedException(resp.reason, status_code=resp.status)
            while not resp.content.at_eof():
                chunk = await resp.content.readline()
                chunk = chunk[len('data:'):]
                if chunk:
                    json_chunk = json.loads(chunk)
                    yield json_chunk['token']['text']

    async def ask(self, prompt) -> str:
        payload = self._setup_payload(prompt)
        async with self._session.post(f'/chat/conversation/{self._current_conversation}', json=payload) as resp:
            if not resp.ok:
                raise InferenceFailedException(resp.reason, status_code=resp.status)
            while not resp.content.at_eof():
                chunk = await resp.content.readline()
                chunk = chunk[len('data:'):]
                if chunk:
                    json_chunk = json.loads(chunk)
                    if json_chunk['generated_text'] is not None:
                        return json_chunk['generated_text']
