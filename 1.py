import cv2

#构建展示图像函数
def show(title,img):
    cv2.imshow(title,img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

img = cv2.imread('images\page.jpg',cv2.IMREAD_GRAYSCALE)
img = cv2.resize(img,(600,600))
print(img.dtype)
show("Test",img)
print(img.shape)
x = 300
y = 400
img = img.reshape([x,y,int(600*600/(x*y))])
show("Test",img)
print(img.shape)
