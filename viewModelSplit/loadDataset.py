from pyecharts.globals import ThemeType
from pandas import DataFrame
from .commDB import *

LAST_DATA_TIME = query_mysql_reptile('SELECT update_time FROM pdd_rep_price ORDER BY ID DESC LIMIT 1')[0][0]

# 数据可视化 数据展示页面

# 查询预加载的字典
shop_name_list = ['jkd', 'qjd', 'jd']
table_headers = ["商品名称", "SKU_ID", "销量", "销售额", "毛利润"]
query_data_set = {'OTC':[13780, 13781, 13782, 13783, 13784, 13785, 13786, 13787, 13788, 13789, 13790, 13791, 13792, 13793, 13794, 13795],
'RX-20':[18463, 18398, 18465, 18420, 18416, 18365, 18459, 18429, 18453, 18384, 18364, 18813, 18373, 18462, 18353, 18391, 18366, 18470, 18456, 18467],
'RX-40':[18413, 18435, 18450, 18369, 18452, 18437, 18376, 18392, 18393, 18395, 18375, 18431, 18468, 18458, 18410, 18481, 18352, 18408, 18379, 18464],
'RX-60':[18368, 18460, 18367, 18400, 18397, 18351, 18455, 18424, 18381, 18466, 18457, 18403, 18448, 18402, 18399, 18389, 18412, 18374, 18407, 18423],
'RX-80':[18428, 18444, 18439, 18422, 18480, 18380, 18469, 18451, 18442, 18405, 18425, 18432, 18390, 18415, 18427, 18447, 18419, 18385, 18418, 18361],
'RX-100':[18433, 18445, 18414, 18371, 18362, 18372, 18356, 18386, 18406, 18438, 18387, 18382, 18446, 18377, 18360, 18358, 18474, 18434, 18357, 18478]}

theme_type_list = [ThemeType.LIGHT, ThemeType.MACARONS, ThemeType.ROMA, ThemeType.SHINE, ThemeType.WALDEN, ThemeType.WESTEROS, ThemeType.WHITE, ThemeType.WONDERLAND]

# 查询函数 返回查询对象
def query_refresh_data(sql_select):
    conn = pymysql.connect(**dbConn)
    cur = conn.cursor()
    cur.execute(sql_select)
    data_set = cur.fetchall()
    cur.close()
    conn.close()
    return data_set

# 获取所有列表写入本地
def get_dataset_list(requests):
    # 地图渲染
    location_list, quantity_area_list, lng_list, lat_list = [], [], [], []  # 区级别地区, 区销售量数量, 经度, 纬度
    sql_map = f'''SELECT area, SUM(quantity), lng, lat FROM location_dataset WHERE lng IS NOT NULL GROUP BY area'''
    data_set_map_display = query_refresh_data(sql_map)
    for lo, qu_area, lng, lat in data_set_map_display:
        location_list.append(lo)
        quantity_area_list.append(int(qu_area)) # Decimal -> Int
        lng_list.append(lng)
        lat_list.append(lat)
    # 饼图渲染
    province_list, quantity_pro_list = [], [] # 省级别地区, 省销售数量
    sql_pie = f'''SELECT province, SUM(quantity) AS num FROM location_dataset GROUP BY province ORDER BY num DESC'''
    data_set_pie_display = query_refresh_data(sql_pie)
    for pr, qu_pro in data_set_pie_display:
        province_list.append(pr)
        quantity_pro_list.append(int(qu_pro))
    province_list_2101, quantity_pro_list_2101 = [], [] # 省级别地区, 省销售数量
    sql_pie = f'''SELECT province, SUM(quantity) AS num FROM location_dataset WHERE ins_date BETWEEN '2021-01-01' AND '2021-01-31' GROUP BY province ORDER BY num DESC'''
    data_set_pie_display = query_refresh_data(sql_pie)
    for pr, qu_pro in data_set_pie_display:
        province_list_2101.append(pr)
        quantity_pro_list_2101.append(int(qu_pro))
    province_list_2102, quantity_pro_list_2102 = [], [] # 省级别地区, 省销售数量
    sql_pie = f'''SELECT province, SUM(quantity) AS num FROM location_dataset WHERE ins_date BETWEEN '2021-02-01' AND '2021-02-28' GROUP BY province ORDER BY num DESC'''
    data_set_pie_display = query_refresh_data(sql_pie)
    for pr, qu_pro in data_set_pie_display:
        province_list_2102.append(pr)
        quantity_pro_list_2102.append(int(qu_pro))
    # 双柱形图渲染
    for shop_name in shop_name_list:
        date_list, sales_list, profit_list = [], [], []
        sales_list_tmp, profit_list_tmp = [], []
        sql_dou_bar_weeks = f'''SELECT DATE_FORMAT(pay_time,'%Y%U') weeks,SUM(money), SUM(profit) FROM calc_tb_main_{shop_name} GROUP BY weeks ORDER BY weeks'''
        sql_dou_bar_month = f'''SELECT DATE_FORMAT(pay_time,'%Y%m') mont,SUM(money), SUM(profit) FROM calc_tb_main_{shop_name} GROUP BY mont ORDER BY mont'''
        data_set_duo_bar_display_w = query_mysql_analyze(sql_dou_bar_weeks)
        data_set_duo_bar_display_m = query_mysql_analyze(sql_dou_bar_month)
        # 周
        # for week, w_money, w_profit in data_set_duo_bar_display_w:
        #     # weeks_date = Week(int(week[:4]), int(week[-2:])).sunday().strftime('%Y-%m-%d') # 转换周为具体日期
        #     date_list.append(week)
        #     sales_list_tmp.append(int(w_money))
        #     profit_list_tmp.append(int(w_profit))
        # for i, j in zip(profit_list_tmp, sales_list_tmp):
        #     dic_pr = {"value": i, "percent": i / j}
        #     profit_list.append(dic_pr)
        #     dic_sl = {"value": j, "percent": j / j} if (i < 0) else {"value": j, "percent": (j - i) / j}
        #     sales_list.append(dic_sl)
        # 月
        for month, m_money, m_profit in data_set_duo_bar_display_m:
            date_list.append(month)
            sales_list_tmp.append(int(m_money))
            profit_list_tmp.append(int(m_profit))
        for i, j in zip(profit_list_tmp, sales_list_tmp):
            dic_pr = {"value": i, "percent": i / j}
            profit_list.append(dic_pr)
            dic_sl = {"value": j, "percent": j / j} if (i < 0) else {"value": j, "percent": (j - i) / j}
            sales_list.append(dic_sl)
    # 表格图渲染
    sql_query_sales = f'''SELECT goods_name, SKU_code, COUNT(SKU_code), SUM(money), SUM(profit) FROM calc_tb_main_{shop_name} GROUP BY SKU_code ORDER BY COUNT(SKU_code) DESC'''
    sql_query_profit = f'''SELECT goods_name, SKU_code, COUNT(SKU_code), SUM(money), SUM(profit) FROM calc_tb_main_{shop_name} GROUP BY SKU_code ORDER BY SUM(profit) DESC'''
    cursor = connection.cursor()
    cursor.execute(sql_query_sales)
    data_set_query_shop_sales = DataFrame(list(cursor.fetchall())).values.tolist()
    cursor.execute(sql_query_profit)
    data_set_query_shop_profit = DataFrame(list(cursor.fetchall())).values.tolist()
    cursor.close()
    # 玫瑰图渲染
    departments_list_key = []
    proportion_sales_list = []
    sql_rose = f'''SELECT cat_name, SUM(sales_tip) FROM (pdd_rep_goods INNER JOIN pdd_goods_cats ON pdd_rep_goods.cat_id = pdd_goods_cats.cat_id ) INNER JOIN pdd_rep_price ON pdd_rep_goods.pdd_inner_code = pdd_rep_price.pdd_inner_code WHERE goods_comm<>'' AND update_time='{LAST_DATA_TIME}' AND pdd_rep_goods.cat_id IN (13780, 13781, 13782, 13783, 13784, 13785, 13786, 13787, 13788, 13789, 13790, 13791, 13792, 13793, 13794, 13795) GROUP BY cat_name ORDER BY SUM(sales_tip) DESC'''
    sum_data = query_refresh_data(sql_rose)
    for department, proportion in sum_data:
        departments_list_key.append(department)
        proportion_sales_list.append(int(proportion))
    # 多柱形图渲染 (pdd药品销量)
    departments_name_list, medicine_name_list, medicine_sales_list, medicine_value_list = [], [], [], []
    department_list = query_data_set.values()
    for multiple_department_list in department_list:
        for departments_id in multiple_department_list:
            detaile_medicine_name_list, detaile_medicine_sales_list, detaile_medicine_value_list = [], [], []
            sql_bar = f'''SELECT goods_comm, SUM(sales_tip), SUM(sales_tip * price) FROM (pdd_rep_goods INNER JOIN pdd_goods_cats ON pdd_rep_goods.cat_id = pdd_goods_cats.cat_id) INNER JOIN pdd_rep_price ON pdd_rep_goods.pdd_inner_code = pdd_rep_price.pdd_inner_code WHERE goods_comm<>'' AND update_time='{LAST_DATA_TIME}' AND pdd_rep_goods.cat_id={departments_id} AND sales_tip>0 GROUP BY goods_comm ORDER BY SUM(sales_tip) DESC'''
            mds_sv_data = query_refresh_data(sql_bar)
            for medicine, sales_volume, sales_value in mds_sv_data:
                detaile_medicine_name_list.append(medicine)
                detaile_medicine_sales_list.append(int(sales_volume))
                detaile_medicine_value_list.append(sales_value)
            departments_name = query_mysql_reptile('SELECT cat_name FROM pdd_goods_cats WHERE cat_id={}'.format(departments_id))[0][0]
            departments_name_list.append(departments_name)
            medicine_name_list.append(detaile_medicine_name_list)
            medicine_sales_list.append(detaile_medicine_sales_list)
            medicine_value_list.append(detaile_medicine_value_list)
    # 写入本地作为缓存
    index_list = ['location_list', 'quantity_area_list', 'lng_list', 'lat_list', 'province_list', 'quantity_pro_list', 'province_list_2101', 'quantity_pro_list_2101', 'province_list_2102', 'quantity_pro_list_2102', 'date_list', 'sales_list', 'profit_list', 'data_set_query_shop_sales', 'data_set_query_shop_profit', 'departments_list', 'proportion_sales_list', 'departments_name_list', 'medicine_name_list', 'medicine_sales_list', 'medicine_value_list']
    all_list = [location_list, quantity_area_list, lng_list, lat_list, province_list, quantity_pro_list, province_list_2101, quantity_pro_list_2101, province_list_2102, quantity_pro_list_2102, date_list, sales_list, profit_list, data_set_query_shop_sales, data_set_query_shop_profit, departments_list_key, proportion_sales_list, departments_name_list, medicine_name_list, medicine_sales_list, medicine_value_list]
    data_set_display = dict(zip(index_list, all_list))
    with open('display_Dataset.json', 'w') as f:
        f.write(str(data_set_display))
    return render(requests, 'search_app/showUpdateDataset.html', {'data_set_display': data_set_display})