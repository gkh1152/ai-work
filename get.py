import os
import xml.etree.ElementTree as ET

# 提取 XML 中所有的类别名称
def extract_classes_from_xml(xml_folder):
    classes = set()  # 使用 set 来避免重复
    for xml_file in os.listdir(xml_folder):
        if xml_file.endswith(".xml"):
            file_path = os.path.join(xml_folder, xml_file)
            tree = ET.parse(file_path)
            root = tree.getroot()
            
            # 获取所有 <object> 标签
            for obj in root.findall("object"):
                # 获取 <name> 标签的内容
                name = obj.find("name").text
                classes.add(name)  # 将类别名称添加到集合中
    return sorted(classes)  # 返回排序后的类别列表

# 示例：指定 XML 文件夹路径
xml_folder = r"D:\1lab\code\ultralytics-main\ultralytics-main\datasets\China_Drone\China_Drone\train\annotations\xmls"

# 获取所有类别名称
classes = extract_classes_from_xml(xml_folder)

# 打印提取的类别名称
print(classes)
