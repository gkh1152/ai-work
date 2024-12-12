from ultralytics.models import YOLO
 
 
if __name__ == '__main__':
    model = YOLO(model='output/train/exp/weights/best.pt')
    model.predict(source='datasets/images/test', device='0', imgsz=640, project='output/detect/', name='exp')