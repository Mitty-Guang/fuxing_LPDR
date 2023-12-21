from  templates.config import conn
cur = conn.cursor()
def check_user():
    sql = "SELECT userid FROM user"
    conn.ping(reconnect=True)
    cur.execute(sql)
    result = cur.fetchall()
    return result