打開MainSystem(主程式) 即可跑出合成結果

每個模塊的功能
    MainSystem          結合需要執行的模塊。
    facecut             臉部裁減，包含轉正臉部與透明化圖片。
    haircut             頭髮裁減，包含透明化。
    Synthetic_Results   合成圖片，包含調整照片大小。

    Send                傳送圖片給用戶端。
    receive             接收用戶端傳送的圖片。
    
    Feature_Point       提取圖片鼻子特徵點的座標，使用此函數Noise_Feature_point(picture)，picture是要讀取的圖片。
    FaceCorrection      用於臉部轉正。

不要動的模塊
    train               訓練模塊。
    dataset             訓練數據。