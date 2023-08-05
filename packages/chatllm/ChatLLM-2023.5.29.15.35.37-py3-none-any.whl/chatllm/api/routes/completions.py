#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : completions
# @Time         : 2023/5/26 13:05
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from fastapi import APIRouter, Body, Depends, HTTPException, Request, status, BackgroundTasks
from fastapi.responses import JSONResponse
from sse_starlette import EventSourceResponse

# ME
from meutils.pipe import *
from chatllm.api.config import *
from chatllm.api.datamodels import *
from chatllm.api.routes.stream_response import *
import json

router = APIRouter()


@router.post("/v1/chat/completions")
async def chat_completions(body: ChatBody, request: Request, background_tasks: BackgroundTasks):
    background_tasks.add_task(torch_gc)
    if request.headers.get("Authorization").split(" ")[1] not in tokens:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Token is wrong!")

    if llm_model:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "LLM model not found!")
    question = body.messages[-1]
    chat_kwargs = {"temperature": body.temperature, "top_p": body.top_p, "max_tokens": body.max_tokens}

    if question.role == 'user':
        question = question.content
    else:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "No Question Found")

    history = []
    user_question = ''
    for message in body.messages:
        if message.role == 'system':
            history.append((message.content, "OK"))
        if message.role == 'user':
            user_question = message.content
        elif message.role == 'assistant':
            assistant_answer = message.content
            history.append((user_question, assistant_answer))

    if os.getenv('DEBUG'):
        logger.info(f"question: {question}, history: {history}")

    if body.stream:
        async def eval_llm():
            first = True
            for response in do_chat(question, history=history, **chat_kwargs):
                if first:
                    first = False
                    yield json.dumps(generate_stream_response_start(), ensure_ascii=False)
                yield json.dumps(generate_stream_response(response), ensure_ascii=False)
            yield json.dumps(generate_stream_response_stop(), ensure_ascii=False)
            yield "[DONE]"

        return EventSourceResponse(eval_llm(), ping=10000)
    else:
        response = ''.join(do_chat(question, history=history, **chat_kwargs))
        return JSONResponse(content=generate_response(response))


@router.post("/v1/completions")
async def completions(body: CompletionBody, request: Request, background_tasks: BackgroundTasks):
    background_tasks.add_task(torch_gc)
    if request.headers.get("Authorization").split(" ")[1] not in tokens:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Token is wrong!")

    if not llm_model:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "LLM model not found!")

    question = body.prompt
    chat_kwargs = {"temperature": body.temperature, "top_p": body.top_p, "max_tokens": body.max_tokens}
    if os.getenv('DEBUG'):
        logger.info(f"question: {question}")

    if body.stream:
        async def eval_llm():
            for response in do_chat(question, **chat_kwargs):
                yield json.dumps(generate_stream_response(response, chat=False), ensure_ascii=False)
            yield json.dumps(generate_stream_response_stop(chat=False), ensure_ascii=False)
            yield "[DONE]"

        return EventSourceResponse(eval_llm(), ping=10000)
    else:
        response = ''.join(do_chat(question, **chat_kwargs))
        return JSONResponse(content=generate_response(response, chat=False))
