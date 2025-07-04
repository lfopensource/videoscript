# VideoScript

A Python tool that generates videos from text scripts with custom background images. Each sentence appears sequentially with professional styling and effects.

## Features

- **Text-to-Video Generation**: Convert text scripts into engaging videos
- **Custom Backgrounds**: Use any image as your video background
- **Sequential Display**: Each sentence appears one at a time for better readability
- **Professional Styling**: Includes text shadows, center alignment, and automatic line wrapping
- **Multiple Formats**: Support for various image and video formats
- **Customizable**: Adjustable timing, font size, and video dimensions

## Installation

### Prerequisites
- Python 3.6 or higher
- pip package manager

### Install Dependencies
```bash
git clone https://github.com/lfopensource/videoscript.git
cd videoscript
pip install -r requirements.txt
```

## Quick Start

### Basic Usage
```python
from subtitle_video_maker import create_text_video

# Your script content
script = """
Welcome to my presentation.
This is the first key point.
Here's the second important message.
Thank you for watching!
"""

# Generate video
create_text_video(
    script_text=script,
    background_image_path="your_background.jpg",
    output_path="my_video.mp4"
)
```

### Command Line Usage
```bash
python subtitle_video_maker.py
```

## Configuration

You can customize various aspects of the video generation:

```python
# Video dimensions
video_width = 1280
video_height = 720

# Timing
sentence_duration = 3  # seconds per sentence
fps = 24

# Text styling
font_size = 48
```

## File Structure

```
videoscript/
├── subtitle_video_maker.py    # Main script
├── requirements.txt           # Dependencies
├── README.md                 # This file
├── background.jpg            # Your background image
└── output_video.mp4          # Generated video
```

## Supported Formats

### Input
- **Images**: JPG, PNG, BMP, GIF
- **Text**: UTF-8 encoded text files or strings

### Output
- **Video**: MP4, AVI, MOV (MP4 recommended)

## Examples

### Example 1: Basic Video
```python
script = "Hello world. This is my first video. Thank you for watching."
create_text_video(script, "background.jpg", "hello.mp4")
```

### Example 2: Custom Parameters
```python
# Longer display time for each sentence
create_text_video(
    script_text="Sentence one. Sentence two.",
    background_image_path="bg.jpg",
    output_path="custom.mp4"
)
```

### Example 3: Batch Processing
```python
scripts = [
    "First video content. Point one. Point two.",
    "Second video content. Different topic. Conclusion."
]

for i, script in enumerate(scripts):
    create_text_video(script, f"bg_{i}.jpg", f"video_{i}.mp4")
```

## Text Formatting

- Use periods (`.` or `。`) to separate sentences
- Long sentences automatically wrap to fit screen width
- Supports both English and Chinese text
- Empty sentences are automatically filtered out

## Troubleshooting

### Common Issues

**Font Problems**
- Windows: Ensure `arial.ttf` or `simhei.ttf` is available
- macOS: May require font path adjustments
- Linux: Install Chinese font packages if needed

**Image Loading Issues**
- Verify image file path and format
- Ensure sufficient disk space
- Check file permissions

**Video Export Problems**
- Install FFmpeg if encountering codec issues
- Ensure output directory is writable
- Check available disk space

### Error Messages

```bash
# If you see import errors
pip install --upgrade moviepy pillow numpy

# If video export fails
# Install FFmpeg: https://ffmpeg.org/download.html
```

## Advanced Usage

### Custom Font
```python
# Modify the font loading section in create_text_clip()
font = ImageFont.truetype("path/to/your/font.ttf", font_size)
```

### Different Video Resolutions
```python
# For Instagram Stories (9:16)
video_width = 1080
video_height = 1920

# For YouTube (16:9)
video_width = 1920
video_height = 1080
```

## Performance Tips

- Use compressed background images to reduce processing time
- Shorter scripts process faster
- Lower resolution videos render more quickly
- Close other applications when processing long videos

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Development Setup
```bash
git clone https://github.com/lfopensource/videoscript.git
cd videoscript
pip install -r requirements.txt
```

### Submitting Changes
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

If you encounter any issues or have questions:
- Open an issue on GitHub
- Check the troubleshooting section above
- Review existing issues for solutions

## Roadmap

- [ ] Command line interface
- [ ] Multiple font support
- [ ] Transition effects between sentences
- [ ] Background music integration
- [ ] Subtitle file format support (SRT, VTT)
- [ ] Video templates
- [ ] Batch processing GUI

## Acknowledgments

Built with:
- [MoviePy](https://github.com/Zulko/moviepy) - Video processing
- [Pillow](https://github.com/python-pillow/Pillow) - Image manipulation
- [NumPy](https://github.com/numpy/numpy) - Array operations

---

**Made with ❤️ by lfopensource**

Star ⭐ this repository if you find it useful!
