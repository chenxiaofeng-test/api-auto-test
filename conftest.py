import pytest
from api.login_api import login
from api.user_api import delete_user


@pytest.fixture
def token():
    """登录拿 token，所有需要登录的用例直接用"""
    resp = login("admin", "123456")
    return resp.json()["data"]["token"]


@pytest.fixture
def clean_user(token):
    """记录用例创建的用户id，跑完自动删除"""
    created_ids = []
    yield created_ids
    for uid in created_ids:
        delete_user(token, uid)