# -*- coding:utf-8 -*-
import redis
import pymysql

dbConn = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': 'rootroot',
    'db': 'reptile_db',
    'charset': 'utf8'
    }
conn = pymysql.connect(**dbConn)
r = redis.Redis(host='127.0.0.1', port=6379, decode_responses=True)
nmpa_sure_list = r.lrange('nmpa_null', 0, -1)

def query_exist_nmpa(nmpa_id):
    query_sql = '''SELECT nmpa_id FROM nmpa_rep WHERE nmpa_id={}'''.format(nmpa_id)
    cur = conn.cursor()
    cur.execute(query_sql)
    result = cur.fetchone()
    cur.close()
    if result is None and str(nmpa_id) not in r.lrange('nmpa_null', 0, -1):
        return 1
    else:
        return 0


if __name__ == '__main__':
    for i in range(21, 198517):
        if query_exist_nmpa(i):
            print(i)
    r.close()
    conn.close()

