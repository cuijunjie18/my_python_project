import cv2
import matplotlib.pyplot as plt
import numpy as np
import argparse

#构建展示图像函数
def show(title,img):
    cv2.imshow(title,img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

#重载自己的图像大小调整函数
def my_resize(img,height = 0,width = 0):
    if(height):
        temp_height = img.shape[0]
        my_ratio = height/temp_height
        img = cv2.resize(img,(0,0),fx = my_ratio,fy = my_ratio)
    if(width):
        temp_width = img.shape[1]
        my_ratio = width/temp_width
        img = cv2.resize(img,(0,0),fx = my_ratio,fy = my_ratio)
    return img

#寻找四个顶点的坐标
#传入的是图像类型(矩阵),而不是列表,但是函数中的比较利用了其列表性质,即下标访问
def My_order_points(pts):
    #为列表分配可容纳4个点的内存,实际上是构建4*2矩阵
    rect = np.zeros((4,2),dtype = "float32")

    #进行矩阵求和(这个方法找顶点会有bug,但是比我自己的好多了)
    s = np.sum(pts,axis = 1)#axis = 1为一维,因为当前矩阵是二维的,即行求和
     
    #进行矩阵相减,行相减,注意这里是h - w
    diff = np.diff(pts,axis = 1)

    #按照鸟瞰图顺序找tl,tr,br,bl
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]
    rect[3] = pts[np.argmax(diff)]
    rect[1] = pts[np.argmin(diff)]
    return rect

#进行透视变化,将原来图像重要信息透视(而不是缩小后的,缩小后的细节丢失过多)
#img为原图,pst为待变化轮廓的4个坐标点
def four_point_transform(img,pst):
    #获取坐标点
    rect = My_order_points(pst)
    (tl,tr,br,bl) = rect
    print(rect)
    
	#计算透视长宽的最大可能
    widthA = np.sqrt((tl[0] - tr[0])**2 + (tl[1] - tr[1])**2)
    widthB = np.sqrt((bl[0] - br[0])**2 + (bl[1] - br[1])**2)
    maxwidth = max(int(widthA),int(widthB))#这里要化为整型,因为后面生成变化图像只能是整数像素
    
    heightA = np.sqrt((tl[0] - bl[0])**2 + (tl[1] - bl[1])**2)
    heightB = np.sqrt((tr[0] - br[0])**2 + (tr[1] - br[1])**2)
    maxheight = max(int(heightA),int(heightB))#同上
    
	#构建变化后的坐标位置,注意这里也要是鸟瞰顺序
    dst = np.array([
        [0,0],
        [maxwidth-1,0],
        [maxwidth-1,maxheight-1],
        [0,maxheight-1]],dtype = "float32")
    
	#计算变化矩阵
    M = cv2.getPerspectiveTransform(rect,dst)
    warped = cv2.warpPerspective(img,M,(maxwidth,maxheight))#实际上最后的参数是截取新生成的图像的对应部分(我们要的矩形文本)
    
	#返回变化后的结果
    return warped
    
    
#搭建待处理的图像路径
img_path = "images/my_paper1.jpg"

#对待处理的图像进行大小调整,便于查看
img = cv2.imread(img_path)
ratio = img.shape[0]/500.0
img_copy = img.copy()
img = my_resize(img_copy,height = 500)
show("Test",img)

#预处理并进行边缘检测
Gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
Gray = cv2.GaussianBlur(Gray,(5,5),0)
Thresh_edge = cv2.Canny(Gray,40,100)#阈值自己根据图像情况调整
#show("Thresh_edge",Thresh_edge)

#进行轮廓提取(仅提取外轮廓)
contours= cv2.findContours(Thresh_edge,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[0]#注意这个0不要忘了,否则contours包含两个列表,会出错

#进行轮廓排序(因为纸张内部可能会有一些干扰轮廓,我们只需要最外围的)
#取最大的5个(可能不足5个)
contours = sorted(contours,key = cv2.contourArea,reverse = True)[0:5]

#测试轮廓
#for i in range(len(contours)):
    #img = cv2.drawContours(img,[contours[i]],-1,(0,0,255),3)
    #show("Contours",img)


#提取我想要的轮廓:应该是矩形的,故做轮廓近似判断
for i in range(len(contours)):
    # epsilon表示从原始轮廓到近似轮廓的最大距离,它是一个准确度参数
	# True表示封闭的
    eplison = cv2.arcLength(contours[i],True)
    approx = cv2.approxPolyDP(contours[i],0.02*eplison,True)
    if(len(approx) == 4):
        Screen_contour = approx
        break

#检测是否获取到了正确的近似轮廓
img = cv2.drawContours(img,[Screen_contour],-1,(0,0,255),3)
show("Test",img)

#弱化形式的透视变化预处理,在成功近似的轮廓中提取4个(即矩形的4个位置点)变化为原图像大小的坐标点(我的白忙活)
My_points_h = []
My_points_w = []
My_points = []
for i in range(len(approx)):
    for j in range(len(approx[i])):
        h = approx[i][j][0]
        w = approx[i][j][1]
        My_points_h.append(h)
        My_points_w.append(w)
        My_points.append([h,w])
        
#终于发现错误了,approx是图像数据类型,而My_points是列表
#测试发现Screen_contour,即近似轮廓还是一个有3个纬度的数据,行,列,通道;而透视变化处理的应该
#是矩阵,及仅有行列的,所以下面的 Screen_contour要reshape
#print(Screen_contour.shape)
#print(My_points)

#关键步骤,利用轮廓进行透视变化,将图片中的关键信息化为标准矩形(利用缩小后的图像)
Per_trans = four_point_transform(img_copy,Screen_contour.reshape(4,2)*ratio)#近似轮廓展开维4*2矩阵
show("Final",Per_trans)
show("Samll",my_resize(Per_trans,height = 650))