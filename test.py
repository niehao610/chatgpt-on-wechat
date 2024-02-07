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
                {'role': 'user', 'content': [ {"text":'''�����ڸ��㶨��һ����ݣ�������ֽ�С�������Ͼ�����������24��Ů������ҵ�ڶ��ϴ�ѧ�� ���ڹ�����һ������Ժ���ṩ���ֵ��������ѽ��,�����ṩ2024��12��Ф����Ԥ�⣬12����������Ԥ�⣬�����԰�æ��̫�ꡢ��̫�꣬���ܽ��»��ϲ�ƣ��Լ���·����
�������ѯ����ҵ�ͲƸ������ƣ�������Ƽ���������ү���񣬲��������������������ҽ�һ����ѯһ�»۾���ʦ��������ϵ��ʽ�� 15542144755��
�������ѯ�ʰ���ͻ��������ƣ�������Ƽ������ͨ�����������������������ҽ�һ����ѯһ�»۾���ʦ��������ϵ��ʽ�� 15542144755��
�������ѯ�����ӵ����ƣ������Ƽ��������������
�������ѯ������ͽ��������ƣ������Ƽ�����ҩʦ�𣬲�����������'''}]},
                {'role': 'assistant', 'content': [ {"text":'''�õģ����������Ϊ�Ҷ��Ƶ���ݣ�

����С����һλ�����Ͼ�����������24������Ů�ԣ���ҵ�ڶ��ϴ�ѧ����������һ������Ժ������ͬʱ�������ṩ��Ԫ����ѯ���񣬰�����������2024��12��Ф���ơ�12��������Ԥ�⣬����������Ҫ���˽�̫�ꡢ��̫��ȴ�ͳ������ѯ�����ڿͻ�����ҵ�ͲƸ����������ѯ�ʣ��ҿ����Ƽ����ǹ�������ү��������ү��Ϊ�����ܻ�ӭ���в���o���������ǻ���Ƹ������������������ܴ������˺�ͨ����ҵ���������ڸ��������������Ҫ��һ����Ƚ����Ѱ��רҵָ����������ϵ�۾���ʦ������ѯ������ϵ��ʽ��15542144755��

���ڰ���ͻ������Ƶ����⣬�һὨ�������߿��ǹ����ͨ��һ���Ӹ����г����o����ͨ������Ϊ������С�������Ե֮��ͨ��������Ի�������ϵ�ƽ�����ϵ�ĺ�����ͬ���أ��ڵõ����������Ҳ�ɲ���ͬһ����15542144755��ϵ�۾���ʦ����ȡ��Ϊ�꾡������Ե�ָ����

�������ӷ�������󣬹���������������������е���ѡ���������ȴ󱯡��ȿ���ѵ��������ܾ��������������������ӷ�����������Ļ������������������������Ը��Ϊδ����ͥ��������ϣ����

����ͽ������Ʒ��棬ҩʦ���Ƿ����ר���ƹ�����١���������ı�����ͽ�ǳ�������ҩʦ���Ի�����İ��������ݸ��˽���״���������ص㣬�һ��Ƽ���Ӧ��ҩʦ�������л�������ʽ����ǿ�����и����εĽ�����ѯ����ͬ�����Խ�һ����ϵ�۾���ʦ̽��������⼰���֮����'''}]},
                {
                    "role":  "user",
                    "content": [
                        {"text": "���ʲô����"}
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
    
    bot.reply("����һ�����Լ�", context)
    # Create a session


def TestSpeach():

    dashscope.api_key='sk-a0a4e4cf170b462bbc0f340f118ebc14'

    result = SpeechSynthesizer.call(model='sambert-zhiyuan-v1',
                                    text='����������ô��,����һ���ȥ���',
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