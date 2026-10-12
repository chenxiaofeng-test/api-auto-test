from common.request_client import client

def login(username, password):
    """"登录接口，返回响应对象"""
    return client.post("/api/login", json={"username": username, "password": password})