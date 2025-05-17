#from https://miyashinblog.com/distance-estimation/
#from https://potesara-tips.com/futurewarning/
#Copilotにも教えてもらいました。

import torch
import csv
import warnings

def yolov5_func(model,image,crop = False):
    
    warnings.simplefilter('ignore',FutureWarning)#yolo使用時のFutureWarningを非表示

    #pytorchから
    #model = torch.hub.load("ultralytics/yolov5", "yolov5s", pretrained=True)
    #検出できる物体を表示
    #print(model.names)

    #results = model("test_car.jpg")
    with torch.amp.autocast('cuda'):
        results = model(image)
    objects = results.pandas().xyxy[0]#検出結果をobjectに格納

    num = 0 #回数
    data = [] #戻り値用

    #object格納データ = x座標とy座標,信頼度,クラスラベル,物体名

    #with open('detection Result.csv','w') as f:
        #print("ID,種類,x座標,y座標,幅,高さ",file = f) #print()の第2引数で出力先変更可

    for i in range(len(objects)):
            
        row = []#仮変数

        name = objects.name[i]
        row.append(name)

        xmin = objects.xmin[i]
        row.append(xmin)

        ymin = objects.ymin[i]
        row.append(ymin)

        width = objects.xmax[i] - objects.xmin[i]
        row.append(width)

        height = objects.ymax[i] - objects.ymin[i]
        row.append(height)
        
        data.append(row)
            #print(f"{i},種類:{name},x:{ximn},y:{ymin},幅:{width},高さ:{hight})
            #csvファイルにバウンディングBOX情報を出力
            #print(f"{i},{name},{xmin},{ymin},{width},{height}",file = f)

    #results.show()#検出した物体の表示
    if crop == True:
        results.crop()#検出した物体の切り抜き
    else:
        return data

if __name__ == '__main__':
    #pytorchから
    model = torch.hub.load("ultralytics/yolov5", "yolov5s", pretrained=True)
    image = "..\\woman's.jpg"
    data = yolov5_func(model,image,crop = False)
    print(data)
