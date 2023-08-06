# Unofficial HuggingFace chat api.

### Description

[![Hatch project](https://img.shields.io/badge/%F0%9F%A5%9A-Hatch-4051b5.svg)](https://github.com/pypa/hatch)
[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/release/python-3113/)

A simple async ready wrapper for reverse engineered API of [HuggingChat](https://huggingface.co/chat).

<p>The project has no affiliation with Hugging Face, and it is neither endorsed nor officially supported by Hugging Face. 
The repository owner(s) and contributors cannot be held responsible for any damages or losses resulting from the 
utilization of this repository or its contents. Users bear sole responsibility for their actions and any potential 
consequences that may ensue.</p>

### Installing

```
pip install hf-chat
```

### Quickstart

```
import asyncio
from hf_chat import ChatCompletion

async def main():
    chat = ChatCompletion("email", "password")
    async with chat:
        await chat.create_conversation(switch_to=True)
        user_input = input('> ')
        print(await chat.ask(user_input))
        
asyncio.run(main())
```

<hr>

Inspired by [Soulter/hugging-chat-api](https://github.com/Soulter/hugging-chat-api)