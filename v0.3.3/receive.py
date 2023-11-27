import socket

# 创建套接字
def ReceivePicture():
    with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
        s.bind(("0.0.0.0",12340))
        s.listen()
        print("等待連結...")
        connection, client_address = s.accept()

    # 接收图像数据
    image_data = b''  # 用于存储二进制图像数据的空字节串

    while True:
        chunk = connection.recv(1024)
        if not chunk:
            break
        image_data += chunk

    # 保存图像到文件
    received_image_path = 'C:/Users/USER/Desktop/project/facecut/face-seg-master/data/face/FacePicture.jpg'
    with open('C:/Users/USER/Desktop/project/facecut/face-seg-master/data/face/FacePicture.jpg', 'wb') as file:
        file.write(image_data)

    connection.close()
    s.close()
if __name__=="__main__":
    ReceivePicture()