# -*- coding: utf-8 -*-
# @FileName    : pushplus.py
# @Author  : LUOQIUYOU
# @Time    : 2024/6/11 17:26


import requests
import json
import logging

logger = logging.getLogger('spider.pushplus')


# 使用pushplus服务推送
def pushplus(content, pushplus_token):
    """
    发送推送消息到PushPlus平台。

    参数:
    content -- 要推送的内容。
    pushplus_token -- PushPlus的令牌，用于身份验证。

    返回:
    无返回值。此函数通过HTTP POST请求向PushPlus发送消息。
    """
    # 定义PushPlus的API URL
    api_url = "http://www.pushplus.plus/send/"
    # 定义请求头，模拟Chrome浏览器发送JSON格式的数据
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        "Content-Type": "application/json",
    }
    # 构建要发送的数据，包括令牌、标题、内容和渠道
    data = {
        "token": pushplus_token,
        "title": "WeiboSpider执行通知",
        "content": content,
        "channel": "wechat",
        "template": "json"
    }
    # 将数据转换为JSON格式并编码为UTF-8
    body = json.dumps(data).encode(encoding='utf-8')
    try:
        # 发送POST请求，推送消息
        requests.post(api_url, headers=headers, data=body)
    except Exception as e:
        # 记录异常信息
        logger.exception(e)
