from moviepy.editor import *
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import whisper
import re

class AdvancedVideoGenerator:
    def __init__(self):
        # 加载whisper模型用于字幕对齐
        self.whisper_model = whisper.load_model("base")
    
    def segment_text_by_time(self, audio_path, text):
        """
        使用whisper对文本进行时间分段
        """
        result = self.whisper_model.transcribe(audio_path)
        segments = result["segments"]
        
        # 将文本按句子分割
        sentences = re.split(r'[。！？.!?]', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        # 简单的时间分配（可以改进）
        subtitle_segments = []
        for i, sentence in enumerate(sentences):
            if i < len(segments):
                start_time = segments[i]["start"]
                end_time = segments[i]["end"]
            else:
                # 如果whisper段落不够，按比例分配
                duration_per_sentence = len(sentence) / sum(len(s) for s in sentences)
                start_time = i * duration_per_sentence
                end_time = (i + 1) * duration_per_sentence
            
            subtitle_segments.append({
                "text": sentence,
                "start": start_time,
                "end": end_time
            })
        
        return subtitle_segments
    
    def create_background_with_waveform(self, audio_path, size=(1920, 1080)):
        """
        创建带音频波形的背景
        """
        audio = AudioFileClip(audio_path)
        duration = audio.duration
        
        def make_frame(t):
            # 创建基础背景
            img = Image.new('RGB', size, (20, 25, 40))
            draw = ImageDraw.Draw(img)
            
            # 添加动态元素（简单的进度条）
            progress = t / duration
            bar_width = int(size[0] * 0.8 * progress)
            bar_height = 10
            bar_y = size[1] - 100
            
            draw.rectangle([
                (size[0] * 0.1, bar_y),
                (size[0] * 0.1 + bar_width, bar_y + bar_height)
            ], fill=(70, 130, 180))
            
            # 添加装饰圆点
            for i in range(5):
                x = size[0] * 0.1 + i * size[0] * 0.2
                y = size[1] * 0.3 + np.sin(t * 2 + i) * 50
                draw.ellipse([x-20, y-20, x+20, y+20], fill=(100, 149, 237))
            
            return np.array(img)
        
        return VideoClip(make_frame, duration=duration)
    
    def create_advanced_video(self, text_audio_path, background_music_path, 
                            output_path, full_text):
        """
        创建高级视频with分段字幕
        """
        # 1. 加载音频
        speech_audio = AudioFileClip(text_audio_path)
        duration = speech_audio.duration
        
        # 2. 创建动态背景
        background_clip = self.create_background_with_waveform(text_audio_path)
        
        # 3. 生成分段字幕
        subtitle_segments = self.segment_text_by_time(text_audio_path, full_text)
        
        # 4. 创建字幕clips
        subtitle_clips = []
        for segment in subtitle_segments:
            txt_clip = TextClip(segment["text"],
                              fontsize=45,
                              color='white',
                              font='Arial-Bold',
                              stroke_color='black',
                              stroke_width=2,
                              method='caption',
                              size=(1400, None),
                              align='center')
            
            txt_clip = txt_clip.set_position(('center', 'bottom')).set_start(segment["start"]).set_duration(segment["end"] - segment["start"])
            subtitle_clips.append(txt_clip)
        
        # 5. 处理背景音乐
        if background_music_path:
            bg_music = AudioFileClip(background_music_path)
            if bg_music.duration < duration:
                bg_music = bg_music.loop(duration=duration)
            else:
                bg_music = bg_music.subclip(0, duration)
            
            # 添加淡入淡出效果
            bg_music = bg_music.volumex(0.25).audio_fadeout(2)
            final_audio = CompositeAudioClip([speech_audio, bg_music])
        else:
            final_audio = speech_audio
        
        # 6. 组合所有元素
        video = CompositeVideoClip([background_clip] + subtitle_clips)
        video = video.set_audio(final_audio)
        
        # 7. 输出视频
        video.write_videofile(output_path, 
                             fps=24, 
                             codec='libx264',
                             audio_codec='aac',
                             temp_audiofile='temp-audio.m4a',
                             remove_temp=True)
        
        print(f"高级视频已生成: {output_path}")

# 使用示例
if __name__ == "__main__":
    generator = AdvancedVideoGenerator()
    
    # 配置
    text_audio = "speech.mp3"
    bg_music = "background.mp3"
    output_video = "advanced_video.mp4"
    full_text = "这里是你的完整文本内容。可以是多句话。每句话会自动分段显示。"
    
    generator.create_advanced_video(text_audio, bg_music, output_video, full_text)
