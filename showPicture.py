import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# 读取图片
lena = mpimg.imread('J:/webShotImg/7/6/6/IMG_www.76665359.com_20191010085754.png')
# 调整显示框名字 大小
plt.figure('Bangde',figsize=(10, 6))
# 调整显示位置
mngr = plt.get_current_fig_manager()
mngr.window.wm_geometry("+0+0")
# 设置显示
plt.imshow(lena)
# 关闭横纵坐标
plt.axis('off')
# 铺满显示
plt.gca().xaxis.set_major_locator(plt.NullLocator())
plt.gca().yaxis.set_major_locator(plt.NullLocator())
plt.subplots_adjust(top=1,bottom=0,left=0,right=1,hspace=0,wspace=0)
# 开始绘画
plt.draw()
# 显示 如果不加pause会出错 = =
plt.pause(3)
# 关闭
plt.close()

# https://blog.csdn.net/baidu_36669549/article/details/91046029
# https://blog.csdn.net/ygfrancois/article/details/85268982