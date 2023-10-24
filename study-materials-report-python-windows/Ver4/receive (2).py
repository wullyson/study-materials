import socket



# 创建套接字
with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
    s.bind(("192.168.54.110",1234))
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
received_image_path = 'C:/study-materials-report-python-windows/Ver4/receive_photo.jpg'
with open('C:/study-materials-report-python-windows/Ver4/receive_photo.jpg', 'wb') as file:
    file.write(image_data)

connection.close()
s.close()
