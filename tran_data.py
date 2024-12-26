import os
import shutil
import random

# 随机种子
random.seed(42)

# 原始数据路径
original_dataset_path = '/mnt/workspace/data/China_MotorBike/train'
original_images_path = os.path.join(original_dataset_path, 'images')
original_labels_path = os.path.join(original_dataset_path, 'labels')

# 目标数据路径
target_dataset_path = '/mnt/workspace/yolo/ultralytics-main/datasets'
target_images_path = os.path.join(target_dataset_path, 'images')
target_labels_path = os.path.join(target_dataset_path, 'labels')

# 创建目标子目录
splits = ['train', 'val', 'test']
for split in splits:
    os.makedirs(os.path.join(target_images_path, split), exist_ok=True)
    os.makedirs(os.path.join(target_labels_path, split), exist_ok=True)

# 获取所有图像文件
all_images = [f for f in os.listdir(original_images_path) if f.endswith(('.jpg', '.png'))]
random.shuffle(all_images)

# 划分比例
total_files = len(all_images)
train_split = int(total_files * 0.7)
val_split = train_split + int(total_files * 0.2)

splits_data = {
    'train': all_images[:train_split],
    'val': all_images[train_split:val_split],
    'test': all_images[val_split:]
}

# 移动文件
for split, files in splits_data.items():
    for image_file in files:
        # 原始图像路径
        src_image_path = os.path.join(original_images_path, image_file)
        dst_image_path = os.path.join(target_images_path, split, image_file)

        # 原始标注路径
        label_file = image_file.rsplit('.', 1)[0] + '.txt'  # 替换扩展名
        src_label_path = os.path.join(original_labels_path, label_file)
        dst_label_path = os.path.join(target_labels_path, split, label_file)

        # 复制文件
        shutil.copy(src_image_path, dst_image_path)
        if os.path.exists(src_label_path):  # 确保标注文件存在
            shutil.copy(src_label_path, dst_label_path)

print("数据集划分完成！")
