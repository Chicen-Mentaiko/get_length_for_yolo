from func_yolov5 import yolov5_func
import torch 


model = torch.hub.load("ultralytics/yolov5", "yolov5s", pretrained=True)

result = yolov5_func(model,"test_car.jpg")

for i in range(len(result)):
    for j in range(len(result)):
        print(result[i][j], end=' ')
    print()
