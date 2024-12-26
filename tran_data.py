import os
import shutil
import random

# 设置数据路径和划分比例
data_path = "datasets"
output_path = "datasets"
split_ratios = {"train": 0.7, "val": 0.2, "test": 0.1}

# 确保输出文件夹存在
for split in ["train", "val", "test"]:
    os.makedirs(os.path.join(output_path, split, "images"), exist_ok=True)
    os.makedirs(os.path.join(output_path, split, "labels"), exist_ok=True)

# 遍历每个国家的文件夹
for country in os.listdir(data_path):
    country_path = os.path.join(data_path, country)
    if not os.path.isdir(country_path):
        continue

    # 获取 images 和 labels 文件夹路径
    images_path = os.path.join(country_path, "images")
    labels_path = os.path.join(country_path, "labels")

    # 获取所有文件列表，并打乱顺序
    image_files = sorted(os.listdir(images_path))
    random.shuffle(image_files)

    # 按比例划分数据
    num_files = len(image_files)
    train_split = int(num_files * split_ratios["train"])
    val_split = int(num_files * (split_ratios["train"] + split_ratios["val"]))

    splits = {
        "train": image_files[:train_split],
        "val": image_files[train_split:val_split],
        "test": image_files[val_split:]
    }

    # 移动文件到目标文件夹
    for split, files in splits.items():
        for file in files:
            # 移动图片文件
            shutil.copy(
                os.path.join(images_path, file),
                os.path.join(output_path, split, "images", file)
            )
            # 移动对应的标签文件
            label_file = file.replace(".jpg", ".txt").replace(".png", ".txt")  # 假设标签文件为 .txt 格式
            shutil.copy(
                os.path.join(labels_path, label_file),
                os.path.join(output_path, split, "labels", label_file)
            )

print("数据划分完成！")
