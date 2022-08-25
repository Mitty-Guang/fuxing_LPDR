from templates.config import conn
cur = conn.cursor()
def add_user(username,password):
    sql="INSERT INTO user(userid,password) VALUES('%s','%s')" %(username,password)
    conn.ping(reconnect=True)
    cur.execute(sql)
    conn.commit()

def check_password(password,password2):
    if password==password2:
        return True
    else:
        return  False
