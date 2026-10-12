from common.request_client import client

def list_users(token):
    """查询用户列表"""
    return client.get("/api/users", headers={"token": token})

def create_user(token, username, phone):
    """新增用户"""
    return client.post("/api/users", json={"username": username, "phone": phone}, headers={"token": token})

def delete_user(token, user_id):
    """删除用户"""
    return client.delete(f"/api/users/{user_id}", headers={"token": token})
