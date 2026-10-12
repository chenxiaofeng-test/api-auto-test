import sqlite3
from config.settings import DB_PATH

def query_one(sql, params):
    """查数据库，返回结果列表（查不到就是空列表）"""
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute(sql, params).fetchall()
    conn.close()
    return rows