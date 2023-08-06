#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : __init__
# @Time         : 2023/5/26 13:29
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *


# MODEL_BASE = {'chatglm'}
def load_llm4chat(model_name_or_path="THUDM/chatglm-6b", device='cpu', num_gpus=2, model_base=None, **kwargs):
    if not model_base:  # 模型基座
        model_base = Path(model_name_or_path).name.lower()
        for p in Path(__file__).parent.glob('*.py'):
            if p.stem in model_base:
                # logger.warning(p) # 自动推断模型基座
                model_base = p.stem

    logger.info(f"MODEL_BASE: {model_base}")

    try:
        model_base = importlib.import_module(f"chatllm.llms.{model_base}")
        do_chat = model_base.load_llm4chat(
            model_name_or_path=model_name_or_path,
            device=device,
            num_gpus=num_gpus,
            **kwargs)
        return do_chat

    except Exception as e:
        logger.error(f"Unsupported model base: {e}")

        def do_chat(query, **kwargs):  # DEV
            logger.warning("测试环境: 生产环境，请配置 LLM_MODEL !!!")
            yield from query

        return do_chat


if __name__ == '__main__':
    print(load_llm4chat('/Users/betterme/PycharmProjects/AI/CHAT_MODEL/chatglm'))
    # print(Path(__file__).parent)
