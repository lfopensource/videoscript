VideoScript 使用指南
项目地址
GitHub: https://github.com/lfopensource/videoscript
安装依赖
首先确保你的系统已安装Python 3.6+，然后安装所需的依赖包：
bashpip install moviepy pillow numpy
使用方法
1. 克隆项目
bashgit clone https://github.com/lfopensource/videoscript.git
cd videoscript
2. 准备素材

背景图片：任何常见格式（jpg, png, bmp等）
字幕文本：准备要显示的文字内容

3. 修改代码使用
方法一：直接修改脚本
打开 subtitle_video_maker.py，找到文件底部的示例代码，修改以下部分：
python# 修改你的字幕内容
sample_script = """
你的第一句话。
你的第二句话。
你的第三句话。
"""

# 修改背景图片路径
background_path = "你的背景图片.jpg"  # 替换为实际路径
方法二：创建独立的使用脚本
创建一个新文件 my_video.py：
pythonfrom subtitle_video_maker import create_text_video

# 你的字幕内容
script_text = """
欢迎观看我的视频。
这是第一个要点。
这是第二个要点。
感谢观看！
"""

# 背景图片路径
background_image = "background.jpg"

# 生成视频
create_text_video(
    script_text=script_text,
    background_image_path=background_image,
    output_path="my_output_video.mp4"
)
4. 运行生成视频
bashpython subtitle_video_maker.py
# 或者
python my_video.py
自定义参数
你可以修改以下参数来自定义视频效果：
pythondef create_text_video(script_text, background_image_path, output_path="output_video.mp4"):
    # 视频尺寸
    video_width = 1280
    video_height = 720
    
    # 帧率
    fps = 24
    
    # 每句话显示时长（秒）
    sentence_duration = 3
    
    # 字体大小
    font_size = 48
文件结构示例
videoscript/
├── subtitle_video_maker.py    # 主程序文件
├── background.jpg             # 背景图片
├── my_video.py               # 你的使用脚本
└── output_video.mp4          # 生成的视频文件
支持的文件格式

背景图片：jpg, jpeg, png, bmp, gif等
输出视频：mp4, avi, mov等（推荐mp4）

文字格式说明

使用中文句号 。 或英文句号 . 来分割句子
每句话会单独显示
长句子会自动换行
支持中英文混合

故障排除
1. 字体问题
如果文字显示异常，可能是字体问题：

Windows：确保有 arial.ttf 或 simhei.ttf
Mac：可能需要调整字体路径
Linux：安装中文字体包

2. 背景图片问题

确保图片路径正确
支持常见图片格式
如果图片加载失败，会自动创建默认背景

3. 视频导出问题

确保有足够的磁盘空间
某些系统可能需要安装FFmpeg

高级用法
批量处理
pythonscripts = [
    "第一个视频的内容。句子一。句子二。",
    "第二个视频的内容。句子一。句子二。",
]

backgrounds = ["bg1.jpg", "bg2.jpg"]

for i, (script, bg) in enumerate(zip(scripts, backgrounds)):
    create_text_video(script, bg, f"video_{i+1}.mp4")
自定义显示时长
python# 修改 sentence_duration 参数
sentence_duration = 5  # 每句话显示5秒
示例效果
生成的视频将会：

以你的图片作为背景
逐句显示字幕内容
每句话居中显示，带阴影效果
自动换行适应屏幕宽度
导出为高质量MP4视频

贡献
欢迎提交Issue和Pull Request到：
https://github.com/lfopensource/videoscript
