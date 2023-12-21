from templates.config import conn
cur = conn.cursor()
def is_exist_record(carID):
    sql="SELECT* FROM record WHERE carID='%s' " %(carID)
    conn.ping(reconnect=True)
    cur.execute(sql)
    result = cur.fetchall()
    if (len(result) == 0):
        return False
    else:
        return True

def insert_record(carID,province):
    sql="insert into record(carID,province,in_time) values('%s','%s',NOW())" %(carID,province)
    conn.ping(reconnect=True)
    cur.execute(sql)
    conn.commit()

def update_record(carID):
    sql="update record set out_time=NOW() where carID='%s'" %(carID)
    conn.ping(reconnect=True)
    cur.execute(sql)
    conn.commit()

def count_province_car_number():
    sql="select province,count(*) as num from record group by province"
    conn.ping(reconnect=True)
    cur.execute(sql)
    result = cur.fetchall()
    table_list=[]
    for r in result:
        table_list.append(list(r))

    return  list(table_list)#返回（省份，数量）元组列表

def check_in_time(carID):
    sql="select in_time from record where carID='%s'"%(carID)
    conn.ping(reconnect=True)
    cur.execute(sql)
    result = cur.fetchall()
    return result

def check_out_time(carID):
    sql = "select out_time from record where carID='%s'" % (carID)
    conn.ping(reconnect=True)
    cur.execute(sql)
    result = cur.fetchall()
    return result

# if __name__ =='__main__':
#     x=count_province_car_number()
#     print(x)