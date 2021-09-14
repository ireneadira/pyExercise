# -*- coding:utf-8 -*-
import time
import redis
import random
import pymysql

dbConn = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': 'rootroot',
    'db': 'analyze_db',
    'charset': 'utf8'
    }

def push_from_list():
    r = redis.Redis(host='127.0.0.1', port=6379, decode_responses=True)
    mds_name_list = '''
'''
    emoji_list = mds_name_list.split('\n')
    # emoji_list = list(set(emoji_list)) # 去重功能
    # mds_name_list.reverse()
    for i in emoji_list:
        r.rpush('calc_num', i)
        print(i)
    print('PUSH Data : ' + str(len(emoji_list)))

def push_one(redis_name, value):
    r = redis.Redis(host='127.0.0.1', port=6379, decode_responses=True)
    r.lpush(redis_name, value)
    print('PUSH COMPLETED : ' + value)

def push_from_mysql():
    sql_get = '''SELECT CONCAT(address_provincial, address_city, address_area) FROM tb_address WHERE lat IS NULL GROUP BY CONCAT(address_provincial, address_city, address_area)'''
    conn = pymysql.connect(**dbConn)
    r = redis.Redis(host='127.0.0.1', port=6379, decode_responses=True)
    cur = conn.cursor()
    cur.execute(sql_get)
    msg = cur.fetchall()
    cur.close()
    conn.close()
    for i in msg:
        r.lpush('location', i[0])
        print(i[0])
    print('PUSH ALL COMPLETED XD')


if __name__ == '__main__':
    start_time = time.time()
    push_from_list()
    # push_one('nmpa_id', '192000')
    # push_from_mysql()
    print('Spend Time Is : ' + str(time.time()-start_time))