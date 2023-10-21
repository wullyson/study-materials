import cv2
image = cv2.imread('KW3.jpg')
x=[]
y=[]
with open('output.txt','r') as f:
	for line in f.readlines():
		temp = line.split(',') 
		x.append(float(temp[0]) * image.shape[1])
		y.append(float(temp[1]) * image.shape[0])
	
print(x[3])	
print(max(x))
print(min(x))
print(max(y))
print(min(y))