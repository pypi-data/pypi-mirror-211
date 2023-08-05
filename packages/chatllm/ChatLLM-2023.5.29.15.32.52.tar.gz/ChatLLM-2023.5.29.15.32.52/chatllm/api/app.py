#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : app
# @Time         : 2023/5/26 14:59
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :

from meutils.pipe import *

os.environ['LLM_MODEL'] = '/Users/betterme/PycharmProjects/AI/CHAT_MODEL/chatglm'
os.environ['DEBUG'] = '1'

from meutils.serving.fastapi import App

from chatllm.api.routes.api import router

app = App()
app.include_router(router)

if __name__ == '__main__':
    app = App()
    app.include_router(router)
    app.run()
