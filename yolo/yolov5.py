import torch
import csv

#pytorchから
model = torch.hub.load("ultralytics/yolov5", "yolov5s", pretrained=True)
#検出できる物体を表示
print(model.names)

results = model("test_car.jpg")
objects = results.pandas().xyxy[0]#検出結果をobjectに格納

#object格納データ = x座標とy座標,信頼度,クラスラベル,物体名

with open('detection Result.csv','w') as f:
    print("ID,種類,x座標,y座標,幅,高さ",file = f) #print()の第2引数で出力先変更可

    for i in range(len(objects)):
        name = objects.name[i]
        xmin = objects.xmin[i]
        ymin = objects.ymin[i]
        width = objects.xmax[i] - objects.xmin[i]
        height = objects.ymax[i] - objects.ymin[i]
        #print(f"{i},種類:{name},x:{ximn},y:{ymin},幅:{width},高さ:{hight})
        #csvファイルにバウンディングBOX情報を出力
        print(f"{i},{name},{xmin},{ymin},{width},{height}",file = f)

results.show()#検出した物体の表示
results.crop()#検出した物体の切り抜き
