from ultralytics import YOLO

model = YOLO("yolov11n.pt")

result = model("3Kyoudai.png")

print(result)
