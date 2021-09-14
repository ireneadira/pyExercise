# encoding:utf-8
from django.shortcuts import render, HttpResponse
from pyecharts.components import *
from pyecharts.options import *
from pyecharts.globals import *
from pyecharts.charts import *
from pyecharts import options as opts
from django.db import connection
from pandas import DataFrame
from decimal import Decimal # 有用
from io import BytesIO
import pymysql, xlwt


# Create your views here.

# mysql连接参数
dbConn = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': 'rootroot',
    'db': 'reptile_db',
    'charset': 'utf8'
}

# 功能: 跳转到自定义的404界面 DEBUG:参数需要设置为True
# 返回: 404页面
def page_not_found(request, exception):
    return render(request, '404.html')
'''====================================================================================================================='''

def testFunc(request):
    # Create your views here.
    # trans_date = time.strftime('%Y-%m-%d', time.localtime())
    # time_stamp = int(time.mktime(time.strptime(trans_date, "%Y-%m-%d")))
    if request.method == 'GET':
        sql_get = f'''SELECT cat_name AS '商品分类', pdd_rep_goods.pdd_inner_code AS '商品内码', prescription AS '处方类型', goods_name AS '药品名称', price AS '药品价格', sales_tip AS '药品销量', goods_brand AS '品牌', goods_comm AS '通用名称', goods_spec AS '药品规格', manufacturer AS '生产厂家', update_time AS '更新时间', mall_name AS '店铺名称', goods_image_url AS '药品主图', goods_desc AS '药品描述' FROM ( pdd_rep_goods INNER JOIN pdd_goods_cats ON pdd_rep_goods.cat_id = pdd_goods_cats.cat_id ) INNER JOIN pdd_rep_price ON pdd_rep_goods.pdd_inner_code = pdd_rep_price.pdd_inner_code WHERE update_time='{LAST_DATA_TIME}' LIMIT 100;'''  # 每日采集数据
        sql_count = f'''SELECT count(*) FROM pdd_rep_price WHERE update_time='{LAST_DATA_TIME}';'''
        data, data_volume = query_mysql_reptile(sql_get=sql_get), query_mysql_reptile(sql_count)[0][0]
        return render(request, 'search_app/testPage.html', {'data': data[:100], 'data_volume': data_volume})
    else:
        data_set = request.POST['dataset_area']
        first_data = data_set.split('\r\n')[0]
        judge_flg = len(first_data.split(' '))
        if judge_flg == 1:
            query_data = tuple(data_set.split('\r\n'))
            query_data = str(query_data).replace(", '')", ')').replace("',)", "')")
            sql_get = f'''SELECT cat_name AS '商品分类', pdd_rep_goods.pdd_inner_code AS '商品内码', prescription AS '处方类型', goods_name AS '药品名称', price AS '药品价格', sales_tip AS '药品销量', goods_brand AS '品牌', goods_comm AS '通用名称', goods_spec AS '药品规格', manufacturer AS '生产厂家', update_time AS '更新时间', mall_name AS '店铺名称', goods_image_url AS '药品主图', goods_desc AS '药品描述' FROM (pdd_rep_goods INNER JOIN pdd_goods_cats ON pdd_rep_goods.cat_id = pdd_goods_cats.cat_id ) INNER JOIN pdd_rep_price ON pdd_rep_goods.pdd_inner_code = pdd_rep_price.pdd_inner_code WHERE goods_comm in {query_data} GROUP BY pdd_rep_goods.pdd_inner_code;'''
            sql_count = f'''SELECT COUNT(*) FROM (SELECT DISTINCT pdd_rep_goods.pdd_inner_code AS 'TBTEST' FROM (pdd_rep_goods INNER JOIN pdd_goods_cats ON pdd_rep_goods.cat_id = pdd_goods_cats.cat_id ) INNER JOIN pdd_rep_price ON pdd_rep_goods.pdd_inner_code = pdd_rep_price.pdd_inner_code WHERE goods_comm in {query_data}) AS TBTEST;'''
        elif judge_flg == 2:
            goods_brand, goods_comm = data_set.split(' ')
            sql_get = f'''SELECT cat_name AS '商品分类', pdd_rep_goods.pdd_inner_code AS '商品内码', prescription AS '处方类型', goods_name AS '药品名称', price AS '药品价格', sales_tip AS '药品销量', goods_brand AS '品牌', goods_comm AS '通用名称', goods_spec AS '药品规格', manufacturer AS '生产厂家', update_time AS '更新时间', mall_name AS '店铺名称', goods_image_url AS '药品主图', goods_desc AS '药品描述' FROM (pdd_rep_goods INNER JOIN pdd_goods_cats ON pdd_rep_goods.cat_id = pdd_goods_cats.cat_id ) INNER JOIN pdd_rep_price ON pdd_rep_goods.pdd_inner_code = pdd_rep_price.pdd_inner_code WHERE goods_brand='{goods_brand}' AND goods_comm='{goods_comm}' GROUP BY pdd_rep_goods.pdd_inner_code;'''
            sql_count = f'''SELECT COUNT(*) FROM (SELECT DISTINCT pdd_rep_goods.pdd_inner_code AS 'TBTEST' FROM (pdd_rep_goods INNER JOIN pdd_goods_cats ON pdd_rep_goods.cat_id = pdd_goods_cats.cat_id ) INNER JOIN pdd_rep_price ON pdd_rep_goods.pdd_inner_code = pdd_rep_price.pdd_inner_code WHERE goods_brand='{goods_brand}' AND goods_comm='{goods_comm}') AS TBTEST;'''
        data, data_volume = query_mysql_reptile(sql_get=sql_get), query_mysql_reptile(sql_count)[0][0]
        return render(request, 'search_app/testPage.html', {'data': data, 'data_volume': data_volume})
        # return HttpResponse(sql_get + '<br><br><br>' + sql_count)



# 功能 测试界面 里面随便写点啥
# 返回 返回测试界面
# def testFunc(request):
    # return HttpResponse('It is a test ...')
    # 1 加载模板文件 模板对象
    # temp = loader.get_template('search_app/index.html') # 返回模板对象
    # 2 定义模板上下文 给模板传递数据
    # context = RequestContext(request, {}) # {}要传递的数据放在这个字典中
    # context.push(locals())
    # 3 模板渲染 使用的变量 语句 替换掉  产生一个标准的HTML内容
    # res_html = temp.render(context=locals(), request=request)
    # 4 返回给浏览器
    # return HttpResponse(res_html)

    # if request.method=='GET':
    #     encrypt_code = request.GET.get('encrypt', default='sherlock')
    #     encrypt_code = hashlib.md5(encrypt_code.encode()).hexdigest().upper()
    # elif request.method=='POST':
    #     encrypt_code = request.POST.get('encrypt', default='sherlock')
    #     encrypt_code = hashlib.md5(encrypt_code.encode()).hexdigest().upper()
    # return render(request, 'search_app/testPage.html', {'data': encrypt_code})

'''====================================================================================================================='''


# 功能 进入首页 搜索界面
# 返回 搜索界面 index界面
def enterSearchpage(request):
    return render(request, 'search_page/index.html')

# 功能 从搜索界面传参接受 进入数据库进行模糊查询 查询表: search_app_tb_goods
# 返回 返回搜索结果界面
def showGoodsMsg(request):
    search_key = request.GET['search']
    if search_key == '':
        sql_get = '''SELECT search_app_tb_goods.goods_name, search_app_tb_goods.goods_spec, search_app_tb_price.tax_cost, search_app_tb_goods.price_flag, search_app_tb_price.price_guid, search_app_tb_supplier.supp_name, search_app_tb_price.update_time, search_app_tb_goods.register_number, search_app_tb_price.goods_id, search_app_tb_goods.other_msg FROM (search_app_tb_supplier INNER JOIN search_app_tb_price ON search_app_tb_supplier.supp_id = search_app_tb_price.supp_id) INNER JOIN search_app_tb_goods ON (search_app_tb_goods.goods_id = search_app_tb_price.goods_id) AND (search_app_tb_supplier.supp_id = search_app_tb_goods.supp_id) WHERE search_app_tb_price.id IN (SELECT MAX(id) FROM search_app_tb_price WHERE goods_id IN (SELECT goods_id FROM search_app_tb_goods WHERE price_flag > 0 AND update_time='2021-07-15') GROUP BY goods_id) ORDER BY price_flag DESC'''
    else:
        sql_get = f"""SELECT search_app_tb_goods.goods_name, search_app_tb_goods.goods_spec, search_app_tb_price.tax_cost, search_app_tb_goods.price_flag, search_app_tb_price.price_guid, search_app_tb_supplier.supp_name, search_app_tb_price.update_time, search_app_tb_goods.register_number, search_app_tb_price.goods_id, search_app_tb_goods.other_msg FROM (search_app_tb_supplier INNER JOIN search_app_tb_price ON search_app_tb_supplier.supp_id = search_app_tb_price.supp_id) INNER JOIN search_app_tb_goods ON (search_app_tb_goods.goods_id = search_app_tb_price.goods_id) AND (search_app_tb_supplier.supp_id = search_app_tb_goods.supp_id) WHERE search_app_tb_price.id IN (SELECT MAX(id) FROM search_app_tb_price WHERE goods_id IN (SELECT goods_id FROM search_app_tb_goods WHERE goods_name like '%{search_key}%') GROUP BY goods_id) ORDER BY update_time DESC"""
    cursor = connection.cursor()
    cursor.execute(sql_get)
    data = cursor.fetchall()
    cursor.close()
    return render(request, 'search_app/showGoods.html', {'data': data})

# 功能 从搜索界面传入批准文号进行模糊查询 查询表: search_app_tb
# 返回 显示批准文号的界面
def showGoodsReg(request, register):
    sql_get = f"""SELECT search_app_tb_goods.goods_name, search_app_tb_goods.goods_spec, search_app_tb_price.tax_cost, search_app_tb_price.price_guid, search_app_tb_supplier.supp_name, search_app_tb_price.update_time, search_app_tb_goods.register_number, search_app_tb_price.goods_id FROM (search_app_tb_supplier INNER JOIN search_app_tb_price ON search_app_tb_supplier.supp_id = search_app_tb_price.supp_id) INNER JOIN search_app_tb_goods ON (search_app_tb_goods.goods_id = search_app_tb_price.goods_id) AND (search_app_tb_supplier.supp_id = search_app_tb_goods.supp_id) WHERE register_number='{register}' GROUP BY search_app_tb_price.goods_id ORDER BY update_time DESC"""
    cursor = connection.cursor()
    cursor.execute(sql_get)
    data = cursor.fetchall()
    cursor.close()
    return render(request, 'search_app/showRegister.html', {'data': data})

# 传入查询语句 返回查询对象
def query_mysql_analyze(sql_query):
    cur = connection.cursor()
    cur.execute(sql_query)
    data = cur.fetchall()
    cur.close()
    return data

# 功能: 查询爬虫库中的接口
# 返回: 返回查询数据data和data长度
def query_mysql_reptile(sql_get):
    conn = pymysql.connect(**dbConn)
    cursor = conn.cursor()
    cursor.execute(sql_get)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data

# 最后有数据的时间
LAST_DATA_TIME = query_mysql_reptile('SELECT update_time FROM pdd_rep_price ORDER BY ID DESC LIMIT 1')[0][0]

# 功能 从rep库中查询数据显示在界面上
# 返回 拼多多数据展示界面
# 参数 type:查询类型 这里是拼多多 export:是否导出
def showPddRep(request):
    if request.method == 'GET':
        search_type = request.GET.get('type')
        export = request.GET.get('export')
        # trans_date = time.strftime('%Y-%m-%d', time.localtime())
        # time_stamp = int(time.mktime(time.strptime(trans_date, "%Y-%m-%d")))
        if export == '0':
            if search_type == 'pdd':
                sql_get = f'''SELECT cat_name AS '商品分类', pdd_rep_goods.pdd_inner_code AS '商品内码', prescription AS '处方类型', goods_name AS '药品名称', price AS '药品价格', sales_tip AS '药品销量', goods_brand AS '品牌', goods_comm AS '通用名称', goods_spec AS '药品规格', manufacturer AS '生产厂家', update_time AS '更新时间', mall_name AS '店铺名称', goods_image_url AS '药品主图', goods_desc AS '药品描述' FROM ( pdd_rep_goods INNER JOIN pdd_goods_cats ON pdd_rep_goods.cat_id = pdd_goods_cats.cat_id ) INNER JOIN pdd_rep_price ON pdd_rep_goods.pdd_inner_code = pdd_rep_price.pdd_inner_code WHERE update_time='{LAST_DATA_TIME}' LIMIT 100;''' # 每日采集数据
                sql_count = f'''SELECT count(*) FROM pdd_rep_price WHERE update_time='{LAST_DATA_TIME}';'''
                data, data_volume = query_mysql_reptile(sql_get=sql_get), query_mysql_reptile(sql_count)[0][0]
                return render(request, 'search_app/showRepPdd.html', {'data': data[:100], 'data_volume': data_volume})
            elif search_type == 'jd':
                sql_get = f'''SELECT three_cat AS '三级目录', update_time AS '更新时间', goods_name AS '药品名称', price AS '药品价格', goods_brand AS '品牌', goods_comm AS '通用名称', goods_spec AS '药品规格', manufacturer AS '生产厂家', shop_name AS '店铺名称', sales_tip AS '药品销量', approval_number AS '批准文号', p.jd_inner_code AS '商品内码', details_msg AS '详细信息' FROM jd_rep_goods AS g INNER JOIN jd_rep_price AS p ON g.jd_inner_code=p.jd_inner_code WHERE update_time='{LAST_DATA_TIME}' LIMIT 100;'''
                sql_count = f'''SELECT count(*) FROM jd_rep_price WHERE update_time='{LAST_DATA_TIME}';'''
                data, data_volume = query_mysql_reptile(sql_get=sql_get), query_mysql_reptile(sql_count)[0][0]
                return render(request, 'search_app/showRepJd.html', {'data': data[:100], 'data_volume': data_volume})
        elif export == '1':
            if search_type == 'pdd':
                sql_get = f'''SELECT cat_name AS '商品分类', pdd_rep_goods.pdd_inner_code AS '商品内码', prescription AS '处方类型', goods_name AS '药品名称', price AS '药品价格', sales_tip AS '药品销量', goods_brand AS '品牌', goods_comm AS '通用名称', goods_spec AS '药品规格', manufacturer AS '生产厂家', update_time AS '更新时间', mall_name AS '店铺名称', goods_image_url AS '药品主图', goods_desc AS '药品描述' FROM ( pdd_rep_goods INNER JOIN pdd_goods_cats ON pdd_rep_goods.cat_id = pdd_goods_cats.cat_id ) INNER JOIN pdd_rep_price ON pdd_rep_goods.pdd_inner_code = pdd_rep_price.pdd_inner_code''' # 每日采集数据
                sql_get = sql_get + f''' WHERE update_time='{LAST_DATA_TIME}';''' # 过滤条件 导出数据
            elif search_type == 'jd':
                sql_get = '''SELECT three_cat AS '三级目录', update_time AS '更新时间', goods_name AS '药品名称', price AS '药品价格', goods_brand AS '品牌', goods_comm AS '通用名称', goods_spec AS '药品规格', manufacturer AS '生产厂家', shop_name AS '店铺名称', sales_tip AS '药品销量', approval_number AS '批准文号', p.jd_inner_code AS '商品内码', details_msg AS '详细信息' FROM jd_rep_goods AS g INNER JOIN jd_rep_price AS p ON g.jd_inner_code=p.jd_inner_code WHERE update_time='{trans_date}';'''
                sql_get = sql_get + f''' WHERE update_time='{LAST_DATA_TIME}';''' # 过滤条件 导出数据
            # resp = exportData(sql_get_sp=sql_get)
            # return resp
            return HttpResponse(f'<h1 style="text-align:center; color:red;">请联系电商部最角落那个人开启这个功能 <br/> <p style="color:white;">{sql_get}</p>')
    elif request.method == 'POST':
        data_set = request.POST['dataset_area']
        return HttpResponse(data_set)


# 功能 查询拼多多数据放入二进制流中
# 返回 二进制流Response对象 (.xls文件)
def exportData(sql_get_sp):
    sql_get = sql_get_sp
    conn = pymysql.connect(**dbConn)
    cursor = conn.cursor()
    cursor.execute(sql_get)
    fields = [field[0] for field in cursor.description]
    all_data = cursor.fetchall()
    cursor.close()
    conn.close()
    book = xlwt.Workbook()
    sheet = book.add_sheet('sheet1')
    for col, field in enumerate(fields):
        sheet.write(0, col, field)
    row = 1
    for data in all_data:
        for col, field in enumerate(data):
            sheet.write(row, col, field)
        row += 1
    sio = BytesIO()
    book.save(sio)
    sio.seek(0)
    response = HttpResponse(sio.getvalue(), content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=Pdd_Filter_Data.xls'
    response.write(sio.getvalue())
    return response


# 功能 数据可视化
# 返回 数据可视化的页面(单页面)
def displayAnaLine(request, gid):
    # 功能 获取信息显示在折线图上方
    # 返回 supplier:供应商名称层 mds_name:商品名称 mds_spec:商品规格
    sql_query_1 = f'''SELECT search_app_tb_supplier.supp_name, search_app_tb_goods.goods_name, search_app_tb_goods.goods_spec FROM (search_app_tb_supplier INNER JOIN search_app_tb_goods ON search_app_tb_supplier.supp_id = search_app_tb_goods.supp_id) WHERE search_app_tb_goods.goods_id={gid}'''
    supplier, mds_name, mds_spec = query_mysql_analyze(sql_query_1)[0]
    # 功能 获取折线图的 x轴数据(日期) y轴数据(价格)
    # 返回 日期列表 价格列表
    sql_query_2 = f'''SELECT search_app_tb_price.update_time, search_app_tb_price.tax_cost FROM (search_app_tb_supplier INNER JOIN search_app_tb_price ON search_app_tb_supplier.supp_id = search_app_tb_price.supp_id) INNER JOIN search_app_tb_goods ON (search_app_tb_goods.goods_id = search_app_tb_price.goods_id) AND (search_app_tb_supplier.supp_id=search_app_tb_goods.supp_id) WHERE search_app_tb_goods.goods_id={gid} ORDER BY search_app_tb_price.update_time ASC'''
    list_temp = DataFrame(list(query_mysql_analyze(sql_query_2)))
    date_list, pric_list = list_temp[0].tolist(), list_temp[1].tolist()
    # 获取所有数据集 开始渲染
    c = (
        Line()
            .add_xaxis(date_list)
            .add_yaxis(supplier, pric_list,
                linestyle_opts=opts.LineStyleOpts(color="#6699cc"),
                label_opts=opts.LabelOpts(is_show=True, position="bottom", color="#aabcfe", rotate = '-20'),
                markline_opts=opts.MarkLineOpts(data=[opts.MarkLineItem(type_="average", name="平均 Average")
                                                      # opts.MarkLineItem(type_="min", name="最小 Min Value"),
                                                      # opts.MarkLineItem(type_="max", name="最大 Max Value")
                                                      ],
                                                linestyle_opts=opts.LineStyleOpts(type_='dashed', color="rgba(235,85,128,0.87)"), is_silent=True))
            .set_global_opts(xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-20)),
                             title_opts=opts.TitleOpts(title=mds_name , pos_left='80%', subtitle=mds_spec)
        )
    )
    return HttpResponse(c.render_embed())


# 返回 数据可视化的页面(单页面) # jd pdd
def displayECLine(request, t_inner_id):
    query_type, inner_code = t_inner_id[0], t_inner_id[1:]
    if query_type=='P':
        sql_query_1 = f'''SELECT mall_name, goods_name, prescription FROM pdd_rep_goods WHERE pdd_inner_code='{inner_code}';'''
        sql_query_2 = f'''SELECT update_time, price FROM pdd_rep_price WHERE pdd_inner_code='{inner_code}';'''
    else:
        sql_query_1 = f'''SELECT shop_name, goods_name, three_cat FROM jd_rep_goods WHERE jd_inner_code='{inner_code}';'''
        sql_query_2 = f'''SELECT update_time, price FROM jd_rep_price WHERE jd_inner_code='{inner_code}';'''
    supplier, mds_name, mds_spec = query_mysql_reptile(sql_query_1)[0]
    list_temp = DataFrame(list(query_mysql_reptile(sql_query_2)))
    date_list, pric_list = list_temp[0].tolist(), list_temp[1].tolist()
    c = (
        Line()
            .add_xaxis(date_list)
            .add_yaxis(supplier, pric_list,
                linestyle_opts=opts.LineStyleOpts(color="#6699cc"),
                label_opts=opts.LabelOpts(is_show=True, position="bottom", color="#aabcfe", rotate = '-20'),
                markline_opts=opts.MarkLineOpts(data=[
                                                      opts.MarkLineItem(type_="average", name="平均 Average")
                                                      # opts.MarkLineItem(type_="min", name="最小 Min Value"),
                                                      # opts.MarkLineItem(type_="max", name="最大 Max Value")
                                                      ],
                                                linestyle_opts=opts.LineStyleOpts(type_='dashed', color="rgba(235,85,128,0.87)"), is_silent=True))
            .set_global_opts(xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-20)),
                             title_opts=opts.TitleOpts(title='\n' + mds_name , pos_left='10%', subtitle=mds_spec)
        )
    )
    return HttpResponse(c.render_embed())


# 测试 ### =============================================================================================================
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

# 销售热区地图
# 所需参数: 区地区列表 区地区销售数量列表 经度列表 纬度列表
def map_hot_display(location_list, quantity_list, lng_list, lat_list):
    g = Geo(init_opts=opts.InitOpts(width='1920px', height='800px', theme=ThemeType.INFOGRAPHIC))
    # 定义坐标对应的名称，添加到坐标库中 add_coordinate(name, lng, lat)
    for i, j, k in zip(location_list, lng_list, lat_list):
        g.add_coordinate(i, j, k)
    dataset_g = [list(z) for z in zip(location_list, quantity_list)]
    g.add_schema(maptype="china")
    g.add("热度分布", data_pair=dataset_g, type_=GeoType.HEATMAP)
    g.add("数据标识", data_pair=dataset_g, type_=GeoType.SCATTER, is_selected=False)
    g.set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    pieces = [
        {'max': 1, 'label': '0以下', 'color': '#50A3BA'},
        {'min': 1, 'max': 10, 'label': '1-10', 'color': '#3700A4'},
        {'min': 10, 'max': 100, 'label': '10-100', 'color': '#81AE9F'},
        {'min': 100, 'max': 1000, 'label': '100-1000', 'color': '#E2C568'},
        {'min': 1000, 'max': 2000, 'label': '1000-20000', 'color': '#FCF84D'},
        {'min': 2000, 'max': 3000, 'label': '2000-3000', 'color': '#DD0200'},
        {'min': 3000, 'max': 4000, 'label': '3000-4000', 'color': '#DD675E'},
        {'min': 4000, 'label': '4000以上', 'color': '#D94E5D'}  # 有下限无上限
    ]
    g.set_global_opts(
    visualmap_opts=opts.VisualMapOpts(max_=5000, is_piecewise=False, pieces=pieces),
    title_opts=opts.TitleOpts(title="RunDay"),
    )
    return g

# 销售区域占比饼图
# 所需参数: 省地区列表 省地区销售数量列表
def pie_per_local_display(province_list, quantity_list_a):
    dataset_p = [list(z) for z in zip(province_list, quantity_list_a)]
    p = (
        Pie(init_opts=opts.InitOpts(width='1920px', height='800px', theme=ThemeType.LIGHT))
            .add("城市占比",
                data_pair=dataset_p,
                radius="80%",
                center=["35%", "50%"],
                label_opts=opts.LabelOpts(is_show=False, position="center"),
            )
            .set_series_opts(
                tooltip_opts=opts.TooltipOpts(
                    trigger="item", formatter="{a} <br/>{b}: {c} ({d}%)"
                ),
                label_opts=opts.LabelOpts(formatter="{b}: {c} ({d}%)"),
            )
            .set_global_opts(
                legend_opts=opts.LegendOpts(type_="scroll", pos_left="80%", orient="vertical"),
                title_opts=opts.TitleOpts(title="RunDay")
        )
    )
    return p

# 销售科室占比饼图
# 所需参数: 销售科室列表 销售科室对应销量列表
def pie_rose_display(departments_list, departments_num_list):
    data_set_r = [list(z) for z in zip(departments_list, departments_num_list)]
    r = (
        Pie(init_opts=opts.InitOpts(width="1680px", height="880px", theme=ThemeType.WESTEROS))
            .add(
            "",
            data_pair=data_set_r,
            radius=["30%", "75%"],
            center=["35%", "50%"],
            # rosetype="area",
        )
            .set_series_opts(
            tooltip_opts=opts.TooltipOpts(
                trigger="item", formatter="{a} <br/>{b}: {c} ({d}%)"
            ),
            label_opts=opts.LabelOpts(formatter="{b}: {c} ({d}%)"),
        )
            .set_global_opts(title_opts=opts.TitleOpts(title="RunDay"),
                             toolbox_opts=opts.TooltipOpts())
    )
    return r

# 销售数据
# 所需参数: 周期列表(年+周形式) 销售量列表 毛利列表
def bar_sales_display(date_list, sales_list, profit_list):
    c = (
        Bar(init_opts=opts.InitOpts(width='1800px', height='700px', theme=ThemeType.LIGHT))
        .add_xaxis(date_list)
        .add_yaxis("毛利", profit_list, stack="stack1", category_gap="25%")
        .add_yaxis("销售额", sales_list, stack="stack1", category_gap="25%")
        .set_series_opts(
            label_opts=opts.LabelOpts(
                position="right",
                formatter=JsCode(
                    "function(x){return Number(x.data.percent * 100).toFixed() + '%';}"
                )
            )
        )
        .set_global_opts(
            toolbox_opts=opts.ToolboxOpts(),
            datazoom_opts=opts.DataZoomOpts(type_="inside")
        )
    )
    return c

# 销售表格数据
# 所需参数 表格表头 表格内容数据[[],[]] 表格标题
def table_Top20_display(headers, rows_data, title):
    table_obj = Table()
    table_obj.add(headers, rows_data)
    table_obj.set_global_opts(title_opts=ComponentTitleOpts(title=title))
    return table_obj

# 药品销量排行柱形图
# 所需参数: 详细分类(感冒发烧,减肥), 药品名称列表, 药品销量列表
def bar_medicine_display(subject, mds_list, sales_list, value_list):
    color_function = """
            function (params) {
                if (params.value > 0 && params.value <= 10) {
                    return 'DarkGray';
                } else if (params.value > 10 && params.value <= 100) {
                    return 'SpringGreen';
                } else if (params.value > 100 && params.value <= 1000) {
                    return 'LightBlue';
                } else if (params.value > 1000 && params.value <= 10000) {
                    return 'RoyalBlue';
                } else if (params.value > 10000 && params.value <= 100000) {
                    return 'Gold';
                } else if (params.value > 100000 && params.value <= 1000000) {
                    return 'Pink';
                } else if (params.value > 1000000 && params.value <= 10000000) {
                    return 'LightCoral';
                } else if (params.value > 10000000 && params.value <= 20000000) {
                    return 'DarkMagenta';
                }
                return 'Black';
            }
            """
    t = Timeline(init_opts=opts.InitOpts(width='1920px', height='800px'))
    for sub, mds, num, val in zip(subject, mds_list, sales_list, value_list):
        bar = (
            Bar()
                .add_xaxis(mds)
                .add_yaxis(sub + ' (销量)', num, itemstyle_opts=opts.ItemStyleOpts(color=JsCode(color_function)))
                .add_yaxis(sub + ' (销售额)', val, itemstyle_opts=opts.ItemStyleOpts(color=JsCode(color_function)), is_selected=False)
                .set_global_opts(title_opts=opts.TitleOpts("PDD {} 分类排序".format(sub)),
                                 datazoom_opts=opts.DataZoomOpts(type_="inside")
                )
            )
        t.add(bar, "{}".format(sub))
    return t


# 本地读取列表文件传参渲染并图形化
# 所需参数: 分析RT的请求
def draw_display_rt_page(requests):
    # 读数据
    f = open('display_Dataset.json')
    dict_dataset = eval(f.read())
    location_list, quantity_area_list, lng_list, lat_list = dict_dataset.get('location_list'), dict_dataset.get('quantity_area_list'), dict_dataset.get('lng_list'), dict_dataset.get('lat_list') # 地图所需数据集
    province_list, quantity_pro_list = dict_dataset.get('province_list'), dict_dataset.get('quantity_pro_list') # 饼图所需数据集
    province_list_2101, quantity_pro_list_2101 = dict_dataset.get('province_list_2101'), dict_dataset.get('quantity_pro_list_2101') # 饼图所需数据集 21年1月
    province_list_2102, quantity_pro_list_2102 = dict_dataset.get('province_list_2102'), dict_dataset.get('quantity_pro_list_2102') # 饼图所需数据集 21年2月
    date_list, sales_list, profit_list = dict_dataset.get('date_list'), dict_dataset.get('sales_list'), dict_dataset.get('profit_list') # 双柱形图所需数据集
    data_set_query_shop_sales, data_set_query_shop_profit, data_set_query_shop_loss = dict_dataset.get('data_set_query_shop_sales'), dict_dataset.get('data_set_query_shop_profit'), dict_dataset.get('data_set_query_shop_loss') # 利润分析表所需数据集
    # 传数据 渲染对象
    g_obj = map_hot_display(location_list, quantity_area_list, lng_list, lat_list)
    p_obj = pie_per_local_display(province_list, quantity_pro_list)
    p_obj_2101 = pie_per_local_display(province_list_2101, quantity_pro_list_2101)
    p_obj_2102 = pie_per_local_display(province_list_2102, quantity_pro_list_2102)
    dou_b_obj = bar_sales_display(date_list, sales_list, profit_list)
    shop_sales_tp20_obj = table_Top20_display(headers=table_headers, rows_data=data_set_query_shop_sales, title='销量排序')
    shop_profit_tp20_obj = table_Top20_display(headers=table_headers, rows_data=data_set_query_shop_profit, title='利润排序')
    # 渲染页面
    tab = Tab(page_title='RunDay Analyze')
    tab.add(g_obj, "全国分布图")
    tab.add(p_obj, "省级占比图")
    tab.add(p_obj_2101, "21.1 省级占比图")
    tab.add(p_obj_2102, "21.2 省级占比图")
    tab.add(dou_b_obj, "店铺分析图")
    tab.add(shop_sales_tp20_obj, "店铺销量排序")
    tab.add(shop_profit_tp20_obj, "店铺利润排序")
    return HttpResponse(tab.render_embed())


# 本地读取列表文件传参渲染并图形化
# 所需参数: 分析PDD的请求
def draw_display_pdd_page(requests):
    # 读数据
    f = open('display_Dataset.json')
    dict_dataset = eval(f.read())
    departments_list, proportion_sales_list = dict_dataset.get('departments_list'), dict_dataset.get('proportion_sales_list') # 玫瑰图所需数据集
    departments_name_list, medicine_name_list, medicine_sales_list, medicine_value_list = dict_dataset.get('departments_name_list'), dict_dataset.get('medicine_name_list'), dict_dataset.get('medicine_sales_list'), dict_dataset.get('medicine_value_list') # 科室柱形图所需数据集
    # 传数据 渲染对象
    r_obj = pie_rose_display(departments_list, proportion_sales_list)
    t_obj_cjb = bar_medicine_display(departments_name_list[:16], medicine_name_list[:16], medicine_sales_list[:16], medicine_value_list[:16])
    t_obj_mxb = bar_medicine_display(departments_name_list[16:36], medicine_name_list[16:36], medicine_sales_list[16:36], medicine_value_list[16:36])
    t_obj_nkzz = bar_medicine_display(departments_name_list[36:56], medicine_name_list[36:56], medicine_sales_list[36:56], medicine_value_list[36:56])
    t_obj_fkzz = bar_medicine_display(departments_name_list[56:76], medicine_name_list[56:76], medicine_sales_list[56:76], medicine_value_list[56:76])
    t_obj_pfjb = bar_medicine_display(departments_name_list[76:96], medicine_name_list[76:96], medicine_sales_list[76:96], medicine_value_list[76:96])
    t_obj_gtzz = bar_medicine_display(departments_name_list[96:116], medicine_name_list[96:116], medicine_sales_list[96:116], medicine_value_list[96:116])
    # 渲染页面
    tab = Tab(page_title='Pdd Analyze')
    tab.add(r_obj, "大类销量占比")
    tab.add(t_obj_cjb, "OTC")
    tab.add(t_obj_mxb, "RX TOP20")
    tab.add(t_obj_nkzz, "RX 20-40")
    tab.add(t_obj_fkzz, "RX 40-60")
    tab.add(t_obj_pfjb, "RX 60-80")
    tab.add(t_obj_gtzz, "RX 80-100")
    return HttpResponse(tab.render_embed())
