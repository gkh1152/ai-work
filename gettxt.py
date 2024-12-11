import os
import xml.etree.ElementTree as ET

# 手动指定类别名称列表
classes =['Block crack', 'D00', 'D10', 'D20', 'D40', 'Repair'] # 在此处指定你的类别名称

# 获取类别ID映射
class_to_id = {name: idx for idx, name in enumerate(classes)}

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
xml_folder = r"D:\1lab\code\ultralytics-main\ultralytics-main\datasets\China_Drone\China_Drone\train\annotations\xmls"
image_folder = r"D:\1lab\code\ultralytics-main\ultralytics-main\datasets\China_Drone\China_Drone\train\images"
output_folder = r"D:\1lab\code\ultralytics-main\ultralytics-main\datasets\China_Drone\China_Drone\train\yolo_annotations"

# 调用函数将 XML 转换为 YOLO 格式的 .txt
xml_to_yolo_txt(xml_folder, image_folder, output_folder, classes)

print(f"YOLO format .txt files have been saved to {output_folder}")
