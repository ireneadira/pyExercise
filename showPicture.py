import matplotlib.pyplot as plt # plt 用于显示图片
import matplotlib.image as mpimg # mpimg 用于读取图片
 
lena = mpimg.imread('picDir') # 读取和代码处于同一目录下的 lena.png
# 此时 lena 就已经是一个 np.array 了，可以对它进行任意处理
# lena.shape #(512, 512, 3)
 
plt.imshow(lena) # 显示图片
plt.axis('off') # 不显示坐标轴
plt.draw()
plt.pause(3)
plt.close()

# 原网址: 1: https://www.cnblogs.com/lantingg/p/9259840.html 2: https://blog.csdn.net/qq_36248632/article/details/90321044