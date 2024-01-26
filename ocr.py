# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/1/25 9:24
# @Author  : Yanjun Hao
# @Site    : 
# @File    : ocr.py
# @Software: PyCharm 
# @Comment :

from PIL import Image, ImageEnhance
import pytesseract
from tqdm import tqdm
import pandas as pd
import cv2
import os
from multiprocessing import Pool, cpu_count
import glob
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
from cfg.cfg import *
from src.pic_ocr import ocr_text_of_frame, split_video_to_frames


def main(is_multiprocessing: bool = False) -> None:
    video_path = FILE_ROOT / "video.mp4"
    frames_path = FIGURE_PATH / "Frames"

    # 视频 --> 一帧一帧照片
    frame_filename_list, _ = split_video_to_frames(video_path=str(video_path), output_folder=frames_path)
    # frame_filename_list = glob.glob(str(frames_path) + "/*")

    # 识别每祯视频的文字
    if is_multiprocessing:
        # SECTION: 多线程
        #  (https://www.cnblogs.com/azureology/p/13212723.html)
        #  (https://cloud.tencent.com/developer/article/1888969)
        print(f"[bold green]多线程识别中...cpu_count: {cpu_count()}[/bold green]")
        with Pool(int(cpu_count() / 2)) as pool:
            ocr_list = list(
                tqdm(pool.imap(ocr_text_of_frame, frame_filename_list), total=len(frame_filename_list)))
            # ocr_list = pool.map(ocr_text_of_frame, frame_filename_list[::2])

        # thread_pool = Pool(int(cpu_count() / 2))
        # ocr_list = thread_pool.map(ocr_text_of_frame, frame_filename_list)
        # thread_pool.close()
        # thread_pool.join()
    else:
        # SECTION: 单线程
        ocr_list = []
        for frame_filename_idx in tqdm(range(len(frame_filename_list)), desc=f"OCR", postfix=f"OCR Model",
                                       colour="green"):
            ocr_list.append(ocr_text_of_frame(frame_path=frame_filename_list[frame_filename_idx]))

    ocr_df = pd.DataFrame(ocr_list)

    # ocr_df['timestamp'] = ocr_df['timestamp'].apply(lambda x: re.sub(r'\.0$', '', x))  # 去掉末尾的.0
    for column in ocr_df.columns:
        if column in ['timestamp', 'pic index']:
            ocr_df[column] = ocr_df[column].apply(lambda x: x.replace(" ", "") if x else None)
        else:
            ocr_df[column] = ocr_df[column].apply(lambda x: x.replace('\n', '') if x else None)

    # 删掉空值所在行
    ocr_df = ocr_df.dropna(axis=0, how='all')  # 删掉全为空值的行

    ocr_df.sort_values(by=['frame_path'], inplace=True, ascending=True)

    ocr_df.drop_duplicates(subset=['timestamp', 'pic index'], keep='first', inplace=True)

    ocr_df['timestamp'] = pd.to_datetime(ocr_df['timestamp'], format='%Y-%m-%d-%H:%M:%S', errors='ignore')
    ocr_df.to_csv(RESULT_PATH / "ocr_result.csv", index=False, encoding='utf-8-sig')

    print("🚀🚀🚀 [italic bold green]Code Ending")


if __name__ == '__main__':
    main(is_multiprocessing=True)
