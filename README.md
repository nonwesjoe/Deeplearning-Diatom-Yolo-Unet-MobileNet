# OM-Diatom-Classification-Yolo-MobileNet
## Architecture：YOLO + U-Net + MobileNetV2
* pipeline
* ![0](imgs/pipeline.png)
### YOLO: dectect where the object is.
* get individual diatom
* ![1](imgs/1.png)
### U-Net: segment from background.
* model architecture 
* ![2](imgs/unet.png)
* segment and data augmentation 
* ![3](imgs/seg1.png)
### MobileNetV2: classify them.
* model architecture
* ![4](imgs/mobilenet.png)
## Showcase 
* I used 3 models for the task and finally it works better than yolo only in my dataset.
* ![Screenshot_1](imgs/4.png)

