# -*- coding: utf-8 -*-
# @FileName    : youpush.py
# @Author  : LUOQIUYOU
# @Time    : 2024/8/7 14:54

import requests
import json


def token_expired(err_code):
    """
    判断令牌是否过期。

    通过检查错误码来判断令牌是否过期。不同的错误码对应不同的错误情况，
    在此函数中，特别关注了几种与令牌过期相关的错误码。

    参数:
    err_code (int): 错误码，用于判断令牌是否过期。

    返回:
    bool: 如果令牌过期，返回True；否则返回False。
    """
    # 检查错误码是否为预定义的令牌过期错误码之一
    if err_code == 40014 or err_code == 42001 or err_code == 42007 or err_code == 42009:
        return True
    else:
        return False


class WXPusher:
    def __init__(self, msgtype, msg, title='defaultTitle'):
        self.base_url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken?'
        self.req_url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token='
        self.corpid = 'xxxx'  # 上面提到的你的企业ID
        self.corpsecret = 'xxxx'  # 上图的Secret
        self.agentid = 'xxxx'  # 填写你的企业ID，不加引号，是个整型常数,就是上图的AgentId
        # 初始化用户信息和消息，获取访问令牌
        self.usr = 'xxxx'
        self.msgtype = msgtype
        self.title = title
        self.msg = msg
        self.access_token = self.get_access_token()

    def get_access_token(self):
        """
        获取访问令牌。

        通过向企业微信的API接口发送GET请求，使用企业的corpID和corpSecret来获取访问令牌。
        该方法构建了完整的请求URL，发送请求并解析返回的JSON数据以获取访问令牌。

        :return: 返回获取到的访问令牌字符串。
        """
        # 构建完整的URL，包括企业微信提供的base URL，corpID和corpSecret
        urls = self.base_url + 'corpid=' + self.corpid + '&corpsecret=' + self.corpsecret

        # 发送GET请求并解析返回的JSON数据
        resp = requests.get(urls).json()

        # 从返回的数据中提取access_token
        access_token = resp['access_token']

        # 返回获取到的访问令牌
        return access_token

    def send_message(self):
        """
        发送消息。

        该方法负责组装请求数据，并发送POST请求以提交消息。
        它首先从内部方法获取消息内容和带有访问令牌的请求URL，然后使用requests库发送POST请求。
        请求成功后，将打印出响应的文本内容。

        :return: 无
        """
        # 获取要发送的消息内容
        data = self.get_message()
        # 组装带有访问令牌的完整请求URL
        req_urls = self.req_url + self.access_token
        # 使用requests库发送POST请求，data参数指定要发送的数据
        # 尝试发送请求，最多重试两次
        for retryCnt in range(0, 3):
            # 发送POST请求
            res = requests.post(url=req_urls, data=data)
            # 打印请求的响应文本
            print(res.text)
            # 检查令牌是否过期
            if token_expired(res.json().get('errcode')):
                # 如果令牌过期，重新获取令牌并重试
                self.access_token = self.get_access_token()
                retryCnt += 1
                continue
            else:
                # 如果没有过期，结束循环
                break

    def get_message(self):
        """
        构建并返回微信企业号消息的数据JSON字符串。

        该函数根据当前实例的用户、消息内容以及应用ID，构建一个符合微信企业号消息格式要求的字典，
        并将其转换为JSON格式的字符串。该字符串可用于向微信企业号发送消息。

        Returns:
            str: 构建好的消息数据JSON字符串。
        """
        # 初始化消息字典，包含接收者、消息类型、应用ID等信息
        if self.msgtype == 'text':
            data = {
                "touser": self.usr,  # 接收消息的用户ID
                "toparty": "@all",  # 接收消息的部门，"@all"表示所有人
                "totag": "@all",  # 接收消息的标签，"@all"表示所有人
                "msgtype": "text",  # 消息类型，此处为文本消息
                "agentid": self.agentid,  # 发送消息的应用ID
                "text": {
                    "content": self.msg,  # 文本消息的内容
                },
                "safe": 0,  # 是否加密消息内容，0表示不加密
                "enable_id_trans": 0,  # 是否启用id转换，0表示不启用
                "enable_duplicate_check": 0,  # 是否启用重复消息检查，0表示不启用
                "duplicate_check_interval": 1800  # 重复消息检查的时间间隔，单位为秒
            }
        elif self.msgtype == 'textcard':
            data = {
                "touser": self.usr,  # 接收消息的用户ID
                "toparty": "@all",  # 接收消息的部门，"@all"表示所有人
                "totag": "@all",  # 接收消息的标签，"@all"表示所有人
                "msgtype": "textcard",  # 消息类型，此处为文本卡片消息
                "agentid": self.agentid,  # 发送消息的应用ID
                "textcard": {
                    "title": self.title,  # 文本消息的标题
                    "description": self.msg,  # 文本消息的内容
                    "url": "https://www.baidu.com",  # 点击消息卡片后跳转的URL
                    "btntxt": "更多"  # 消息卡片的按钮文字，默认为“详情”，可自定义
                },
                "safe": 0,  # 是否加密消息内容，0表示不加密
                "enable_id_trans": 0,  # 是否启用id转换，0表示不启用
                "enable_duplicate_check": 0,  # 是否启用重复消息检查，0表示不启用
                "duplicate_check_interval": 1800  # 重复消息检查的时间间隔，单位为秒
            }
        elif self.msgtype == 'markdown':
            data = {
                "touser": self.usr,  # 接收消息的用户ID
                "toparty": "@all",  # 接收消息的部门，"@all"表示所有人
                "totag": "@all",  # 接收消息的标签，"@all"表示所有人
                "msgtype": "markdown",  # 消息类型，此处为文本消息
                "agentid": self.agentid,  # 发送消息的应用ID
                "markdown": {
                    "content": self.msg,  # 文本消息的内容
                },
                "safe": 0,  # 是否加密消息内容，0表示不加密
                "enable_id_trans": 0,  # 是否启用id转换，0表示不启用
                "enable_duplicate_check": 0,  # 是否启用重复消息检查，0表示不启用
                "duplicate_check_interval": 1800  # 重复消息检查的时间间隔，单位为秒
            }
        # 将消息字典转换为JSON格式的字符串
        data = json.dumps(data)
        return data
