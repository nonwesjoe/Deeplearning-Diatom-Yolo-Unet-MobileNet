import os.path
from ultralytics import YOLO
from PIL import Image
import os
print('--------------w-ready----------------')

model= YOLO("yolomodelor.pt")

def yolomodel(model,path): #input model | output boxlist
    results = model(path)
    for result in results:
        boxes = result.boxes  # Boxes object for bounding box outputs
    boxlist=[]
    for n, i in enumerate(boxes.xyxy.numpy()):
        print(i[0], i[1], i[2], i[3])
        xmin = int(i[0])
        ymin = int(i[1])
        xmax = int(i[2])
        ymax = int(i[3])
        boxlist.append([xmin, ymin, xmax, ymax])
    return boxlist


def cropimage(boxlist,path): #input boxlist | output imglist
    imglist=[]
    for i in boxlist:
        img = Image.open(path)
        cropped_image = img.crop((i[0], i[1], i[2], i[3]))
        imglist.append(cropped_image)
    return imglist

def cropandsave(boxlist,inpath,outpath):# input boxlist | save croped image and return pathlist
    pathlist=[]
    for num,i in enumerate(boxlist):
        img = Image.open(inpath)
        cropped_image = img.crop((i[0], i[1], i[2], i[3]))
        rawname=str(num)+'.png'
        imgname=os.path.join(outpath,rawname)
        cropped_image.save(imgname)
        pathlist.append(rawname)
    return pathlist

def cropandsavex(i,inpath,imgname):# input boxlist | save croped image and return pathlist
    img = Image.open(inpath)
    cropped_image = img.crop((i[0], i[1], i[2], i[3]))
    cropped_image.save(imgname)
    return
#
# path='origin/1.png'
# results=model(path)
# for result in results:
#     boxes = result.boxes  # Boxes object for bounding box outputs
#     segment= result.masks  # Masks object for segmentation masks outputs
#     print(type(segment))