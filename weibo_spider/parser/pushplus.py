# -*- coding: utf-8 -*-
# @FileName    : pushplus.py
# @Author  : LUOQIUYOU
# @Time    : 2024/6/11 17:26


import requests
import json


# 使用pushplus服务推送
def pushplus(content, pushplus_token):
    api_url = "http://www.pushplus.plus/send/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        "Content-Type": "application/json",
    }
    data = {
        "token": pushplus_token,
        "title": "WeiboSpider执行通知",
        "content": content,
        "channel": "wechat",
        "template": "json"
    }
    body = json.dumps(data).encode(encoding='utf-8')
    requests.post(api_url, headers=headers, data=body)

