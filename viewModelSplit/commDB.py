from django.db import connection
import pymysql

# 传入查询语句 返回查询对象 Django自带connection
def query_mysql_analyze(sql_query):
    cur = connection.cursor()
    cur.execute(sql_query)
    data = cur.fetchall()
    cur.close()
    return data

# 数据库连接参数
dbConn = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': 'rootroot',
    'db': 'reptile_db',
    'charset': 'utf8'
}
conn = pymysql.connect(**dbConn)

# 传入查询语句 返回查询对象 采集库查询
def query_mysql_reptile(sql_get):
    cursor = conn.cursor()
    cursor.execute(sql_get)
    data = cursor.fetchall()
    cursor.close()
    return data






