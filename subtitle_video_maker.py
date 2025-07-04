import os
from moviepy.editor import *
from PIL import Image, ImageDraw, ImageFont
import numpy as np

def create_text_video(script_text, background_image_path, output_path="output_video.mp4"):
    """
    创建一个视频，逐句显示文字，背景为指定图片
    
    参数:
    script_text: 要显示的文字内容（字符串）
    background_image_path: 背景图片路径
    output_path: 输出视频路径
    """
    
    # 设置视频参数
    video_width = 1280
    video_height = 720
    fps = 24
    sentence_duration = 3  # 每句话显示3秒
    
    # 分割文字为句子
    sentences = [s.strip() for s in script_text.split('。') if s.strip()]
    if not sentences:
        sentences = [s.strip() for s in script_text.split('.') if s.strip()]
    
    print(f"共有 {len(sentences)} 句话")
    
    # 加载背景图片
    try:
        background = Image.open(background_image_path)
        # 调整背景图片大小
        background = background.resize((video_width, video_height), Image.Resampling.LANCZOS)
        background_array = np.array(background)
    except Exception as e:
        print(f"无法加载背景图片: {e}")
        # 如果图片加载失败，创建纯色背景
        background_array = np.full((video_height, video_width, 3), [50, 50, 50], dtype=np.uint8)
    
    # 创建视频片段列表
    clips = []
    
    for i, sentence in enumerate(sentences):
        print(f"处理第 {i+1} 句: {sentence[:30]}...")
        
        # 创建文字图片
        text_clip = create_text_clip(sentence, background_array, video_width, video_height)
        
        # 设置显示时间
        text_clip = text_clip.set_duration(sentence_duration)
        
        clips.append(text_clip)
    
    # 合并所有片段
    final_video = concatenate_videoclips(clips)
    
    # 导出视频
    print("开始导出视频...")
    final_video.write_videofile(
        output_path,
        fps=fps,
        codec='libx264',
        audio_codec='aac'
    )
    
    print(f"视频已保存到: {output_path}")
    return output_path

def create_text_clip(text, background_array, width, height):
    """
    创建单个文字片段
    """
    # 复制背景
    frame = background_array.copy()
    
    # 转换为PIL图像以便添加文字
    img = Image.fromarray(frame)
    draw = ImageDraw.Draw(img)
    
    # 设置字体（你可能需要调整字体路径）
    try:
        # 尝试使用系统字体
        font_size = 48
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        try:
            # 如果Arial不可用，尝试其他字体
            font = ImageFont.truetype("simhei.ttf", font_size)  # 黑体
        except:
            # 使用默认字体
            font = ImageFont.load_default()
    
    # 文字换行处理
    wrapped_text = wrap_text(text, font, width - 100)
    
    # 计算文字位置（居中）
    text_bbox = draw.multiline_textbbox((0, 0), wrapped_text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    x = (width - text_width) // 2
    y = (height - text_height) // 2
    
    # 添加文字阴影
    shadow_offset = 2
    draw.multiline_text((x + shadow_offset, y + shadow_offset), wrapped_text, 
                       font=font, fill=(0, 0, 0, 128), align='center')
    
    # 添加主文字
    draw.multiline_text((x, y), wrapped_text, font=font, fill=(255, 255, 255), align='center')
    
    # 转换回numpy数组
    frame_with_text = np.array(img)
    
    # 创建moviepy的ImageClip
    clip = ImageClip(frame_with_text, duration=1)
    
    return clip

def wrap_text(text, font, max_width):
    """
    文字换行处理
    """
    lines = []
    words = text.split()
    current_line = []
    
    for word in words:
        test_line = ' '.join(current_line + [word])
        # 创建临时Image来测试文字宽度
        temp_img = Image.new('RGB', (1, 1))
        temp_draw = ImageDraw.Draw(temp_img)
        bbox = temp_draw.textbbox((0, 0), test_line, font=font)
        text_width = bbox[2] - bbox[0]
        
        if text_width <= max_width:
            current_line.append(word)
        else:
            if current_line:
                lines.append(' '.join(current_line))
                current_line = [word]
            else:
                lines.append(word)
    
    if current_line:
        lines.append(' '.join(current_line))
    
    return '\n'.join(lines)

# 示例使用
if __name__ == "__main__":
    # 示例文字内容
    sample_script = """
    欢迎来到我们的视频演示。这是第一句话。
    现在我们展示第二句话的效果。
    每句话都会在屏幕上停留几秒钟。
    背景图片可以是任何你喜欢的图片。
    这个程序可以轻松地创建文字视频。
    """
    
    # 背景图片路径（请替换为你的图片路径）
    background_path = "background.jpg"  # 请确保这个文件存在
    
    # 如果没有背景图片，创建一个示例图片
    if not os.path.exists(background_path):
        print("创建示例背景图片...")
        # 创建一个渐变背景
        img = Image.new('RGB', (1280, 720), color=(70, 130, 180))
        draw = ImageDraw.Draw(img)
        
        # 添加一些装饰性图形
        for i in range(0, 1280, 100):
            for j in range(0, 720, 100):
                color = (70 + i//20, 130 + j//20, 180 + (i+j)//40)
                draw.rectangle([i, j, i+50, j+50], fill=color)
        
        img.save(background_path)
        print(f"示例背景图片已创建: {background_path}")
    
    # 创建视频
    try:
        output_file = create_text_video(sample_script, background_path, "my_text_video.mp4")
        print(f"视频创建成功！输出文件: {output_file}")
    except Exception as e:
        print(f"创建视频时出错: {e}")
        print("请确保安装了所需的依赖包:")
        print("pip install moviepy pillow numpy")
