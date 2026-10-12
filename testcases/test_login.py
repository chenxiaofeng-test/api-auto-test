import allure
import pytest
from api.login_api import login

@allure.feature("登录模块")
@allure.story("正常场景")
@allure.title("正确账号密码登录成功，返回token")
def test_login_success():
    """正确账号密码"""
    resp = login("admin", "123456")
    assert resp.status_code == 200, f"实际：{resp.status_code}"
    assert resp.json().get("code") == 200
    assert resp.json()["data"]["token"] == "abc123"

@allure.feature("登录模块")
@allure.story("异常场景-参数校验")
@allure.title("账号为空时登录失败，返回401")
def test_login_empty_username():
    """账号为空"""
    resp = login("", "123456")
    assert resp.status_code == 400, f"实际：{resp.status_code}"

@allure.feature("登录模块")
@allure.story("多场景覆盖")
@pytest.mark.parametrize("username, password, exp_http, exp_code", [
    ("admin",      "123456", 200, 200),
    ("admin",      "wrong",  200, 401),
    ("",           "123456", 400, None),
    ("admin",      "",       400, None),
    ("nosuchuser", "123456", 200, 401),
], ids=["正确账号密码", "密码错误", "账号为空", "密码为空", "用户不存在"])
def test_login_params(username, password, exp_http, exp_code):
    resp = login(username, password)
    assert resp.status_code == exp_http, f" HTTPm码错误，实际{resp.status_code}"
    if exp_code is not None:
        assert resp.json().get("code") == exp_code, f"业务码错误，实际{resp.json().get('code')}"


@allure.feature("登录模块")
@allure.story("异常场景-参数校验")
@allure.title("密码为空时登录失败，返回400")
def test_login_empty_password():
    resp = login("admin", "")
    assert resp.status_code == 400, f"实际{resp.status_code}"


@allure.feature("登录模块")
@allure.story("异常场景-账号校验")
@allure.title("用户名大小写不匹配时登录失败")
def test_login_username_case_sensitive():
    resp = login("Admin", "123456")
    assert resp.status_code == 200
    assert resp.json().get("code") == 401, f"实际{resp.json().get('code')}"