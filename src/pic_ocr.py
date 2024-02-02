# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/1/24 15:26
# @Author  : Yanjun Hao
# @Site    :
# @File    : OCR.py
# @Software: PyCharm
# @Comment :

# SECTION: -------------------------------方式1---------------------------------------
# NOTE:
#  OCR文本检测
#  Linking: https://www.bilibili.com/video/BV15N4y1Q76F/?spm_id_from=333.337.search-card.all.click&vd_source=40437a7834b5b148effaa5971e14f8d6
# from paddleocr import PaddleOCR
# img_path=r'C:\Users\YanJun\Desktop\识别.png'
# ocr=PaddleOCR(lang='ch')
# result = ocr.ocr(img_path)
# NOTE: DL环境运行会报错ModuleNotFoundError: No module named 'paddle',
#  可通过python -m pip install paddlepaddle-gpu==2.4.2 -i https://pypi.tuna.tsinghua.edu.cn/simple安装GPU版本，担心担心破坏pytorch环境
# SECTION: -------------------------------方式1---------------------------------------


# SECTION: -------------------------------方式2---------------------------------------
#  tesseract安装包下载链接: https://digi.bib.uni-mannheim.de/tesseract/?C=M;O=D
# https://blog.csdn.net/cxyxx12/article/details/134920510
# https://blog.csdn.net/Castlehe/article/details/118751833
# https://blog.csdn.net/wuShiJingZuo/article/details/135016582
# https://blog.csdn.net/qq_38563206/article/details/132990793


from cfg.cfg import *
from PIL import Image, ImageEnhance
import pytesseract
from paddleocr import PaddleOCR
import shutil
import pandas as pd
import cv2
import os
from rich import print
import re
import sys
from pathlib import Path

FILE = Path(__file__).resolve()
ROOT_0 = FILE.parents[0]  # project root directory
ROOT_1 = FILE.parents[1]  # project root directory
if str(ROOT_0) not in sys.path:
    sys.path.append(str(ROOT_0))  # add ROOT to PATH
if str(ROOT_1) not in sys.path:
    sys.path.append(str(ROOT_1))  # add ROOT to PATH

pytesseract.pytesseract.tesseract_cmd = r'd:\SoftWare\Tesseract-OCR\tesseract.exe'


def ocr_text_of_frame_by_paddleocr(frame_path: str) -> dict:
    ocr = PaddleOCR(lang='ch')

    """🐱‍👓识别超时就停止"""
    try:
        ocr_result_list = ocr.ocr(frame_path)
        # print(ocr_result_list)

        # 使用正则表达式提取日期时间信息
        time_match = re.search(r'\((.*?) UTC\)', ocr_result_list[0])
        time_match_ = re.search(r'\((.*?) UTO\)', ocr_result_list[0])
        if time_match:
            timestamp = time_match.group(1)
        else:
            if time_match_:
                timestamp = time_match_.group(1)
            else:
                timestamp = None

        # 使用正则表达式提取 "Current Image: 48 / 1381"
        # pic_idx_match = re.search(r'Current Image: (\d+/\d+)', text)
        pic_idx_match = re.search(
            r'Current Image: (.+?) \| L/R Keyframes', ocr_result_list[-1])
        if pic_idx_match:
            pic_idx = pic_idx_match.group(1)
        else:
            pic_idx = None
        return {
            "timestamp": timestamp,
            "pic index": pic_idx,
            "text": ocr_result_list,
            "frame_path": frame_path,
        }

    except RuntimeError as timeout_error:
        # Tesseract processing is terminated
        print(f"🤗🤗🤗 [italic bold red]OCR ERROR: {frame_path}")
        return {
            "timestamp": None,
            "pic index": None,
            "text": None,
            "frame_path": frame_path,
        }


def ocr_text_of_frame_by_pytesseract(frame_path: str) -> dict:
    img = Image.open(frame_path)
    width, height = img.size
    # img.show()

    # 图片裁剪
    # 将要裁剪的图片块距原图左边界距左边距离，上边界距上边距离，右边界距左边距离，下边界距上边的距离。
    pic_idx_image_box = (1980, 0, 2140, 18)
    pic_idx_crop_img = img.crop(pic_idx_image_box)
    # time_box = (238,0,395,18)
    # time_crop_img = img.crop(time_box)
    # time_crop_img.show()

    # 增强图片对比度
    enhancer = ImageEnhance.Contrast(img)
    img_contrast = enhancer.enhance(2.0)
    pic_idx_enhancer = ImageEnhance.Contrast(pic_idx_crop_img)
    pic_idx_img_contrast = pic_idx_enhancer.enhance(2.0)

    # 指定配置，开启多列文字处理
    custom_config = r'--oem 3 --psm 6'

    """🐱‍👓识别超时就停止"""
    try:
        all_text = pytesseract.image_to_string(img_contrast,
                                               # lang='chi_sim',
                                               timeout=0.5,
                                               #    config=custom_config,
                                               )

        # 使用正则表达式提取日期时间信息
        time_match = re.search(r'\((.*?) UTC\)', all_text)
        time_match_ = re.search(r'\((.*?) UTO\)', all_text)
        if time_match:
            timestamp = time_match.group(1)
        else:
            if time_match_:
                timestamp = time_match_.group(1)
            else:
                timestamp = None

        # 使用正则表达式提取 "Current Image: 48 / 1381"
        # pic_idx_match = re.search(r'Current Image: (\d+/\d+)', text)
        pic_idx_match = re.search(
            r'Current Image: (.+?) \| L/R Keyframes', all_text)
        if pic_idx_match:
            pic_idx = pic_idx_match.group(1)
        else:
            pic_idx_text = pytesseract.image_to_string(pic_idx_img_contrast,
                                                       # lang='chi_sim',
                                                       timeout=0.5,
                                                       #    config=custom_config,
                                                       )
            second_ocr_pic_idx_match = re.search(
                r'Current Image: (.+?)', pic_idx_text)
            if second_ocr_pic_idx_match:
                pic_idx = second_ocr_pic_idx_match.group(1)
            else:
                pic_idx = None
        return {
            "timestamp": timestamp,
            "pic index": pic_idx,
            "text": all_text,
            "frame_path": frame_path,
        }
    except RuntimeError as timeout_error:
        # Tesseract processing is terminated
        print(f"🤗🤗🤗 [italic bold red]OCR ERROR: {frame_path}")
        return {
            "timestamp": None,
            "pic index": None,
            "text": None,
            "frame_path": frame_path,
        }


def split_video_to_frames(video_path: str, output_folder: Path) -> tuple:
    # 打开视频文件
    cap = cv2.VideoCapture(video_path)

    # 清空文件夹
    shutil.rmtree(output_folder, ignore_errors=True)
    # 创建输出文件夹
    os.makedirs(output_folder, exist_ok=True)

    # 获取视频的帧率
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    # 读取视频帧
    frame_count = 0
    frame_filename_list = []
    while True:
        ret, frame = cap.read()

        # 如果视频读取完毕，退出循环
        if not ret:
            break

        # 保存每一帧为图像文件
        frame_filename = os.path.join(
            output_folder, f"frame_{frame_count:04d}.jpg")
        cv2.imwrite(frame_filename, frame)
        frame_filename_list.append(frame_filename)

        frame_count += 1

    # 释放视频捕获对象
    cap.release()
    return frame_filename_list, fps


if __name__ == "__main__":
    # 视频文件路径
    video_path = "path/to/your/video.mp4"

    # 输出文件夹路径
    output_folder = "path/to/your/output/folder"

    # 调用函数拆分视频成帧
    split_video_to_frames(video_path, output_folder)
