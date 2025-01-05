#copy form https://imagingsolution.net/program/python/opencv-python/opencv_videocapture/

import cv2
import sys

#カメラ起動
cap = cv2.VideoCapture(0)

index = 0

if len(sys.argv) == 1:
    directory = input("場所を入力>")
else:
    directory = sys.argv[1]

while True:
    #画像キャプチャ
    ret,frame = cap.read()

    #画像表示
    cv2.imshow("Frame",frame)

    #qキーでquit
    if cv2.waitKey(1) == ord('q'):
        break
    elif cv2.waitKey(1) == ord('s'):
        cv2.imwrite(f"{directory}\img{index:05d}.jpg",frame)
        index += 1
        print("save images: img" + str(index) + ".jpg")

cap.release()
cv2.destroyAllWindows()
