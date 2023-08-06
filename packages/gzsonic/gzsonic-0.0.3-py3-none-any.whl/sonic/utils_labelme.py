import json
import logging
import os
import shutil
import traceback
from collections import Counter

import cv2
import math
import numpy as np
from tqdm import tqdm


def cv_imread(file_path):
    cv_img = cv2.imdecode(
        np.fromfile(file_path, dtype=np.uint8), cv2.IMREAD_COLOR)
    return cv_img


def shape_to_points(shape):
    new_points = []
    shape_type = shape['shape_type']
    points = shape['points']
    if shape_type == 'polygon':
        new_points = points
        if len(points) < 3:
            new_points = []
            print('polygon 异常，少于三个点', shape)
    elif shape_type == 'rectangle':
        (x1, y1), (x2, y2) = points
        x1, x2 = sorted([x1, x2])
        y1, y2 = sorted([y1, y2])
        new_points = [(x1, y1), (x2, y1), (x2, y2), (x1, y2)]
    elif shape_type == "circle":
        # Create polygon shaped based on connecting lines from/to following degress
        bearing_angles = [
            0, 15, 30, 45, 60, 75, 90, 105, 120, 135, 150, 165, 180, 195, 210,
            225, 240, 255, 270, 285, 300, 315, 330, 345, 360
        ]

        orig_x1 = points[0][0]
        orig_y1 = points[0][1]

        orig_x2 = points[1][0]
        orig_y2 = points[1][1]

        # Calculate radius of circle
        radius = math.sqrt((orig_x2 - orig_x1)**2 + (orig_y2 - orig_y1)**2)

        circle_polygon = []

        for i in range(0, len(bearing_angles) - 1):
            ad1 = math.radians(bearing_angles[i])
            x1 = radius * math.cos(ad1)
            y1 = radius * math.sin(ad1)
            circle_polygon.append((orig_x1 + x1, orig_y1 + y1))

            ad2 = math.radians(bearing_angles[i + 1])
            x2 = radius * math.cos(ad2)
            y2 = radius * math.sin(ad2)
            circle_polygon.append((orig_x1 + x2, orig_y1 + y2))

        new_points = circle_polygon
    else:
        print('未知 shape_type', shape['shape_type'])

    new_points = np.asarray(new_points, dtype=np.int32)
    return new_points


def labelme2coco(json_path_list,
                 new_img_dir,
                 category_map,
                 category_list,
                 copy=True,
                 queue=None,
                 prograss_start=0,
                 prograss_end=100,
                 overwrite=False,
                 add_subdir=True):
    """
    :param json_path_list: json 文件名列表
    :param new_img_dir: 目标图片文件夹路径
    :param category_map: labelme 分类列表（abcdefg）
    :param category_list: coco 分类列表（脏污、黑点等）
    :param copy:
    :return:
    """
    annotations = []
    images = []
    obj_count = 0
    with tqdm(json_path_list, desc='labelme2coco') as pbar:
        bar_stepcount = len(pbar)
        bar_step = prograss_end - prograss_start
        bar_step *= 1.00
        bar_step /= bar_stepcount
        for idx, json_path in enumerate(pbar):
            if queue is not None:
                queue.put({
                    'func': 'progress_update',
                    'color': 2,
                    'val': prograss_start + idx * bar_step
                })

            if not os.path.exists(json_path):  # OK 样本
                continue
            json_filename = os.path.split(json_path)[-1]
            with open(json_path, encoding='utf-8') as f:
                data = json.load(f)

            old_dir = os.path.split(json_path)[0]
            img_path = f"{old_dir}/{data['imagePath']}"
            if not os.path.exists(img_path):
                logging.error(f'图片文件不存在：{img_path}')
                continue

            if add_subdir:
                subdir = os.path.split(old_dir)[-1]
                new_img_path = f"{new_img_dir}/{subdir}_{data['imagePath']}"
            else:
                new_img_path = f"{new_img_dir}/{data['imagePath']}"
            if copy:
                try:
                    if overwrite or not os.path.exists(new_img_path):
                        new_img_path.replace('\\', '/')
                        shutil.copy(img_path, new_img_path)
                except:
                    traceback.print_exc()
                    print(f'拷贝文件失败：{img_path}')
                    continue

            img = cv_imread(new_img_path)
            img_filename = os.path.split(new_img_path)[-1]
            height, width = img.shape[:2]
            images.append(
                dict(
                    id=idx, file_name=img_filename, height=height,
                    width=width))

            for shape in data['shapes']:
                if shape['label'] not in category_map:
                    print('发现未知标签', json_path, shape)
                    continue

                new_points = []
                try:
                    new_points = shape_to_points(shape)
                except:
                    logging.error(traceback.format_exc())

                if len(new_points) == 0:
                    print('解析 shape 失败', json_path, shape)
                    continue

                px = [x[0] for x in new_points]
                py = [x[1] for x in new_points]
                poly = new_points.flatten().tolist()
                x_min, y_min, x_max, y_max = (min(px), min(py), max(px),
                                              max(py))

                # 处理越界的 bbox
                x_max = min(x_max, width - 1)
                y_max = min(y_max, height - 1)

                category_id = category_list.index(category_map[shape['label']])
                data_anno = dict(
                    image_id=idx,
                    id=obj_count,
                    category_id=category_id,
                    bbox=[x_min, y_min, x_max - x_min, y_max - y_min],
                    area=(x_max - x_min) * (y_max - y_min),
                    segmentation=[poly],
                    iscrowd=0)

                annotations.append(data_anno)
                obj_count += 1

    categories = [{'id': i, 'name': x} for i, x in enumerate(category_list)]
    coco_format_json = dict(
        images=images, annotations=annotations, categories=categories)

    # 统计分类
    category_counter = Counter([x['category_id'] for x in annotations])
    for k, v in category_counter.most_common():
        print(category_list[k], v)
    return coco_format_json
