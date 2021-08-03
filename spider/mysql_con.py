import  pymysql
def get_conn():
    conn = pymysql.connect( #连接数据库
        host="1.117.231.72",
        user="beerer",
        password="QWEqwe123",
        db="bidding",
        charset="utf8",
        port=3306,
    )
    # 创建游标：
    cursor = conn.cursor()
    return conn, cursor

def close_conn(conn, cursor): #关闭数据库连接
    if cursor:
        cursor.close()
    if conn:
        conn.close()