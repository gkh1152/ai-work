from ultralytics.models import YOLO
import os
os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'
 
if __name__ == '__main__':
    model = YOLO(model='ultralytics/cfg/models/11/yolo11.yaml')
    model.load('yolo11n.pt')
    model.train(data='./data.yaml', epochs=32, batch=32, device='0', imgsz=640, workers=2, cache=False,
                amp=True, mosaic=False, project='output/train', name='exp')
