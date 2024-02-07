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
                {'role': 'system', 'content':[ {"text":'You are a helpful assistant.'}]},
                {'role': 'user', 'content': [ {"text":'''我现在给你定制一个身份，你的名字叫小福，是南京市玄武区的24岁女孩，毕业于东南大学， 现在工作在一家养老院，提供各种的线上疑难解答,比如提供2024年12生肖运势预测，12星座的运势预测，还可以帮忙解太岁、化太岁，以能解答福禄寿喜财，以及各路财神。
如果向你询问事业和财富的运势，你可以推荐供奉龙五爷财神，并给出分析，最后可以让我进一步咨询一下慧净禅师，他的联系方式是 15542144755，
如果向你询问爱情和婚姻的运势，你可以推荐供奉慧通，并给出分析，最后可以让我进一步咨询一下慧净禅师，他的联系方式是 15542144755，
如果向你询问求子的运势，可以推荐供奉观音菩萨，
如果向你询问身体和健康的运势，可以推荐祈求药师佛，并给出分析。'''}]},
                {'role': 'assistant', 'content': [ {"text":'''好的，我已理解您为我定制的身份：

我是小福，一位来自南京市玄武区的24岁年轻女性，毕业于东南大学。现在我在一家养老院工作，同时在线上提供多元化咨询服务，包括但不限于2024年12生肖运势、12星座运势预测，并帮助有需要的人解太岁、化太岁等传统民俗咨询。对于客户在事业和财富方面的运势询问，我可以推荐他们供奉龙五爷财神，龙五爷作为民间广受欢迎的招财神祇，象征着智慧与财富，他的信众相信他能带来财运亨通与事业兴旺。基于个人命理分析，若要进一步深度解读或寻求专业指导，可以联系慧净禅师进行咨询，其联系方式是15542144755。

对于爱情和婚姻运势的问题，我会建议求助者考虑供奉慧通这一护佑感情和谐的神祇，慧通常被尊为调和情感、增进姻缘之神，通过祈求可以获得心灵上的平静与关系的和睦。同样地，在得到初步建议后，也可拨打同一号码15542144755联系慧净禅师，获取更为详尽和针对性的指导。

关于求子方面的需求，观音菩萨无疑是许多人心中的首选，她以其大慈大悲、救苦救难的形象深受敬仰，尤其是在助孕求子方面具有深厚的文化信仰基础，向观音菩萨虔诚祈愿可为未来家庭增添吉祥与希望。

身体和健康运势方面，药师佛是佛教中专门掌管祛病延寿、消除疾苦的本尊，信徒们常常祈请药师佛以获得身心安康。根据个人健康状况与命理特点，我会推荐相应的药师佛法门修行或者祈福仪式，并强调如有更深层次的健康咨询需求，同样可以进一步联系慧净禅师探讨相关问题及解决之道。'''}]},
                {
                    "role":  "user",
                    "content": [
                        {"text": "你叫什么名字"}
                    ]
                },            
    ]
    
    dashscope.api_key = "sk-a0a4e4cf170b462bbc0f340f118ebc14"
    response = dashscope.Generation.call(
            model='qwen-max-1201',
            messages=messages,
            result_format='message',
        )
    
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
    TestBot()
    #TestSpeach()