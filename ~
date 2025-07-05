import os
from moviepy.editor import *
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import re

def create_text_video(script_text, background_image_path, output_path="output_video.mp4"):
    """
    Create a video that displays text segments separated by commas with a background image
    
    Args:
    script_text: Text content to display (string)
    background_image_path: Path to background image
    output_path: Output video file path
    """
    
    # Set video parameters
    video_width = 1280
    video_height = 720
    fps = 24
    segment_duration = 2  # Display each segment for 2 seconds
    
    # Split text by commas
    segments = split_by_comma(script_text)
    
    print(f"Total segments: {len(segments)}")
    for i, segment in enumerate(segments):
        print(f"Segment {i+1}: {segment}")
    
    # Load background image
    try:
        background = Image.open(background_image_path)
        # Resize background image
        background = background.resize((video_width, video_height), Image.Resampling.LANCZOS)
        background_array = np.array(background)
    except Exception as e:
        print(f"Cannot load background image: {e}")
        # If image loading fails, create a solid color background
        background_array = np.full((video_height, video_width, 3), [50, 50, 50], dtype=np.uint8)
    
    # Create video clip list
    clips = []
    
    for i, segment in enumerate(segments):
        print(f"Processing segment {i+1}: {segment[:30]}...")
        
        # Create text clip
        text_clip = create_text_clip(segment, background_array, video_width, video_height)
        
        # Set display duration
        text_clip = text_clip.set_duration(segment_duration)
        
        clips.append(text_clip)
    
    # Concatenate all clips
    final_video = concatenate_videoclips(clips)
    
    # Export video
    print("Starting video export...")
    final_video.write_videofile(
        output_path,
        fps=fps,
        codec='libx264',
        audio_codec='aac'
    )
    
    print(f"Video saved to: {output_path}")
    return output_path

def split_by_comma(text):
    """
    Split text by commas, supports both English and Chinese punctuation
    """
    # Clean text
    text = text.strip()
    
    # Use regex to split, supporting both English and Chinese commas and periods
    # Preserve delimiters
    segments = re.split(r'([,，。.])', text)
    
    # Recombine to ensure each segment includes its following punctuation
    result = []
    current_segment = ""
    
    for i, part in enumerate(segments):
        if part.strip():  # Skip empty strings
            if part in ',，。.':  # If it's a delimiter
                if current_segment:
                    current_segment += part
                    result.append(current_segment.strip())
                    current_segment = ""
            else:  # If it's text content
                current_segment += part
    
    # Handle the last segment (may not have punctuation)
    if current_segment.strip():
        result.append(current_segment.strip())
    
    # Filter out empty segments or segments with only punctuation
    result = [seg for seg in result if seg and not seg in ',，。.']
    
    return result

def create_text_clip(text, background_array, width, height):
    """
    Create a single text clip with background
    """
    # Copy background
    frame = background_array.copy()
    
    # Convert to PIL image for text rendering
    img = Image.fromarray(frame)
    draw = ImageDraw.Draw(img)
    
    # Set font
    try:
        font_size = 48
        font = ImageFont.truetype("arial.ttf", font_size)
    except:
        try:
            font = ImageFont.truetype("simhei.ttf", font_size)
        except:
            font = ImageFont.load_default()
    
    # Text wrapping
    wrapped_text = wrap_text(text, font, width - 100)
    
    # Calculate text position (center alignment)
    text_bbox = draw.multiline_textbbox((0, 0), wrapped_text, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    x = (width - text_width) // 2
    y = (height - text_height) // 2
    
    # Add text shadow
    shadow_offset = 2
    draw.multiline_text((x + shadow_offset, y + shadow_offset), wrapped_text, 
                       font=font, fill=(0, 0, 0, 128), align='center')
    
    # Add main text
    draw.multiline_text((x, y), wrapped_text, font=font, fill=(255, 255, 255), align='center')
    
    # Convert back to numpy array
    frame_with_text = np.array(img)
    
    # Create moviepy ImageClip
    clip = ImageClip(frame_with_text, duration=1)
    
    return clip

def wrap_text(text, font, max_width):
    """
    Text wrapping functionality
    """
    lines = []
    words = text.split()
    current_line = []
    
    for word in words:
        test_line = ' '.join(current_line + [word])
        # Create temporary Image to test text width
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

def create_progressive_text_video(script_text, background_image_path, output_path="progressive_video.mp4"):
    """
    Create a video with progressive text display, where each frame shows all content up to the current comma
    """
    # Set video parameters
    video_width = 1280
    video_height = 720
    fps = 24
    segment_duration = 2
    
    # Split text by commas
    segments = split_by_comma(script_text)
    
    # Create cumulative display text list
    progressive_texts = []
    accumulated_text = ""
    
    for segment in segments:
        if accumulated_text:
            accumulated_text += " " + segment
        else:
            accumulated_text = segment
        progressive_texts.append(accumulated_text)
    
    print(f"Progressive display stages: {len(progressive_texts)}")
    
    # Load background image
    try:
        background = Image.open(background_image_path)
        background = background.resize((video_width, video_height), Image.Resampling.LANCZOS)
        background_array = np.array(background)
    except Exception as e:
        print(f"Cannot load background image: {e}")
        background_array = np.full((video_height, video_width, 3), [50, 50, 50], dtype=np.uint8)
    
    # Create video clip list
    clips = []
    
    for i, text in enumerate(progressive_texts):
        print(f"Processing stage {i+1}: {text[:50]}...")
        
        # Create text clip
        text_clip = create_text_clip(text, background_array, video_width, video_height)
        text_clip = text_clip.set_duration(segment_duration)
        
        clips.append(text_clip)
    
    # Concatenate all clips
    final_video = concatenate_videoclips(clips)
    
    # Export video
    print("Starting progressive video export...")
    final_video.write_videofile(
        output_path,
        fps=fps,
        codec='libx264',
        audio_codec='aac'
    )
    
    print(f"Progressive video saved to: {output_path}")
    return output_path

# Example usage
if __name__ == "__main__":
    # Sample text content with comma-separated segments
    sample_script = """
    Welcome to our video demonstration, this is a great tool, that can help you create professional video content.
    Now let's look at the first feature, text will be displayed by comma segments, each part will appear separately.
    Next we'll show the second feature, background images can be customized, text will be automatically centered.
    Finally, thank you for watching, hope this tool is helpful to you, thanks!
    """
    
    # Background image path
    background_path = "background.jpg"
    
    # Create sample background image if it doesn't exist
    if not os.path.exists(background_path):
        print("Creating sample background image...")
        img = Image.new('RGB', (1280, 720), color=(70, 130, 180))
        draw = ImageDraw.Draw(img)
        
        # Add some decorative graphics
        for i in range(0, 1280, 100):
            for j in range(0, 720, 100):
                color = (70 + i//20, 130 + j//20, 180 + (i+j)//40)
                draw.rectangle([i, j, i+50, j+50], fill=color)
        
        img.save(background_path)
        print(f"Sample background image created: {background_path}")
    
    # Create both types of videos
    try:
        print("=" * 50)
        print("Creating comma-split video (each comma segment displayed separately)")
        output_file1 = create_text_video(sample_script, background_path, "comma_split_video.mp4")
        print(f"Comma-split video created successfully! Output file: {output_file1}")
        
        print("=" * 50)
        print("Creating progressive video (cumulative display up to current comma)")
        output_file2 = create_progressive_text_video(sample_script, background_path, "progressive_video.mp4")
        print(f"Progressive video created successfully! Output file: {output_file2}")
        
    except Exception as e:
        print(f"Error creating video: {e}")
        print("Please ensure you have installed the required dependencies:")
        print("pip install moviepy pillow numpy")
