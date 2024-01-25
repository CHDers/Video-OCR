# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2024/1/25 9:22
# @Author  : Yanjun Hao
# @Site    : 
# @File    : cfg.py
# @Software: PyCharm 
# @Comment :

# NOTE: Linking: https://mp.weixin.qq.com/s/K1csxX_D8TIyZf-McBJQeg (还在使用os.path?Python中的Pathlib太香了)
# NOTE: Linking: https://zhuanlan.zhihu.com/p/508087828  (Python的platform模块)

import warnings

import matplotlib
import numpy as np
from matplotlib import font_manager
import matplotlib.pyplot as plt
import os
from pathlib import Path
import warnings
import pandas as pd
import platform


warnings.filterwarnings('ignore')
pd.set_option('max_colwidth', 200)
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', 1000)

# NOTE：---------------------------------------绘图风格------------------------------------
plt.style.use(['science', 'no-latex', 'grid'])
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.size'] = 14
plt.rcParams['axes.linewidth'] = 1.5
# plt.rcParams['xtick.major.size'] = 5
# plt.rcParams['ytick.major.size'] = 5
# plt.rcParams['xtick.minor.size'] = 2
# plt.rcParams['ytick.minor.size'] = 2
# %matplotlib inline
# %config InlineBackend.figure_format = 'svg'
# %config InlineBackend.figure_format = 'retina'

# 显示坐标轴刻度上的负数
matplotlib.rcParams['axes.unicode_minus'] = False

# 设置保存图片的格式和dpi
matplotlib.rcParams['savefig.dpi'] = 600
matplotlib.rcParams['savefig.format'] = 'svg'

# 设置显示中文
matplotlib.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签

# 散点图绘图的marker标识点类型
SCATTER_MARKER_LIST = ['o', '*', '^', 's', '+', 'p']
LINE_STYLE_LIST = ['-', '--', '-.', ':',
                   'solid', 'dashed', 'dashdot', 'dotted']
COLOR_LIST = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple', 'tab:brown', 'tab:pink', 'tab:gray',
              'tab:gray', 'tab:cyan']
# NOTE：---------------------------------------绘图风格------------------------------------


# NOTE：---------------------------------------系统选择------------------------------------
if platform.system() == "Windows":  # 'Linux', 'Windows'或者 'Java'
    font = {'family': 'Times New Roman', 'size': '14'}  # SimSun宋体 'weight':'bold',
    matplotlib.rc('font', **font)
# NOTE：---------------------------------------系统选择------------------------------------


# NOTE：---------------------------------------字体设置------------------------------------
# 设置中英文字体
chinese_font = font_manager.FontProperties(fname='C:\Windows\Fonts\simsun.ttc',
                                           size=14)  # times.ttf是Times New Roman常规，simsun.ttc是宋体常规
chinese_font_marker = font_manager.FontProperties(fname='C:\Windows\Fonts\simsun.ttc',
                                                  size=14)  # times.ttf是Times New Roman常规，simsun.ttc是宋体常规
# NOTE：---------------------------------------字体设置------------------------------------


# NOTE：---------------------------------------路径设置------------------------------------
# ROOT_PATH = os.path.abspath('../../../')
ROOT_PATH = Path(__file__).absolute().parent.parent

# 文件保存路径
FILE_ROOT = ROOT_PATH / "datasets"
RESULT_PATH = ROOT_PATH / "assets/data"
FIGURE_PATH = ROOT_PATH / "assets/figure"


# NOTE：---------------------------------------路径设置------------------------------------


if __name__ == "__main__":
    print(FILE_ROOT, RESULT_PATH, FIGURE_PATH)