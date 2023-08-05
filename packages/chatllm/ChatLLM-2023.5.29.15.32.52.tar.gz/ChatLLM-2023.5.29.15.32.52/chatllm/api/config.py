#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : config
# @Time         : 2023/5/26 13:08
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *
from meutils.decorators import clear_cuda_cache

from chatllm.llms import load_llm4chat

torch_gc = clear_cuda_cache(lambda: logger.info('Clear GPU'), bins=os.getenv('TIME_INTERVAL', 15))

tokens = set(os.getenv('TOKENS', 'chatllm').split(','))
embedding_model = os.getenv('EMBEDDING_MODEL')
if embedding_model:
    from sentence_transformers import SentenceTransformer

    embedding_model = SentenceTransformer(embedding_model)
else:
    class RandomSentenceTransformer:
        def encode(self, texts):
            logger.error("请配置 EMBEDDING_MODEL")
            return np.random.random((len(texts), 64))


    embedding_model = RandomSentenceTransformer()

llm_model = os.getenv('LLM_MODEL')
device = os.getenv('DEVICE', 'cpu')
num_gpus = os.getenv('NUM_GPUS', 2)

if llm_model:  # 必配参数
    do_chat = load_llm4chat(model_name_or_path=llm_model, device=device, num_gpus=num_gpus)
    do_chat = partial(do_chat, return_history=False)
else:
    def do_chat(query, **kwargs):  # DEV
        yield from '请配置 LLM_MODEL'
