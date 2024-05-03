import cv2
import numpy as np
import matplotlib.pyplot as plt
#from imutils import contours
#import myutils

#构建展示函数,辅助框架搭建流程
def show(name,img):
    cv2.imshow(name,img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

#手动建立轮廓排序函数
def sort_contours(contours,method = "left-to-right"):
    new_contours = []
    my_reverse = False
    if method == "right-to-left" or method == "below-to-top":
        my_reverse = True
    if method == "left-to-right" or method == "right-to-left":
        contours_x = {}
        for i in range(len(contours)):
            x,y,w,h = cv2.boundingRect(contours[i])
            contours_x[i] = x
        finish_x = sorted(contours_x.items(),key = lambda d:d[1],reverse = my_reverse)#按值排序
        for i in finish_x:
            new_contours.append(contours[i[0]])
    if method == "top-to-below" or method == "below-to-top":
        contours_y = {}
        for i in range(len(contours)):
            x,y,w,h = cv2.boundingRect(contours[i])
            contours_y[i] = y
        finish_y = sorted(contours_y.items(),key = lambda d:d[1],reverse = my_reverse)
        for i in finish_y:
            new_contours.append(contours[i[0]])
    return new_contours 

#初始化所需图片的路径
template_number_path = "images/STxihei.png"
card_path = "images/card.jpg"

#导入身份证号码模板
template_number_image = cv2.imread(template_number_path)
#show('Template',template_number_image)

template_gary = cv2.cvtColor(template_number_image,cv2.COLOR_BGR2GRAY)
template_thresh = cv2.threshold(template_gary,127,255,cv2.THRESH_BINARY_INV)[1]
#show('Template_thresh',template_thresh)

#提取每个数字的模板
template_each = []
contours,hierarchy = cv2.findContours(template_thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
contours = sort_contours(contours,method="left-to-right")
for i in range(len(contours)):
    x,y,w,h = cv2.boundingRect(contours[i])
    template_each.append(cv2.resize(template_thresh[y:y+h,x:x+w],(78,148)))

#for i in range(len(template_each)):
    #show("Each-Template",template_each[i])

#导入身份证信息
card_rgb = cv2.imread(card_path)
card_rgb = cv2.resize(card_rgb,(426,270))
card_gray = cv2.cvtColor(card_rgb,cv2.COLOR_RGB2GRAY)
#进入数字号码区域
card_rgb = card_rgb[200:220,130:370]
cut_number = card_gray[200:220,130:370]
#show('number_region',cut_number)
cut_number_big = cv2.resize(cut_number,(0,0),fx = 3,fy = 3)
card_rgb_big = cv2.resize(card_rgb,(0,0),fx = 3,fy = 3)
#show('Big',cut_number_big)
thresh = cv2.threshold(cut_number_big,50,255,cv2.THRESH_OTSU|cv2.THRESH_BINARY_INV)[1]
show('Test',thresh)

#提取身份证号码的轮廓进行矩形切割
contours,hierarchy = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
contours = sort_contours(contours,method = "left-to-right")

#进行模板匹配
indentify_come = []
for i in range(len(contours)):
    x,y,w,h = cv2.boundingRect(contours[i])
    temp = thresh[y:y+h,x:x+w]
    temp = cv2.resize(temp,(78,148))
    maxn = 0
    pos = 0
    for i in range(len(template_each)):
        x = cv2.minMaxLoc(cv2.matchTemplate(temp,template_each[i],cv2.TM_CCORR_NORMED))[1]
        if(x > maxn):
            maxn = x
            pos = i
    indentify_come.append(pos)
#输出结果
for i in range(len(indentify_come)):
    print(indentify_come[i],end = ' ')#python中一行输出的方法


