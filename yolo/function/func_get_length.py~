#get_ans.py

def get_m(things_height, resolution_height, image_sencer_size, camera_calibration, height_from_yolo):
    
    pixel = image_sencer_size / resolution_height

    get_mm_height_from_yolo = height_from_yolo * pixel
    get_mm_camera_calibration = camera_calibration * pixel

    get_length_from_pic = things_height * get_mm_camera_calibration / get_mm_height_from_yolo

    # 四捨五入された結果を取得
    get_length_from_pic_m = round(get_length_from_pic, 2)

    #print(get_length_from_pic_m)
    return get_length_from_pic_m
