import socket

def receive():
# 创建套接字
    with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
        s.bind(("0.0.0.0",12340))
        s.listen()
        print("等待连接...")
        connection, client_address = s.accept()
    # 接收图像数据
    image_data = b''  # 用于存储二进制图像数据的空字节串
    while True:
        chunk = connection.recv(1024)
        if not chunk:
            break
        image_data += chunk

    # 保存图像到文件
    received_image_path = 'C:/study-materials-report-python-windows/Ver6/receive_image.jpg'
    with open('C:/study-materials-report-python-windows/Ver6/receive_image.jpg', 'wb') as file:
        file.write(image_data)

    connection.close()
    s.close()
if __name__=="__main__":    
    receive()