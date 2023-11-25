import socket

def SendPicture():
        # 设置图像文件的存储路径和名称
        photo_filename = "C:/Users/USER/Desktop/project/facecut/face-seg-master/data/done/after.png"

                # 创建套接字连接到另一个程序
        with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
                s.connect(("25.16.40.2",12340))
        
        # 发送图像文件到另一个程序
                with open(photo_filename, 'rb') as file:
                        image_data = file.read()
                        s.sendall(image_data)
        print("圖像文字已發送")
if __name__=="__main__":
        SendPicture()