import os
import numpy as np
from pdf2image import convert_from_path
from PIL import Image, ImageOps, ImageDraw

# --- 全局配置参数 ---
INPUT_FOLDER = "input"          # 输入文件夹
OUTPUT_FOLDER = "output"        # 输出文件夹
POPPLER_BIN_PATH = None         # Poppler 路径 (macOS brew 安装无需设置，Windows 可能需要指定)
DPI = 400                       # PDF 读取分辨率 (300标准, 400-600高清)
LOW_THRESHOLD = 100             # 黑场阈值 (0-255): 低于此值的像素变纯黑，建议根据情况调整 (60-100)
HIGH_THRESHOLD = 190            # 白场阈值 (0-255): 高于此值的像素变纯白
OUTPUT_SUFFIX = "_inverted"     # 输出文件后缀名

def apply_contrast_enhancement(image, low_threshold=50, high_threshold=200):
    """
    对图像应用双阈值处理并进行线性拉伸：
    - 小于 low_threshold -> 0 (纯黑)
    - 大于 high_threshold -> 255 (纯白)
    - 中间值 -> 线性拉伸到 0-255 之间
    """
    # 转为 float 类型进行计算，防止溢出
    img_array = np.array(image, dtype=np.float32)

    # 1. 截断范围 (Clip)
    # 所有小于 low 的变成 low，大于 high 的变成 high
    img_array = np.clip(img_array, low_threshold, high_threshold)
    
    # 2. 线性拉伸 (Linear Contrast Stretching)
    # 将 [low, high] 映射到 [0, 255]
    # 公式: output = (input - low) * 255 / (high - low)
    if high_threshold > low_threshold:
        img_array = (img_array - low_threshold) * 255.0 / (high_threshold - low_threshold)
    
    #.转换回 uint8 图像数据
    return Image.fromarray(np.uint8(img_array))

def invert_and_enhance_pdf(input_pdf_path, output_pdf_path, poppler_path=None, dpi=300, low_threshold=60, high_threshold=190):
    """
    读取 PDF -> 反色 -> 增强对比度 -> 保存
    :param dpi: 控制分辨率。300 是标准打印质量，400-600 是高清，但文件会变大。
    """
    print(f"正在读取 PDF: {input_pdf_path} ...")
    print(f"当前设置分辨率 DPI: {dpi} (若速度过慢或内存不足，请适当调低)")
    
    try:
        # 关键点1：在这里设置读取的 DPI
        images = convert_from_path(input_pdf_path, dpi=dpi, poppler_path=poppler_path)
    except Exception as e:
        print(f"读取 PDF 失败。请检查路径是否正确。\n错误信息: {e}")
        return

    processed_images = []
    total_pages = len(images)
    print(f"共 {total_pages} 页，开始处理颜色和对比度...")

    for i, img in enumerate(images):
        # 1. 确保图像模式为 RGB
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # 2. 反色处理
        inverted_img = ImageOps.invert(img)
        
        # 3. 增强对比度
        # 这里的阈值：
        # low_threshold: 反色后亮度 < low_threshold 变纯黑
        # high_threshold: 反色后亮度 > high_threshold 变纯白
        enhanced_img = apply_contrast_enhancement(inverted_img, low_threshold=low_threshold, high_threshold=high_threshold)
        
        processed_images.append(enhanced_img)
        print(f"  - [{i+1}/{total_pages}] 处理完成")

    # 保存为新的 PDF
    if processed_images:
        print(f"正在保存到: {output_pdf_path} ...")
        # 关键点2：保存时 resolution 参数要与读取时的 DPI 一致，
        # 否则生成的 PDF 页面尺寸可能会变得非常大或非常小。
        processed_images[0].save(
            output_pdf_path, 
            "PDF", 
            resolution=float(dpi),  # 保持分辨率元数据一致
            save_all=True, 
            append_images=processed_images[1:]
        )
        print(f"处理成功！输出文件位于: {os.path.abspath(output_pdf_path)}")
    else:
        print("未找到可处理的页面。")

# --- 主程序 ---
if __name__ == "__main__":
    
    # 3. 确保文件夹存在
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)
        print(f"已创建输出文件夹: {OUTPUT_FOLDER}")

    if not os.path.exists(INPUT_FOLDER):
        os.makedirs(INPUT_FOLDER)
        print(f"已创建输入文件夹: {INPUT_FOLDER}")
        # 生成一个简单的测试图
        print(f"输入文件夹为空，生成测试文件 example.pdf ...")
        test_file_path = os.path.join(INPUT_FOLDER, "example.pdf")
        img = Image.new('RGB', (800, 800), color='black')
        d = ImageDraw.Draw(img)
        d.text((50,50), "High Resolution Test", fill=(255,255,255))
        img.save(test_file_path, "PDF")

    # 4. 遍历处理所有 PDF 文件
    pdf_files = [f for f in os.listdir(INPUT_FOLDER) if f.lower().endswith('.pdf')]
    
    if not pdf_files:
        print(f"在 '{INPUT_FOLDER}' 中未找到 PDF 文件。")
    else:
        print(f"发现 {len(pdf_files)} 个 PDF 文件，准备处理...")
        
        for filename in pdf_files:
            input_path = os.path.join(INPUT_FOLDER, filename)
            
            # 构造输出文件名：原文件名_inverted.pdf
            file_stem = os.path.splitext(filename)[0]
            output_filename = f"{file_stem}{OUTPUT_SUFFIX}.pdf"
            output_path = os.path.join(OUTPUT_FOLDER, output_filename)
            
            print(f"\n--- 处理文件: {filename} ---")
            # 运行转换函数
            invert_and_enhance_pdf(
                input_path, 
                output_path, 
                poppler_path=POPPLER_BIN_PATH, 
                dpi=DPI,
                low_threshold=LOW_THRESHOLD,
                high_threshold=HIGH_THRESHOLD
            )
            
        print(f"\n所有文件处理完毕！请查看 '{OUTPUT_FOLDER}' 文件夹。")