# -*- coding: gbk -*-
import json
import time
from typing import List, Tuple

import openai
import openai.error
import broadscope_bailian
from broadscope_bailian import ChatQaMessage

from bot.ali.ali_qwen_bot import AliQwenBot
from bot.bot import Bot
from bot.ali.ali_qwen_session import AliQwenSession
from bot.session_manager import SessionManager

from bridge.context import ContextType
from bridge.context import Context
from bridge.reply import Reply, ReplyType
from common.log import logger
from common import const
from config import conf, load_config
from http import HTTPStatus
import dashscope
from dashscope.audio.tts import SpeechSynthesizer


def simple_multimodal_conversation_call():
    """Simple single round multimodal conversation call.
    """
    messages = [
        {
            "role": "user",
            "content": [
                {"text": "介绍一下你自己?"}
            ]
        }
    ]
    dashscope.api_key = "sk-a0a4e4cf170b462bbc0f340f118ebc14"
    response = dashscope.MultiModalConversation.call(model='qwen-vl-plus',
                                                     messages=messages)
    
    # The response status_code is HTTPStatus.OK indicate success,
    # otherwise indicate request is failed, you can get error code
    # and message from code and message.
    if response.status_code == HTTPStatus.OK:
        print(response)
    else:
        print(response.code)  # The error code.
        print(response.message)  # The error message.


def TestBot():
    """Test bot.
    """
    # Load configuration.
    load_config()
    # Create a bot.
    bot = AliQwenBot()
    context = Context(
        ContextType.TEXT,
        "",
        {"session_id":123}
        )
    
    bot.reply("介绍一下你自己", context)
    # Create a session


def TestSpeach():

    dashscope.api_key='sk-a0a4e4cf170b462bbc0f340f118ebc14'

    result = SpeechSynthesizer.call(model='sambert-zhiyuan-v1',
                                    text='今天天气怎么样,我们一起出去玩吧',
                                    sample_rate=48000,
                                    format='wav')

    if result.get_audio_data() is not None:
        with open('D:\\py_project\\chatgpt-on-wechat\\output-sambert-zhiyuan-v1.wav', 'wb') as f:
            f.write(result.get_audio_data())
    print('  get response: %s' % (result.get_response()))

if __name__ == '__main__':
    #simple_multimodal_conversation_call()
    #TestBot()
    TestSpeach()