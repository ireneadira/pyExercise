from pyecharts.components import *
from pyecharts.options import *
from pyecharts.globals import *
from pyecharts.charts import *
from pyecharts import options as opts


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
