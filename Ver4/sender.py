import socket

def sender():
        photo_filename = "captured_image.jpg"
        with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
                s.connect(("25.21.22.74",12340))
                
                # 发送图像文件到另一个程序
                with open(photo_filename, 'rb') as file:
                    image_data = file.read()
                    s.sendall(image_data)
                    print("图像文件已发送")

if __name__=="__main__":
    sender()
