# PDF Invert Printer / PDF 反色打印工具

[English Guide](#english) | [中文说明](#chinese)

<a name="english"></a>
## 🇬🇧 English Guide

### Introduction
This tool converts PDF files by inverting colors (turning dark backgrounds into white) and enhancing contrast (making text darker and sharper). It is designed for printing slides or documents that originally have dark/night modes, helping you save ink and improve readability on paper.

### Features
- **Batch Processing**: Automatically detects and processes all PDF files in the `input` directory.
- **Smart Inversion**: Inverts colors to make backgrounds white.
- **Contrast Enhancement**: Uses thresholding and linear stretching to ensure text is pure black and backgrounds are pure white, eliminating gray artifacts.
- **HD Output**: Adjustable DPI settings for high-quality printing.

### Prerequisites
1. **Python 3.x**
2. **Poppler**: Required backend for processing PDFs.
   - **macOS**: Install via Homebrew: `brew install poppler`
   - **Windows**: Download Poppler binaries and add `bin` folder to PATH (or configure path in `main.py`).

### Installation
1. Clone the repository.
2. Install the required Python libraries:
   ```bash
   pip install pdf2image Pillow numpy
   ```

### Usage
1. **Initialize Folders**: Run the script once to generate the necessary folders.
   ```bash
   python main.py
   ```
   This will create an `input` folder and an `output` folder.
2. **Add Files**: Place your PDF files into the **`input`** folder.
3. **Run**: Execute the script again.
   ```bash
   python main.py
   ```
4. **Get Results**: The processed files will be saved in the **`output`** folder with the suffix `_inverted.pdf`.

### Configuration
You can customize the following global variables at the top of `main.py`:
- `DPI`: Resolution setting (default: 300).
- `LOW_THRESHOLD`: Threshold for black (0-255). Pixels darker than this become pure black. **Increase this value if your text looks gray.**
- `HIGH_THRESHOLD`: Threshold for white (0-255). Pixels lighter than this become pure white.

---

<a name="chinese"></a>
## 🇨🇳 中文说明

### 简介
这是一个 PDF 处理工具，主要用于将 PDF 文件进行“反色”处理（即：深色背景变白，浅色文字变黑），并自动增强对比度。它非常适合用来打印那些为了屏幕阅读而设计成深色/夜间模式的幻灯片或电子书，既能节省墨水，又能让打印件更加清晰易读。

### 功能特点
- **批量处理**: 自动扫描并处理 `input` 文件夹下的所有 PDF 文件。
- **智能反色**: 将黑底白字转换为白底黑字。
- **对比度增强**: 采用“双阈值+线性拉伸”算法，有效去除灰色噪点，让灰色文字变成纯黑，背景变成纯白。
- **高清输出**: 支持自定义 DPI 分辨率，保证打印清晰度。

### 环境要求
1. **Python 3.x**
2. **Poppler**: `pdf2image` 库依赖此工具来读取 PDF。
   - **macOS**: 打开终端运行 `brew install poppler`
   - **Windows**: 下载 Poppler 二进制包，解压后将其 `bin` 目录添加到系统环境变量 PATH 中（或者直接在 `main.py` 代码中指定路径）。

### 安装指南
1. 下载本项目代码。
2. 安装必要的 Python 依赖包：
   ```bash
   pip install pdf2image Pillow numpy
   ```

### 使用方法
1. **初始化**: 首次运行脚本。
   ```bash
   python main.py
   ```
   程序会自动在当前目录下创建 `input` (输入) 和 `output` (输出) 两个文件夹。
2. **放入文件**: 将你需要处理的 PDF 文件复制到 **`input`** 文件夹中。
3. **运行程序**: 再次运行脚本。
   ```bash
   python main.py
   ```
4. **查看结果**: 处理完成后的 PDF 文件会保存在 **`output`** 文件夹中，文件名后缀为 `_inverted`。

### 参数调整
如果你对输出效果不满意，可以在 `main.py` 文件开头修改以下配置：
- `DPI`: 设置读取和保存的分辨率，默认为 300。如果要打印得非常清晰，可设为 400 或 600。
- `LOW_THRESHOLD`: **黑场阈值** (建议 60-120)。
  - 如果处理出来的**文字不够黑（偏灰）**，请尝试**调大**这个数值。
- `HIGH_THRESHOLD`: **白场阈值**。高于此亮度的像素会被强制变为纯白。
