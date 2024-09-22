import cv2
import numpy as np
import Track as Tr

# 识别的颜色 BGR = (0,0,254)
# 可乐瓶盖 BGR = (71,31,200)
# 展示函数
def show(img,title = 'Test'):
    cv2.imshow(title,img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# 根据给定的HSV图像确定追踪的HSV的上下界
def cvt_hsv(hsv):
    b = hsv[0][0][0]
    l_hsv = np.uint8([[[b-30,100,100]]]) # """括号一定只能一个"""
    h_hsv = np.uint8([[[b+30,255,255]]])
    return l_hsv,h_hsv

# 基于轮廓查找的图像追踪
def Track(origin,mask):
    # mask已经是二级图像了,直接轮廓查找
    contours = cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    img = cv2.drawContours(origin,contours,-1,(0,255,0),5)
    show(img)
    

# 确定待识别的颜色,注意要shape为(1,1,1)   
track_color = np.uint8([[[71,31,200]]]) # BGR格式
hsv = cv2.cvtColor(track_color,cv2.COLOR_BGR2HSV)
l_hsv,h_hsv = cvt_hsv(hsv)
print(hsv)
print(l_hsv)
print(h_hsv)


# 打开视频捕获器,进行预处理
cap = cv2.VideoCapture(0)

if cap.isOpened() == False:
    print("Error!")
else:
    while(True):

        # 获取每一帧图像
        ret,frame = cap.read()

        # 兼容视频读入的处理
        if ret == False:
            break

        # 对图像进行颜色空间转换
        hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)

        # 生成目标掩膜
        mask = cv2.inRange(hsv,l_hsv,h_hsv)

        # 用掩膜对原图像进行处理
        res = cv2.bitwise_and(frame,frame,mask = mask)

        # 追踪图像
        track = Tr.Track(frame,mask)

        # """
        cv2.imshow('Track',track)
        cv2.imshow('Mask',mask)
        cv2.imshow('res',res)
        # """

        # Track(frame,mask)
        
        key = cv2.waitKey(10)&0xFF
        if key == 27:
            break
        """
        if key == ord('s'):
            cv2.imwrite('images/mask.png',mask)
            cv2.imwrite('images/origin.png',frame)
            break
        """

cap.release()
cv2.destroyAllWindows()
