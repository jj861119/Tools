import xml.etree.ElementTree as E
import json
from glob import glob
import os
import shutil
class_dict = {
    'person': 0,
    'car': 1,
    'motorbike': 2,
    'bicycle': 3,
    'bus': 4

}

for file_name in glob('Annotations/*.xml'):
    # file_name = 'Annotations\\2007_000663.xml'
    print(file_name)
    tree = E.parse(file_name)
    root = tree.getroot()
    d={}
    d['folder'] = root.find('folder').text
    d['filename'] = root.find('filename').text
    xml_img_size = root.find('size')
    d['size'] = [xml_img_size.find('width').text,
                xml_img_size.find('height').text,
                xml_img_size.find('depth').text]

    count = 0
    d['objects'] = {}
    for object in root.findall('object'):
        d['objects'][count] = {}
        d['objects'][count]['name']  = object.find('name').text
        d['objects'][count]['bbox']  = []
        # xmin, ymin, xmax, ymax
        for child in object.find('bndbox'):
            d['objects'][count]['bbox'].append(child.text)

        count += 1

    json_data = json.dumps(d)
    file_name = file_name.split('\\')[-1].split('.')[0]
    with open(f'Annotations_json_ALPR/{file_name}.json', "w") as json_file:
        json_file.write(json_data)

    img_width = float(xml_img_size.find('width').text)
    img_height = float(xml_img_size.find('height').text)
    with open(f'Annotations_yolov5_ALPR/{file_name}.txt', "w") as f:
        for object in d['objects'].values():
            name = object['name']
            if name in class_dict.keys():
                img_src = f'JPEGImages/{d["filename"]}'
                img_dst = f'images_{name}/{d["filename"]}'
                if not os.path.exists(img_dst):
                    shutil.copyfile(img_src, img_dst)
                box = object['bbox']
                f.write(f'{class_dict[name]} ')
                f.write(f'{float(box[0]) / img_width} ')
                f.write(f'{float(box[1]) / img_height} ')
                f.write(f'{(float(box[2]) - float(box[0])) / img_width} ')
                f.write(f'{(float(box[3]) - float(box[1])) / img_height}\n')