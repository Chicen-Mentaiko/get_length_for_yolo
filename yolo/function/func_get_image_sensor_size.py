import math

def calculate_sensor_size(diagonal_size, aspect_ratio_width, aspect_ratio_height):
    # アスペクト比計算
    aspect_ratio = aspect_ratio_width / aspect_ratio_height

    # 幅高さ計算
    height = math.sqrt((diagonal_size ** 2) / (1 + aspect_ratio ** 2))
    width = height * aspect_ratio

    return width, height

def gcd(x, y):
    if y == 0:
        return x
    else:
        return gcd(y, x % y)

if __name__ == '__main__':
    import cv2
    width = 36.0
    height = 24.0

    cap = cv2.VideoCapture(0)

    cap_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    cap_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)

    print("cap: " + str(cap_width) + ", " + str(cap_height))

    g = gcd(int(cap_width), int(cap_height))

    aspect_ratio_width = cap_width / g
    aspect_ratio_height = cap_height / g

    print("アスペクト比: " + str(int(aspect_ratio_width)) + ":" + str(int(aspect_ratio_height)))  # アスペクト比

    diagonal_size = math.sqrt(width ** 2 + height ** 2)
    sensor_size = calculate_sensor_size(diagonal_size, cap_width / g, cap_height / g)

    print(sensor_size)
