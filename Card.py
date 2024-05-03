import cv2
import matplotlib.pyplot as plt
import numpy as np

def show(title,img):
    cv2.imshow(title,img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

#设置路径参数
card_1_path = "images/credit_card_01.png"
template_path = "images/ocr_a_reference.png"

#读取模板BGR图像
template = cv2.imread(template_path)
show('BGR_template',template)

#转换灰度值
template_gray = cv2.cvtColor(template,cv2.COLOR_BGR2GRAY)
show('Gray_template',template)
print(template.shape)

#二极化
ret,thresh = cv2.threshold(template_gray,127,255,cv2.THRESH_BINARY_INV)
show('Thresh_template',thresh)

#获取模板外轮廓
contours,hierarchy = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
temp = template.copy()
#初始化每个数字模板的图像数组
digits = []
for (index,contour) in enumerate(contours):#经打印验证,外轮廓是从9开始倒着来的
    x,y,w,h = cv2.boundingRect(contour)
    res = thresh.copy()[y:y+h,x:x+w]
    res = cv2.resize(res,(0,0),fx = 1.5,fy = 1.5)
    digits.append(res)

#将轮廓顺序反转
digits.reverse()
for i in range(0,10):
    show(str(i),digits[i])




#读取银行卡1的BGR图像
card1 = cv2.imread(card_1_path)
show('Card_BGR',card1)

#缩小图片大小,减少像素点,便于数字闭运算连成块
card1 = cv2.resize(card1,(292,184))

#转换为灰度图
card1_gray = cv2.cvtColor(card1,cv2.COLOR_BGR2GRAY)
show('Card_Gray',card1_gray)

#进行一次Tophat形态学操作,取出图像的相对背景的亮部分
kernel = np.ones((3,3))
card1_tophat = cv2.morphologyEx(card1_gray,cv2.MORPH_TOPHAT,kernel)
show('Card_Tophat',card1_tophat)

#进行一次Sobel算子计算梯度,提高Tophat操作后有用部分的亮度
card1_gradx = cv2.convertScaleAbs(cv2.Sobel(card1_tophat,cv2.CV_64F,1,0,ksize = 3))
card1_grady = cv2.convertScaleAbs(cv2.Sobel(card1_tophat,cv2.CV_64F,0,1,ksize = 3))
card1_gradxy = cv2.addWeighted(card1_gradx,0.5,card1_grady,0.5,0)
show('Sobel_xy',card1_gradxy)

#进行形态学闭运算,填充暗区域,使数字连成块
card1_close = cv2.morphologyEx(card1_gradxy,cv2.MORPH_CLOSE,kernel,iterations = 3)#经检验,迭代三次最优
show('Close',card1_close)

#将图像二极化处理,便于提高轮廓查找准确率
ret,card1_thresh = cv2.threshold(card1_close,0,255,cv2.THRESH_BINARY|cv2.THRESH_OTSU)#乐观算法,自己找合适阈值
show('Thresh',card1_thresh)

#获取轮廓
contours,hierarchy = cv2.findContours(card1_thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
card1_temp = card1.copy()
#测试轮廓获取顺序
for contour in contours:
    res = cv2.drawContours(card1_temp,[contour],-1,(0,0,255),2)
    show('Test',res)      #测验结果:[4,5,6,7](由卡1得到)

#获取符合条件的轮廓比例
x,y,w,h = cv2.boundingRect(contours[4])
standard = w/h

#将所获得的轮廓进行筛选并提取出数字块图像,只留下数字部分
blocks_thresh = []
blocks_rgb = []
for contour in contours:
    x,y,w,h = cv2.boundingRect(contour)
    if w/h >= 3.125-0.125 and w/h <= 3.125+0.125: #允许数字块间存在一定偏差
        cut = card1.copy()[y-5:y+h+5,x-5:x+w+5]
        blocks_rgb.append(cut)

#将图像列表反转为正确的顺序
blocks_rgb.reverse()
#恢复数字块rgb的大小
for i in range(0,len(blocks_rgb)):
    blocks_rgb[i] = cv2.resize(blocks_rgb[i],(0,0),fx = 3,fy = 3)
print(len(blocks_rgb))

#对每个数字块(RGB,因为Thresh已将区块内数字连接,无法区分了)进行轮廓处理,取出内部具体数据,即每个数字
numbers = []
for i in range(0,len(blocks_rgb)):
    temp_gray = cv2.cvtColor(blocks_rgb[i],cv2.COLOR_BGR2GRAY)
    ret,thresh = cv2.threshold(temp_gray,0,255,cv2.THRESH_BINARY|cv2.THRESH_OTSU)
    contours,hierarchy = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    score = []
    for contour in contours:
        x,y,w,h = cv2.boundingRect(contour)
        img = thresh.copy()[y:y+h,x:x+w]
        img = cv2.resize(img,(81,129))
        score.append(img)
    score.reverse()
    for img in score:
        numbers.append(img)

for img in numbers:
    show('Cut_block',img)
#初始化最终识别结果
ans = []
for img in numbers:
    #初始化最佳匹配度及对应的数字
    most_near = -5
    img_number = -1
    for i in range(0,len(digits)):#遍历模板进行匹配
        res = cv2.matchTemplate(img,digits[i],cv2.TM_CCOEFF_NORMED)#归一化匹配
        minn,maxl,minloc,maxloc = cv2.minMaxLoc(res)
        if maxl > most_near:
            most_near = maxl
            img_number = i
    ans.append(img_number)

#输出结果的字符串
card_number_str = ""
for i in ans:
    card_number_str += str(i)
print(card_number_str)