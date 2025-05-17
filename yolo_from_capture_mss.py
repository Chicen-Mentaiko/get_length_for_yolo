#yolo_from_capture_mss.py

#from{
# https://qiita.com/kakuteki/items/e48b47e8ce77332bc051
# https://ja.stackoverflow.com/questions/37060/typeerror-module-object-is-not-callable%e3%81%8c%e5%87%ba%e3%81%be%e3%81%99
# https://af-e.net/python-2d-array-usage/
# https://shikaku-mafia.com/opencv-puttext/
# https://shikaku-mafia.com/opencv-rectangle/
# https://qiita.com/nguti/items/9cb9e2880844ab68e861
#https://dev.classmethod.jp/articles/taking-a-screenshot-with-python-pillow-opencv-and-tried-object-detection/
#https://torus07.hatenablog.com/entry/OpenCV-07
#https://qiita.com/GANTZ/items/603e5428fd8eac8ff2b2

#copy from yolo_from_capture.py

from mss import mss
import numpy as np
import cv2
import torch
import sys
import time


from function.func_yolov5 import yolov5_func #自作

sct = mss() #mss関数を導入

#リサイズ可能window設定
cv2.namedWindow('Capture',cv2.WINDOW_NORMAL) 

monitor = {"top":0, "left":0, "width":1280, "height":720} #画面設定

if len(sys.argv) == 1:
    #Yolov5用のモデル
    model = torch.hub.load("ultralytics/yolov5", "yolov5s", pretrained=True)
else:
    model = torch.hub.load('yolov5','custom',path='yolov5\\yolov5s.pt',source='local')

#変数再利用
yolo = None

# キャプチャがオープンしている間続ける
#while(cap.isOpened()):

ret = True

while(1):
    # フレームを読み込む
    #ret, frame = cap.read()
    #スクショ取得
    frame = np.array(sct.grab(monitor))

    
    # JPEG形式にエンコード
    _, jpeg_image = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 100])

    if ret == True:
        yolo = yolov5_func(model,frame)
        
        for i in range(len(yolo)):
            #枠を描画****
            cv2.rectangle(
                    frame,
                    pt1 = (int(yolo[i][1]),int(yolo[i][2])),
                    pt2 = (int(yolo[i][1]) + int(yolo[i][3]),int(yolo[i][2]) + int(yolo[i][4])),
                    color = (0,0,255),
                    thickness = 3, #デフォは1
                    lineType = cv2.LINE_4 #デフォはcv2.LINE_8
                    #Shiftもあるけどめんどいから略
                    )

            #--文字を描写
            #文字の背景箱
            cv2.rectangle(
                    frame,
                    pt1 = (int(yolo[i][1]),int(yolo[i][2]) - 20),
                    pt2 = (int(yolo[i][1] + len(yolo[i][0]) * 10),int(yolo[i][2])),
                    color = (0,0,255),
                    thickness = -1
                    #以下略
                    )
            #文字本体
            cv2.putText(
                    frame,
                    text = str(yolo[i][0]),
                    org = (int(yolo[i][1]),int(yolo[i][2]) - 5) ,
                    fontFace = cv2.FONT_HERSHEY_PLAIN,
                    fontScale = 1.0,
                    color = (0,0,0),
                    thickness = 1,
                    lineType = cv2.LINE_AA
                    #以下略
                    )


        
        #ファイル見る
        frame = frame[:,:,0:3]
        frame = np.asarray(frame)

        # フレームを表示
        cv2.imshow('Capture', frame)
        

        # 'q'キーが押されたらループから抜ける
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

# キャプチャをリリースし、ウィンドウを閉じる
#cap.release()
cv2.destroyAllWindows()
frame[0][0][0] = 1 #お気持ち
