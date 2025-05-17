#from https://copilot.microsoft.com/shares/aNw7eqiBPtL6cRy4vfHyw

import win32gui
import win32ui
import win32con
import win32api
import numpy as np
import cv2
from PIL import Image
import torch
import sys
import time
import threading

from ultralytucs import YOLO

#from function.func_yolov5_test import yolov5_func #自作


fps = 0#get fps

#リサイズ可能window作成
cv2.namedWindow('Capture',cv2.WINDOW_NORMAL)

def printfps():
    global fps
    while True:
        time.sleep(1)
        print(fps)
        fps = 0       

def capture_monitor(monitor_left, monitor_top, monitor_width, monitor_height):
    # デスクトップのデバイスコンテキストを取得
    hdesktop = win32gui.GetDesktopWindow()

    # デバイスコンテキストを作成
    desktop_dc = win32gui.GetWindowDC(hdesktop)
    img_dc = win32ui.CreateDCFromHandle(desktop_dc)
    mem_dc = img_dc.CreateCompatibleDC()

    # キャプチャ用のビットマップを作成
    bitmap = win32ui.CreateBitmap()
    bitmap.CreateCompatibleBitmap(img_dc, monitor_width, monitor_height)
    mem_dc.SelectObject(bitmap)

    # 指定範囲をキャプチャ
    mem_dc.BitBlt((0, 0), (monitor_width, monitor_height), img_dc, (monitor_left, monitor_top), win32con.SRCCOPY)

    # ビットマップを画像として取得
    bmpinfo = bitmap.GetInfo()
    bmpstr = bitmap.GetBitmapBits(True)

    # ピクセルデータをOpenCV用に変換
    img = np.frombuffer(bmpstr, dtype='uint8')
    img = img.reshape((bmpinfo['bmHeight'], bmpinfo['bmWidth'], 4))  # BGRA形式
    img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)  # BGR形式に変換

    # クリーンアップ
    win32gui.DeleteObject(bitmap.GetHandle())
    mem_dc.DeleteDC()
    img_dc.DeleteDC()
    win32gui.ReleaseDC(hdesktop, desktop_dc)

    #return img
    return img

if len(sys.argv) == 1:
    #Yolov5用のモデル
    model = torch.hub.load("ultralytics/yolov5", "yolov5s", pretrained=True)
else:
    model = torch.hub.load('yolov5','custom',path='yolov5\\yolov5s.pt',source='local')

#変数再利用
yolo = None


# 特定のモニターの位置とサイズを定義
# 例えば、第1モニター (仮想スクリーンの左上位置、幅と高さを定義)
monitor_left = 0
monitor_top = 0
monitor_width = 1920  # モニターの幅
monitor_height = 1080  # モニターの高さ


# キャプチャがオープンしている間続ける
#while(cap.isOpened()):

ret = True

thread = threading.Thread(target=printfps,name='printfps',daemon = True)
thread.start()

print("is Start...")


# メインループでキャプチャと表示
while True:
 
    #色の変数初期化
    color_red = 0
    color_green = 0
    color_blue = 0

    # モニターキャプチャ
    frame = capture_monitor(monitor_left, monitor_top, monitor_width, monitor_height)


    if ret == True:
        yolo = yolov5_func(model,frame)
    

        for i in range(len(yolo)):

            if len(yolo[i][0]) % 2 == 0:
                color_red = 255
            if len(yolo[i][0]) % 3 == 0:
                color_green = 255
            if len(yolo[i][0]) % 5 == 0:
                color_blue = 255

            #枠を描画****
            cv2.rectangle(
                    frame,
                    pt1 = (int(yolo[i][1]),int(yolo[i][2])),
                    pt2 = (int(yolo[i][1]) + int(yolo[i][3]),int(yolo[i][2]) + int(yolo[i][4])),
                    color = (color_red,color_green,color_blue),
                    thickness = 3, #デフォは1
                    lineType = cv2.LINE_4 #デフォはcv2.LINE_8
                    #Shiftもあるけどめんどいから略
                    )

            #--文字を描写
            #文字の背景箱
            cv2.rectangle(
                    frame,
                    pt1 = (int(yolo[i][1]),int(yolo[i][2]) - 20),
                    pt2 = (int(yolo[i][1] + (len(yolo[i][0]) * 10) + 40),int(yolo[i][2])),
                    color = (color_red,color_green,color_blue),
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
            #確率を出力
            cv2.putText(
                   frame,
                   text = str(yolo[i][5]),
                   org = (int(yolo[i][1] + (len(yolo[i][0] * 10))),int(yolo[i][2]) - 5) ,
                   fontFace = cv2.FONT_HERSHEY_PLAIN,
                   fontScale = 1.0,
                   color = (0,0,0),
                   thickness = 1,
                   lineType = cv2.LINE_AA
                   #以下略
                   )
                       

        #フレームを表示
        cv2.imshow('Capture', frame)
        fps += 1 
        print(fps)

        # 'q'キーが押されたらループから抜ける
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

# キャプチャをリリースし、ウィンドウを閉じる
#cap.release()
cv2.destroyAllWindows()
