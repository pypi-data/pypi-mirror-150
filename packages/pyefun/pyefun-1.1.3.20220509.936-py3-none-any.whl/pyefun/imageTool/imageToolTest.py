import unittest

from .imageTool import *
from .imageToolPIL import *


class TestCacheUtil(unittest.TestCase):

    def test_PIL(self):
        图片操作 = 图像操作PIL类().创建空白图片(100, 200, color=(255, 0, 0)).显示图片()
        # 图片操作 = 图像操作PIL类(r"9108efa6518a1fbadfa77047.jpeg")
        # 图片数据 = 图片操作.绘制点(10, 10).显示图片()
        # 图片数据 = 图片操作.绘制圆形(100, 100, 100).显示图片()
        # 图片数据 = 图片操作.绘制填充圆形(100, 100, 100).显示图片()
        # 图片数据 = 图片操作.剪裁(0, 0, 100, 100).保存为文件("test1.jpg").显示图片()
        # 图片数据 = 图片操作.剪裁(0, 0, 100, 100).二值化().显示图片()
        # 图片数据 = 图片操作.绘制矩形(0, 0, 100, 100).绘制文本汉字("123啊", 48, 48, (255, 0, 0)).显示图片()
        # 图片数据 = 图片操作.绘制填充矩形(0, 0, 100, 100, (255, 0, 0)).显示图片()
        # 图片数据 = 图片操作.绘制多边形([[0, 74], [200, 74], [300, 142], [0, 142]], (255, 0, 0)).显示图片()
        # 图片数据 = 图片操作.绘制填充多边形([[0, 74], [200, 74], [300, 142], [0, 142]], (255, 0, 0)).显示图片()
        # 图片数据 = 图片操作.二值化().显示图片()
        # 图片数据 = 图片操作.二值化()
        # print(图片数据.到base64())

        # 图像操作类2().加载图片从base64(图片数据.到base64()).显示图片()
        # 图片数据 = 图片操作.二值化(180)
        # 图片操作.二值化(127).颜色翻转().显示图片()
        # 图片操作.图像翻转左右().显示图片()
        # 图片操作.图像翻转上下().显示图片()
        # 图片操作.增强对比度().显示图片()
        # 图片操作.增强亮度().显示图片()
        # 图片操作.锐利度(0).显示图片()
        # 图片操作.高斯模糊(3).显示图片()
        #
        # 图片操作.边缘检测().显示图片()
        # 图片操作.轮廓().显示图片()

    def test_CV2(self):
        pass
        图片操作 = 图像操作类(r"9108efa6518a1fbadfa77047.jpeg")
        图片数据 = 图片操作.绘制点(10, 10).显示图片()
        # # 图片数据 = 图片操作.图像翻转上下().显示图片()
        # 图片数据 = 图片操作.图像翻转左右().显示图片()
        # print(图片数据)
        # 图像操作类().创建空白图片(100, 200, (255, 255, 255)).绘制文本汉字("哈哈哈", 0, 0).绘制点(50, 50, (255, 0, 0), 10).显示图片()

        # 图片数据 = 图片操作.剪裁(0, 0, 100, 100).保存为文件("test1.jpg").显示图片()
        # 图片数据 = 图片操作.剪裁(0, 0, 100, 100).二值化()
        # 图片数据 = 图片操作.绘制矩形(0, 0, 100, 100).绘制文本汉字("123啊", 48, 48, (255, 0, 0)).显示图片()
        # 图片数据 = 图片操作.绘制填充矩形(0, 0, 100, 100, (255, 0, 0)).显示图片()
        # 图片数据 = 图片操作.绘制多边形([[0, 74], [200, 74], [300, 142], [0, 142]], (255, 0, 0)).显示图片()
        # 图片数据 = 图片操作.绘制填充多边形([[0, 74], [200, 74], [300, 142], [0, 142]], (255, 0, 0)).显示图片()
        # 图片数据 = 图片操作.二值化().显示图片()
        # 图片数据 = 图片操作.二值化().转换为base64()
        # print(图片数据.到base64())

        # 图像操作类().加载图片从base64(图片数据.到base64()).显示图片()
        # 图片数据 = 图片操作.二值化(180)
        # 图片数据 = 图像操作类(图片数据).颜色翻转()
        # 图像操作类(图片数据).显示图片()
