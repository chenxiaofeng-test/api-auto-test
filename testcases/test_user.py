import pytest
from api.user_api import list_users, create_user, delete_user
import allure

@allure.feature("用户模块")
@allure.story("查询用户列表")
@allure.title("带有效token查询用户列表成功")
def test_list_users_with_token(token):
    """带 token 查列表"""
    resp = list_users(token)
    assert resp.status_code == 200, f"实际 {resp.status_code}"
    assert resp.json().get("code") == 200

@allure.feature("用户模块")
@allure.story("异常场景-鉴权")
@allure.title("未携带token查询用户列表，返回401")
def test_list_users_without_token():
    """不带 token → 401"""
    resp = list_users(None)
    assert resp.status_code == 401, f"实际 {resp.status_code}"

@allure.feature("用户模块")
@allure.story("异常场景-鉴权")
@allure.title("携带无效token查询用户列表，返回401")
def test_list_users_wrong_token():
    """假 token → 401"""
    resp = list_users("wrongtoken")
    assert resp.status_code == 401, f"实际 {resp.status_code}"

@allure.feature("用户模块")
@allure.story("删除用户")
@allure.title("删除用户成功，数据库校验记录已清除")
def test_delete_user_with_db_check(token):
    """删除 + 数据库校验"""
    resp = create_user(token, "待删除", "13900008888")
    new_id = resp.json()["data"]["id"]

    resp = delete_user(token, new_id)
    assert resp.status_code == 200
    assert resp.json().get("msg") == "删除成功"

    # 数据库校验
    from common.db_client import query_one
    rows = query_one("SELECT id FROM users WHERE id = ?", (new_id,))
    assert len(rows) == 0, f"接口说删了，但数据库里还有 {len(rows)} 条"

@allure.feature("用户模块")
@allure.story("新增用户")
@allure.title("新增用户成功，数据库校验字段一致")
def test_create_user_with_db_check(token):
    """新增 + 数据库校验"""
    username = "张三测试"
    phone = "13711112222"

    resp = create_user(token, username, phone)
    new_id = resp.json()["data"]["id"]

    from common.db_client import query_one
    rows = query_one("SELECT id, username, phone FROM users WHERE id = ?", (new_id,))
    assert len(rows) == 1, "数据库里没查到这条记录"
    assert rows[0][1] == username, f"用户名不一致，实际 {rows[0][1]}"
    assert rows[0][2] == phone, f"手机号不一致，实际 {rows[0][2]}"

    delete_user(token, new_id)   # 清理

@allure.feature("用户模块")
@allure.story("异常场景-删除")
@allure.title("删除不存在的用户id，返回404")
def test_delete_user_not_exist(token):
    resp = delete_user(token, 99999)
    assert resp.status_code == 404, f"实际 {resp.status_code}"


@allure.feature("用户模块")
@allure.story("异常场景-删除")
@allure.title("删除id为0的用户，返回404")
def test_delete_user_id_zero(token):
    resp = delete_user(token, 0)
    assert resp.status_code == 404, f"实际 {resp.status_code}"


@allure.feature("用户模块")
@allure.story("异常场景-删除")
@allure.title("删除负数id的用户，返回404")
def test_delete_user_negative_id(token):
    resp = delete_user(token, -1)
    assert resp.status_code == 404, f"实际 {resp.status_code}"



@allure.feature("用户模块")
@allure.story("异常场景-参数类型")
@allure.title("删除非数字id，返回422")
def test_delete_user_invalid_id_type(token):
    resp = delete_user(token, "abc")
    assert resp.status_code == 422, f"实际 {resp.status_code}"



@pytest.mark.xfail(reason="缺陷BUG-001:手机号未做格式校验", strict=False)
@allure.feature("用户模块")
@allure.story("异常场景-参数校验")
@allure.title("手机号为字母时新增应失败")
def test_create_user_phone_with_letter(token, clean_user):
    resp = create_user(token, "测试", "abc")
    if resp.status_code == 200:
        clean_user.append(resp.json()["data"]["id"])
    assert resp.status_code == 400, f"实际{resp.status_code}, 接口未做校验"


@pytest.mark.xfail(reason="缺陷BUG-001：手机号未做长度校验", strict=False)
@allure.feature("用户模块")
@allure.story("异常场景-参数校验")
@allure.title("手机号长度不足时新增应失败")
def test_create_user_phone_too_short(token):
    resp = create_user(token, "测试", "138")
    assert resp.status_code == 400, f"实际 {resp.status_code}"


@pytest.mark.xfail(reason="缺陷BUG-001：手机号未做长度校验", strict=False)
@allure.feature("用户模块")
@allure.story("异常场景-参数校验")
@allure.title("手机号超长时新增应失败")
def test_create_user_phone_too_long(token):
    resp = create_user(token, "测试", "1" * 50)
    assert resp.status_code == 400, f"实际 {resp.status_code}"



@allure.feature("用户模块")
@allure.story("异常场景-参数校验")
@allure.title("用户名为空时新增失败，返回400")
def test_create_user_empty_username(token):
    resp = create_user(token, "", "13800138000")
    assert resp.status_code == 400, f"实际 {resp.status_code}"


@pytest.mark.xfail(reason="缺陷BUG-002：用户名未做长度校验", strict=False)
@allure.feature("用户模块")
@allure.story("异常场景-参数校验")
@allure.title("用户名超长时新增应失败")
def test_create_user_username_too_long(token):
    resp = create_user(token, "张" * 100, "13800138000")
    assert resp.status_code == 400, f"实际 {resp.status_code}"


@pytest.mark.xfail(reason="缺陷BUG-002：手机号为空未校验", strict=False)
@allure.feature("用户模块")
@allure.story("异常场景-参数校验")
@allure.title("手机号为空时新增应失败")
def test_create_user_empty_phone(token):
    resp = create_user(token, "测试", "")
    assert resp.status_code == 400, f"实际 {resp.status_code}"






























