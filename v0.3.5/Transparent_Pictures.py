import cv2

def Transparent_Pictures(star,result):
    transparent_image1=cv2.imread(star)
    transparent_image1 = cv2.cvtColor(transparent_image1, cv2.COLOR_BGR2BGRA)
    gray_transparent_image1=cv2.cvtColor(transparent_image1, cv2.COLOR_BGR2GRAY) 
    w=transparent_image1.shape[1]
    h=transparent_image1.shape[0]

    for x in range(w):
        for y in range(h):
            if gray_transparent_image1[y, x] == 0:
                transparent_image1[y, x, 3] = 0 
    cv2.imwrite(result,transparent_image1)

if __name__=='__main__':

    star='./data/finish/incereaseH_image.png'
    result='./data/finish/transparent_face.png'
    Transparent_Pictures(star,result)