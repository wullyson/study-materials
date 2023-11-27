from receive import ReceivePicture
from Send import SendPicture
from haircut import haircut
from facecut import facecut
from Synthetic_Results import Synthetic
if __name__=="__main__":
    image1 = './data/Pre-Process_1/Face_matting.png' #臉
    image2 = './data/Pre-Process_1/Hair_matting.png' #頭髮
    #ReceivePicture()
    facecut()
    haircut()
    Synthetic(image1,image2)
    #SendPicture()