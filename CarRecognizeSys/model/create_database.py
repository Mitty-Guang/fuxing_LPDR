import  pymysql
def create_db():
    conn = pymysql.connect(host="localhost", user="root", password="cgafd5967421", charset="utf8")
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
    sql="create table record(carID varchar(15),province varchar(10),in_time datetime,out_time datetime,primary key(carID));"
    cur.execute(sql)



