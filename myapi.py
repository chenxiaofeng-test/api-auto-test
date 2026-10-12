import sqlite3
import uvicorn
from fastapi import FastAPI, HTTPException, Header

app = FastAPI(title="练手API")
DB = "test.db"
VALID_TOKEN = "abc123"      # 模拟：登录成功后拿到的令牌


def get_conn():
    return sqlite3.connect(DB)


def init_db():
    conn = get_conn()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            phone TEXT
        )
    """)
    conn.execute(
        "INSERT OR IGNORE INTO users (id, username, phone) VALUES (1,'admin','13800000000')")
    conn.commit()
    conn.close()


def check_token(token):
    if token != VALID_TOKEN:
        raise HTTPException(status_code=401, detail="token无效或已过期")


@app.post("/api/login")
def login(body: dict):
    username = body.get("username")
    password = body.get("password")
    if not username or not password:
        raise HTTPException(status_code=400, detail="用户名和密码不能为空")
    if username == "admin" and password == "123456":
        return {"code": 200, "msg": "登录成功", "data": {"token": VALID_TOKEN}}
    return {"code": 401, "msg": "用户名或密码错误"}


@app.get("/api/users")
def list_users(page: int = 1, size: int = 10, token: str = Header(None)):
    check_token(token)
    conn = get_conn()
    rows = conn.execute(
        "SELECT id, username, phone FROM users LIMIT ? OFFSET ?",
        (size, (page - 1) * size)).fetchall()
    conn.close()
    return {
        "code": 200,
        "msg": "success",
        "data": {"total": len(rows), "list": [{"id": r[0], "username": r[1], "phone": r[2]} for r in rows]}
    }


@app.post("/api/users")
def create_user(body: dict, token: str = Header(None)):
    check_token(token)
    username = body.get("username")
    if not username:
        raise HTTPException(status_code=400, detail="用户名不能为空")
    conn = get_conn()
    cur = conn.execute("INSERT INTO users (username, phone) VALUES (?, ?)",
                       (username, body.get("phone")))
    conn.commit()
    new_id = cur.lastrowid
    conn.close()
    return {"code": 200, "msg": "新增成功", "data": {"id": new_id}}


@app.delete("/api/users/{user_id}")
def delete_user(user_id: int, token: str = Header(None)):
    check_token(token)
    conn = get_conn()
    cur = conn.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    changed = cur.rowcount
    conn.close()
    if changed == 0:
        raise HTTPException(status_code=404, detail="用户不存在")
    return {"code": 200, "msg": "删除成功"}


if __name__ == "__main__":
    init_db()
    uvicorn.run(app, host="127.0.0.1", port=8880)