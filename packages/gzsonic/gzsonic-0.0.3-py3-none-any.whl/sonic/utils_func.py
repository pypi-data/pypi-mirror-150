import json
import cv2
import os
import numpy as np
import platform
from natsort import os_sorted
from glob import glob
from PIL import Image, ImageFont, ImageDraw

extensions = ['.bmp', '.gif', '.jpeg', '.jpg', '.pbm', '.png', '.tif', '.tiff']


def check_cwd():
    cwd = os.getcwd()
    if cwd.endswith('ui'):
        os.chdir('../')


def get_font(font_size=20):
    if platform.system() == 'Windows':
        font_path = 'simhei.ttf'
    elif platform.system() == 'Linux':
        font_path = 'NotoSansCJK-Regular.ttc'
    elif platform.system() == 'Darwin':
        font_path = 'Hiragino Sans GB.ttc'
    font = ImageFont.truetype(font_path, font_size)
    return font


def cv2_add_text(img, text, position, color=(255, 255, 0), font_size=20):
    if isinstance(img, np.ndarray):  # 判断是否OpenCV图片类型
        img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    # 创建一个可以在给定图像上绘图的对象
    draw = ImageDraw.Draw(img)
    # 字体的格式
    font = get_font(font_size)
    # 上移50像素点
    position = (position[0] - 20, position[1] - 20)
    # 绘制文本
    draw.text(position, text, color, font=font)
    # 转换回OpenCV格式
    return cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)


def open_folder(path):
    if platform.system() == 'Windows':
        os.startfile(path)


# 语法糖，记录函数运行时间
def count_time(function):
    def function_timer(*args, **kwargs):
        import time
        t0 = time.time()
        result = function(*args, **kwargs)
        t1 = time.time()
        print(f'【{function.__name__}】 函数花费时间{t1 - t0:6.2f}ms')
        return result

    return function_timer


def cv2_read_img(file_path):
    cv_img = cv2.imdecode(np.fromfile(file_path, dtype=np.uint8), cv2.IMREAD_UNCHANGED)
    return cv_img


def sorted_path_list(path_list):
    return os_sorted(path_list)


def glob_extensions(directory: str, ext_names: list = extensions):
    path_list = []
    if directory:
        for ext_name in ext_names:
            path_list += glob(
                f'{directory}/**/*{ext_name}', recursive=True)
    return sorted_path_list(path_list)


def make_dirs(dir_path):
    """
    如果文件夹不存在就创建。
    :filepath:需要创建的文件夹路径
    :return:
    """
    if not os.path.exists(dir_path):
        os.makedirs(dir_path, exist_ok=True)


# debug函数
def show_ndarry_pic(img):
    if len(img.shape) >= 3:
        new_img = Image.fromarray(img[:, :, ::-1], 'RGB')
    else:
        new_img = Image.fromarray(img, 'L')
    new_img.show()


def show_qpixmap(pixmap):
    img = Image.fromqpixmap(pixmap)
    img.show()


def save_json(json_path, data):
    with open(json_path, 'w', encoding='utf8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
