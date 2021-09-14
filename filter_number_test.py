import pandas as PD
import re
import redis
import pymysql
import Exercise.testProject

# sheet1 = PD.read_excel('D:/Documents/Rep_Data/7.27/7.27拼多多数据(全部).xlsx', names=['销量'])
# print(sheet1)

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

def deal_sale_volume(sale_volume):
    if sale_volume != '':
        if '万' in sale_volume:
            sale_volume = re.findall('(\d+(\.\d+)?)', sale_volume)
            sale_volume = int(float(sale_volume[0][0]) * 10000)
        else:
            sale_volume = re.findall('(\d+(\.\d+)?)', sale_volume)
            sale_volume = sale_volume[0][0]
        return sale_volume

def update_2_db(idnum, sales_volume):
    sql_up = f'''UPDATE pdd_rep SET sales_volume={sales_volume} WHERE ID={idnum}'''
    cur = conn.cursor()
    cur.execute(sql_up)
    conn.commit()
    cur.close()

if __name__ == '__main__':
    # list_str = ''''''
    # mds_name_list = list_str.split('\n')
    # # mds_name_list = list(set(mds_name_list)) # 去重功能
    # # mds_name_list.reverse()
    # for i in mds_name_list:
    #     sv = deal_sale_volume(i)
    #     print(sv)
    Exercise.testProject.watch_xs()


