from ultralytics.models import YOLO
import os
os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'
 
if __name__ == '__main__':
    model = YOLO(model='output/train/exp/weights/best.pt')
    model.val(data='./data.yaml', split='val', batch=32, device='0', project='output/val', name='exp',
              half=False,)