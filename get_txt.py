import os
import xml.etree.ElementTree as ET

# 类别映射规则
class_mapping = {
    "D00": "D00", "D01": "D00",    # D00 和 D01 归为 D00
    "D10": "D10", "D11": "D10",    # D10 和 D11 归为 D10
    "D20": "D20",                  # D20 保持为 D20
    "D40": "D40", "D43": "D40", "D44": "D40",  # D40, D43, D44 归为 D40
}

# 为映射后的类别分配索引
final_classes = ["D00", "D10", "D20", "D40"]
class_to_id = {name: idx for idx, name in enumerate(final_classes)}

# 输入和输出路径
input_folder = "/mnt/workspace/data/China_MotorBike/train/annotations/xmls"  # 替换为你的 XML 文件夹路径
output_folder = "/mnt/workspace/data/China_MotorBike/train/txtf"  # 替换为目标 TXT 文件夹路径
os.makedirs(output_folder, exist_ok=True)

# 遍历 XML 文件
for xml_file in os.listdir(input_folder):
    if not xml_file.endswith(".xml"):
        continue

    # 解析 XML 文件
    tree = ET.parse(os.path.join(input_folder, xml_file))
    root = tree.getroot()

    # 获取图像尺寸
    size = root.find("size")
    img_width = int(size.find("width").text)
    img_height = int(size.find("height").text)

    # 存储有效标签的 YOLO 格式数据
    yolo_data = []

    # 遍历所有 object 标签
    for obj in root.findall("object"):
        name = obj.find("name").text
        if name not in class_mapping:
            continue  # 跳过无效标签

        # 映射类别到大类
        mapped_name = class_mapping[name]
        if mapped_name not in class_to_id:
            continue  # 跳过无效类别映射

        # 获取边界框信息
        bndbox = obj.find("bndbox")
        xmin = int(bndbox.find("xmin").text)
        ymin = int(bndbox.find("ymin").text)
        xmax = int(bndbox.find("xmax").text)
        ymax = int(bndbox.find("ymax").text)

        # 计算 YOLO 格式的相对坐标
        x_center = (xmin + xmax) / 2.0 / img_width
        y_center = (ymin + ymax) / 2.0 / img_height
        width = (xmax - xmin) / img_width
        height = (ymax - ymin) / img_height

        # 获取类别 ID
        class_id = class_to_id[mapped_name]

        # 添加到 YOLO 数据列表
        yolo_data.append(f"{class_id} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}")

    # 输出 TXT 文件
    txt_file = os.path.join(output_folder, xml_file.replace(".xml", ".txt"))
    with open(txt_file, "w") as f:
        f.write("\n".join(yolo_data))

print("XML 文件已转换为 YOLO 格式 TXT 文件！")






""" import os
import xml.etree.ElementTree as ET

# 手动指定类别名称列表
classes = ['Block crack', 'D00', 'D10', 'D20', 'D40', 'Repair']  # 在此处指定你的类别名称

# 获取类别ID映射
class_to_id = {name: idx for idx, name in enumerate(classes)}

# 初始化类别计数器
class_counts = {name: 0 for name in classes}  # 每个类别计数初始为0

# 将 XML 转换为 YOLO 格式的 .txt
def xml_to_yolo_txt(xml_folder, image_folder, output_folder, classes):
    # 创建输出文件夹（如果不存在）
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 遍历 XML 文件夹
    for xml_file in os.listdir(xml_folder):
        if xml_file.endswith(".xml"):
            file_path = os.path.join(xml_folder, xml_file)
            tree = ET.parse(file_path)
            root = tree.getroot()
            
            # 获取图像文件名，去掉扩展名
            image_filename = root.find("filename").text
            image_name = os.path.splitext(image_filename)[0]  # 去掉扩展名

            # 获取图像的尺寸
            width = int(root.find(".//size/width").text)
            height = int(root.find(".//size/height").text)

            # 创建对应的 YOLO 格式的 .txt 文件
            txt_file_path = os.path.join(output_folder, image_name + ".txt")
            with open(txt_file_path, "w") as f:
                # 遍历所有的 <object> 标签
                for obj in root.findall("object"):
                    name = obj.find("name").text  # 获取类别名称
                    if name in class_to_id:
                        # 统计类别数量
                        class_counts[name] += 1  # 累计该类别的计数

                        # 获取目标框的坐标
                        bndbox = obj.find("bndbox")
                        xmin = int(bndbox.find("xmin").text)
                        ymin = int(bndbox.find("ymin").text)
                        xmax = int(bndbox.find("xmax").text)
                        ymax = int(bndbox.find("ymax").text)

                        # 计算 YOLO 格式的坐标
                        x_center = (xmin + xmax) / 2.0 / width
                        y_center = (ymin + ymax) / 2.0 / height
                        obj_width = (xmax - xmin) / float(width)
                        obj_height = (ymax - ymin) / float(height)

                        # 获取类别的 ID
                        class_id = class_to_id[name]

                        # 写入 YOLO 格式的内容：类别ID x_center y_center width height
                        f.write(f"{class_id} {x_center} {y_center} {obj_width} {obj_height}\n")

            print(f"Converted {xml_file} to YOLO format.")

# 示例：指定 XML 文件夹、图像文件夹、输出文件夹路径
xml_folder = "/mnt/workspace/data/Czech/train/annotations/xmls"
image_folder = "/mnt/workspace/data/Czech/train/images/"
output_folder = "/mnt/workspace/data/Czech/train/txtf"

# 调用函数将 XML 转换为 YOLO 格式的 .txt
xml_to_yolo_txt(xml_folder, image_folder, output_folder, classes)

# 打印类别统计结果
print("Label Counts:")
for label, count in class_counts.items():
    print(f"{label}: {count}")

print(f"YOLO format .txt files have been saved to {output_folder}")
 """