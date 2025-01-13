import w,s,z
import os
import cv2
print('----------super-ready---------')
modelw=w.model
models=s.model
modelz=z.model

cropout='wsz/w/'
segout='wsz/s/'
modout='wsz/z/'

os.makedirs(cropout, exist_ok=True)
os.makedirs(segout, exist_ok=True)
os.makedirs(modout, exist_ok=True)


def clean(path):
    for file in os.listdir(path):
        os.remove(os.path.join(path,file))

clean(cropout)
clean(segout)
clean(modout)

def dectect(inpath):
    ne=os.path.basename(inpath)
    boxlist=w.yolomodel(modelw,inpath)

    cropedpath=w.cropandsave(boxlist,inpath,cropout)

    pad=[]
    for crop in cropedpath:
        path=os.path.join(cropout,crop)
        padpath=os.path.join(segout,crop)
        pad.append(padpath)
        newimg=s.segmentmodel(models,path)
        paddedpath=s.pad_to_square(newimg,padpath)


    dit={}
    labels=[]
    for ri in pad:
        label=z.model_output(modelz,ri)
        labels.append(label)
        dit[ri]=label
        print(ri,'---------',label)

    img=cv2.imread(inpath)
    num=0
    for box,lab in zip(boxlist,labels):
        num=num+1
        cv2.rectangle(img, (box[0], box[1]), (box[2], box[3]), (0, 255, 0), 3)
        cv2.putText(img, f'{num}-{lab}', (box[0],box[1]), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255) , 2)

    cv2.imwrite(modout+f'{ne}',img)
    return img,dit


