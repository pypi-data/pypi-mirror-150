import uuid
import requests
import json
import enum
import zipfile
import tarfile
import os
from multiprocessing import  Process, Pool
import urllib.parse as path_encoder
import time
import datetime


HELLO_WORLD_MESSAGE = 'Hello world! PyOhio Demo - 3! CLEpy'

API_GW = "https://aaw5kr39wf.execute-api.cn-north-1.amazonaws.com.cn/api/"

def test_login():
    headers = {
        'Content-Type': 'application/json'
    }
    API_GW = "https://aaw5kr39wf.execute-api.cn-north-1.amazonaws.com.cn/api/"
    account_info = {
        "username": "yaru",
        "password": "intelpass"
    }
    payload = json.dumps(account_info)
    print(f"payload {payload}")
    response = requests.request("POST", f"{API_GW}/login", headers=headers, data=payload)
    print(response)
    response_body = json.loads(response.text)
    token = response_body["data"]["token"]
    print(token)
    return 1


def get_message():
    return HELLO_WORLD_MESSAGE

