# -*- coding: utf-8 -*-
"""
Author: chazzjimel
Email: chazzjimel@gmail.com
wechat：cheung-z-x

Description:
ali voice service

"""
import json
import os
import re
import time

from bridge.reply import Reply, ReplyType
from common.log import logger
from voice.voice import Voice
from voice.ali.ali_api import AliyunTokenGenerator
from voice.ali.ali_api import text_to_speech_aliyun
from voice.ali.ali_api import speech_to_text_aliyun
from config import conf


class AliVoice(Voice):
    def __init__(self):
        """
        初始化AliVoice类，从配置文件加载必要的配置。
        """
        try:
            curdir = os.path.dirname(__file__)
            config_path = os.path.join(curdir, "config.json")
            logger.info("AliVoice init success")
            with open(config_path, "r") as fr:
                config = json.load(fr)
            self.token = None
            self.token_expire_time = 0
            # 默认复用阿里云千问的 access_key 和 access_secret
            self.api_url = "1"
            self.app_key = "1"
            self.access_key_id =config["access_key_id"]
            self.access_key_secret = config["access_key_secret"]
        except Exception as e:
            logger.warn("AliVoice init failed: %s, ignore " % e)

    def textToVoice(self, text):
        """
        将文本转换为语音文件。

        :param text: 要转换的文本。
        :return: 返回一个Reply对象，其中包含转换得到的语音文件或错误信息。
        """
        # 清除文本中的非中文、非英文和非基本字符
        text = re.sub(r'[^\u4e00-\u9fa5\u3040-\u30FF\uAC00-\uD7AFa-zA-Z0-9'
                      r'äöüÄÖÜáéíóúÁÉÍÓÚàèìòùÀÈÌÒÙâêîôûÂÊÎÔÛçÇñÑ，。！？,.]', '', text)
        # 提取有效的token
        token_id = ""
        fileName = text_to_speech_aliyun("", text, "","")
        if fileName:
            logger.info("[Ali] textToVoice text={} voice file name={}".format(text, fileName))
            reply = Reply(ReplyType.VOICE, fileName)
        else:
            reply = Reply(ReplyType.ERROR, "抱歉，语音合成失败")
        return reply

    def get_valid_token(self):
       return ""
    
    def voiceToText(self, voice_file):
        logger.info("[ALI] voice file name={}".format(voice_file))
        try:
            text = speech_to_text_aliyun(voice_file)
            reply = Reply(ReplyType.TEXT, text)
            logger.info("[ALI] voiceToText text={} voice file name={}".format(text, voice_file))
        except Exception as e:
            logger.warn("[ALI] voiceToText failed: %s" % e)
            reply = Reply(ReplyType.ERROR, "我暂时还无法听清您的语音，请稍后再试吧~")
        finally:
            return reply