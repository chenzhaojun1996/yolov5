# import os
# import random
# trainval_percent = 0.1
# train_percent = 0.9
# xmlfilepath = 'imgs/xml'
# txtsavepath = 'imgs/txt'
#
# total_xml = os.listdir(xmlfilepath)
# num = len(total_xml)
# list = range(num)
# tv = int(num * trainval_percent)
# tr = int(tv * train_percent)
# trainval = random.sample(list, tv)
# train = random.sample(trainval, tr)
# ftrainval = open('imgs/ImageSets/trainval.txt', 'w')
# ftest = open('imgs/ImageSets/test.txt', 'w')
# ftrain = open('imgs/ImageSets/train.txt', 'w')
# fval = open('imgs/ImageSets/val.txt', 'w')
# for i in list:
#     name = total_xml[i][:-4] + '\n'
#     if i in trainval:
#         ftrainval.write(name)
#         if i in train:
#             ftest.write(name)
#         else:
#             fval.write(name)
#     else:
#         ftrain.write(name)
#
#
# print(total_xml)
# ftrainval.close()
# ftrain.close()
# fval.close()
# ftest.close()



import xml.etree.ElementTree as ET
import pickle
import os
from os import listdir, getcwd
from os.path import join

sets = ['train', 'test','val']
classes = ['car']
def convert(size, box):
    dw = 1. / size[0]
    dh = 1. / size[1]
    x = (box[0] + box[1]) / 2.0
    y = (box[2] + box[3]) / 2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    return (x, y, w, h)


def convert_annotation(image_id):
    in_file = open('imgs/xml/%s.xml' % (image_id))
    out_file = open('imgs/labels/%s.txt' % (image_id), 'w')
    tree = ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)
    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes or int(difficult) == 1:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text),
             float(xmlbox.find('ymax').text))
        bb = convert((w, h), b)
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')




wd = getcwd()
print(wd)



for image_set in sets:
    if not os.path.exists('imgs/labels/'):
        os.makedirs('imgs/labels/')
    image_ids = open('imgs/ImageSets/%s.txt' % (image_set)).read().strip().split()
    list_file = open('imgs/%s.txt' % (image_set), 'w')
    for image_id in image_ids:
        list_file.write(os.path.join(wd, 'imgs\pic\%s.jpg\n' % (image_id)))
        convert_annotation(image_id)
    list_file.close()

