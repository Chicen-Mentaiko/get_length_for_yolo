#from https://qiita.com/kakuteki/items/e48b47e8ce77332bc051
import cv2

# ウェブカメラのキャプチャを開始,0はデフォルトのウェブカメラ
cap = cv2.VideoCapture(0) 

# キャプチャがオープンしている間続ける
while(cap.isOpened()):
    # フレームを読み込む
    ret, frame = cap.read()
    if ret == True:
        # フレームを表示
        cv2.imshow('Webcam Live', frame)

        # 'q'キーが押されたらループから抜ける
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

# キャプチャをリリースし、ウィンドウを閉じる
cap.release()
cv2.destroyAllWindows()
