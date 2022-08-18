import  pymysql
def create_db():
    conn = pymysql.connect(host="localhost", user="lqw", password="woyaoshang600fen", charset="utf8")
    cur = conn.cursor()
    sql="drop database if exists flask"
    cur.execute(sql)
    sql="create database flask"
    cur.execute(sql)
    sql="use flask"
    cur.execute(sql)
    sql="drop table if exists user; "
    cur.execute(sql)
    sql="drop table if exists record;"
    cur.execute(sql)
    sql="create table user( "+"userid varchar(10),"+"password varchar(10),"+"primary key(userid));"
    cur.execute(sql)
    sql="create table record(carID varchar(15),create_time timestamp not null default CURRENT_TIMESTAMP COMMENT '创建时间',update_time timestamp not null default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP COMMENT '更新时间',primary key(carID));"
    cur.execute(sql)



