# coding: utf-8
import sys
import numpy as np
from mnist import load_mnist
from PIL import Image
import cv2



def img_show(img):
    pil_img = Image.fromarray(np.uint8(img))
    pil_img.show()

def my_show(img):
    cv2.imshow('Test',img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

#加载数据集，flatten是把numpy数据展开成一维数组了
#获取的是训练数据及训练标签
(x_train, t_train), (x_test, t_test) = load_mnist(flatten=True, normalize=False)

print(x_train.shape)

img = x_train[0]
label = t_train[0]
print('显示的数字是:',label)  # 5

print(img.shape)  # (784,)
img = img.reshape(28, 28)  # 把图像的形状变为原来的尺寸
print(img.shape)  # (28, 28)

#img_show(img)
#print(type(img),img.dtype)
my_show(img)
