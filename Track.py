import cv2
import numpy as np

def show(img,title = 'Test'):
    cv2.imshow(title,img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def Track(origin,thresh):
    """物体追踪函数"""
    # origin = cv2.imread('images/origin.png')
    # thresh = cv2.imread('images/mask.png') # 虽然程序运行的时候是二级图,但是保存为png后处理为BGR了
    # print(thresh.shape)
    # print(origin.shape)
    """
    if(thresh.shape[2] == 3):
        gray = cv2.cvtColor(thresh,cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray,127,255,cv2.THRESH_BINARY)[1]
    # thresh = cv2.threshold(thresh,127,255,cv2.THRESH_BINARY_INV)[1]
    # show(thresh)
    """

    # 轮廓处理
    contours = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[0]

    # 特殊判断,没有轮廓直接返回原图像
    if(len(contours) == 0):
        return origin

    # 仅找面积最大的轮廓
    maxn = 0
    index = 0
    for i in range(len(contours)):
        S = cv2.contourArea(contours[i])
        if S > maxn:
            maxn = S
            index = i

    res = cv2.drawContours(origin,[contours[index]],-1,(0,255,0),3)
    return res
"""
# 找外接矩形
x,y,w,h = cv2.boundingRect(contours[index])
img = cv2.rectangle(origin,(x,y),(x+w,y+h),(0,255,0),5)
show(img)
"""
