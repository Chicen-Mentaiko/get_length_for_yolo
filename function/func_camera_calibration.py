#copy from https://miyashinblog.com/opencv-undistort/
#camera_calibration.py


import cv2
import numpy as np
import glob
#import sys

def camera_calibration(file):

    # Defining the dimensions of checkerboard
    CHECKERBOARD = (7,10)
    # cv2.TERM_CRITERIA_EPS:指定された精度(epsilon)に到達したら繰り返し計算を終了する
    # cv2.TERM_CRITERIA_MAX_ITER:指定された繰り返し回数(max_iter)に到達したら繰り返し計算を終了する
    # cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER : 上記のどちらかの条件が満たされた時に繰り返し計算を終了する
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    # Creating vector to store vectors of 3D points for each checkerboard image
    objpoints = []
    # Creating vector to store vectors of 2D points for each checkerboard image
    imgpoints = [] 


    # Defining the world coordinates for 3D points
    objp = np.zeros((1, CHECKERBOARD[0]*CHECKERBOARD[1], 3), np.float32)
    objp[0,:,:2] = np.mgrid[0:CHECKERBOARD[0], 0:CHECKERBOARD[1]].T.reshape(-1, 2)
    prev_img_shape = None

    if file == None:
        #修正(画像保存先を選択するか、引数で最初からやるか
        #if len(sys.argv) == 1:
        directory = input("画像保存先入力>")
            #file = directory + "\\*.jpg"
        #else:
            #directory = sys.argv[1]
        file = directory + "\\*.jpg"


    # Extracting path of individual image stored in a given directory
    images = glob.glob(file)#fileは上のやつ

    for filepath in images:
        img = cv2.imread(filepath)
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        # Find the chess board corners
        # If desired number of corners are found in the image then ret = true
        ret, corners = cv2.findChessboardCorners(gray, CHECKERBOARD, cv2.CALIB_CB_ADAPTIVE_THRESH+
        	cv2.CALIB_CB_FAST_CHECK+cv2.CALIB_CB_NORMALIZE_IMAGE)

        """
        If desired number of corner are detected,
        we refine the pixel coordinates and display 
        them on the images of checker board
        """
        if ret == True:
            objpoints.append(objp)
            # refining pixel coordinates for given 2d points.
            corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)

            imgpoints.append(corners2)

            # Draw the corners
            img = cv2.drawChessboardCorners(img, CHECKERBOARD, corners2,ret)

    cv2.destroyAllWindows()

    h,w = img.shape[:2]

    """
    Performing camera calibration by 
    passing the value of known 3D points (objpoints)
    and corresponding pixel coordinates of the 
    detected corners (imgpoints)
    """
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1],None,None)

    '''

    #出力    
    print("Camera matrix :")#これがカメラパラメータ
    print(mtx)
    print("dist :")#これが歪係数
    print(dist)
    # カメラ行列の各行をリストに追加し、数値だけに変換
    mtx_rows = [[float(num) for num in row] for row in mtx]
    # 歪み係数の各値をリストに追加し、数値だけに変換 
    dist_values = [float(value) for value in dist.flatten()]
    '''

    mtx_rows = np.array(mtx)
    dist_values = np.array(dist)
    #print(mtx_rows)
    #print(dist_values)
    
    return mtx_rows,dist_values

if __name__ == '__main__':
   mtx,dist = camera_calibration(None)
   print(mtx,dist)
