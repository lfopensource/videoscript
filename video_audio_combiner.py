#!/usr/bin/env python3
"""
Video Audio Combiner
Combines video file with audio and background music into a final output video.
"""

import os
import sys
from pathlib import Path
import argparse
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip

def find_files_in_downloads():
    """
    Automatically find video, audio, and BGM files in the Downloads folder.
    Returns a dictionary with file paths.
    """
    # Get Downloads folder path
    downloads_path = Path.home() / "Downloads"
    
    if not downloads_path.exists():
        print(f"Downloads folder not found at: {downloads_path}")
        return None
    
    # Define supported file extensions
    video_extensions = ['.mp4', '.avi', '.mov', '.mkv', '.webm']
    audio_extensions = ['.mp3', '.wav', '.aac', '.m4a', '.flac']
    
    files = {
        'video': [],
        'audio': [],
        'bgm': []
    }
    
    # Search for files in Downloads folder
    for file_path in downloads_path.glob("*"):
        if file_path.is_file():
            file_ext = file_path.suffix.lower()
            file_name = file_path.name.lower()
            
            if file_ext in video_extensions:
                files['video'].append(file_path)
            elif file_ext in audio_extensions:
                if 'bgm' in file_name or 'background' in file_name or 'music' in file_name:
                    files['bgm'].append(file_path)
                else:
                    files['audio'].append(file_path)
    
    return files

def list_found_files(files):
    """Display found files to user for selection."""
    print("\n=== Found Files ===")
    
    for file_type, file_list in files.items():
        print(f"\n{file_type.upper()} files:")
        if file_list:
            for i, file_path in enumerate(file_list, 1):
                print(f"  {i}. {file_path.name}")
        else:
            print("  None found")

def select_files(files):
    """Allow user to select which files to use."""
    selected = {}
    
    for file_type, file_list in files.items():
        if not file_list:
            print(f"\nNo {file_type} files found!")
            continue
        
        if len(file_list) == 1:
            selected[file_type] = file_list[0]
            print(f"\nUsing {file_type}: {file_list[0].name}")
        else:
            print(f"\nSelect {file_type} file:")
            for i, file_path in enumerate(file_list, 1):
                print(f"  {i}. {file_path.name}")
            
            while True:
                try:
                    choice = int(input(f"Enter choice (1-{len(file_list)}): ")) - 1
                    if 0 <= choice < len(file_list):
                        selected[file_type] = file_list[choice]
                        break
                    else:
                        print("Invalid choice. Please try again.")
                except ValueError:
                    print("Please enter a valid number.")
    
    return selected

def combine_audio_video(video_path, audio_path, bgm_path=None, output_path=None, 
                       audio_volume=1.0, bgm_volume=0.3, fade_duration=1.0):
    """
    Combine video with audio and optional background music.
    
    Args:
        video_path: Path to video file
        audio_path: Path to main audio file
        bgm_path: Path to background music file (optional)
        output_path: Output file path
        audio_volume: Volume level for main audio (0.0 to 1.0)
        bgm_volume: Volume level for background music (0.0 to 1.0)
        fade_duration: Fade in/out duration in seconds
    """
    
    print(f"\n=== Processing Files ===")
    print(f"Video: {video_path.name}")
    print(f"Audio: {audio_path.name}")
    if bgm_path:
        print(f"BGM: {bgm_path.name}")
    
    try:
        # Load video clip
        print("\nLoading video...")
        video = VideoFileClip(str(video_path))
        video_duration = video.duration
        
        # Load main audio
        print("Loading audio...")
        audio = AudioFileClip(str(audio_path))
        
        # Adjust audio to match video duration
        if audio.duration > video_duration:
            print(f"Trimming audio to match video duration ({video_duration:.2f}s)")
            audio = audio.subclip(0, video_duration)
        elif audio.duration < video_duration:
            print(f"Audio is shorter than video. Extending audio.")
            # Loop audio to match video duration
            loops_needed = int(video_duration / audio.duration) + 1
            audio = audio.loop(duration=video_duration)
        
        # Apply volume and fade to main audio
        audio = audio.volumex(audio_volume)
        if fade_duration > 0:
            audio = audio.fadein(fade_duration).fadeout(fade_duration)
        
        # Prepare final audio
        final_audio = audio
        
        # Add background music if provided
        if bgm_path:
            print("Loading background music...")
            bgm = AudioFileClip(str(bgm_path))
            
            # Loop BGM to match video duration
            if bgm.duration < video_duration:
                loops_needed = int(video_duration / bgm.duration) + 1
                bgm = bgm.loop(duration=video_duration)
            else:
                bgm = bgm.subclip(0, video_duration)
            
            # Apply volume and fade to BGM
            bgm = bgm.volumex(bgm_volume)
            if fade_duration > 0:
                bgm = bgm.fadein(fade_duration).fadeout(fade_duration)
            
            # Combine audio and BGM
            print("Mixing audio tracks...")
            final_audio = CompositeAudioClip([audio, bgm])
        
        # Set the final audio to video
        print("Combining video with audio...")
        final_video = video.set_audio(final_audio)
        
        # Generate output filename if not provided
        if output_path is None:
            output_path = video_path.parent / f"combined_{video_path.stem}.mp4"
        
        # Write the final video
        print(f"\nExporting final video to: {output_path}")
        print("This may take a while depending on video length...")
        
        final_video.write_videofile(
            str(output_path),
            codec='libx264',
            audio_codec='aac',
            temp_audiofile='temp-audio.m4a',
            remove_temp=True,
            verbose=False,
            logger=None
        )
        
        print(f"\n✅ Success! Combined video saved as: {output_path}")
        
        # Clean up
        video.close()
        audio.close()
        if bgm_path:
            bgm.close()
        final_video.close()
        
        return output_path
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        return None

def main():
    """Main function to run the video combiner."""
    parser = argparse.ArgumentParser(description='Combine video with audio and background music')
    parser.add_argument('--video', type=str, help='Path to video file')
    parser.add_argument('--audio', type=str, help='Path to audio file')
    parser.add_argument('--bgm', type=str, help='Path to background music file')
    parser.add_argument('--output', type=str, help='Output file path')
    parser.add_argument('--audio-volume', type=float, default=1.0, help='Main audio volume (0.0-1.0)')
    parser.add_argument('--bgm-volume', type=float, default=0.3, help='Background music volume (0.0-1.0)')
    parser.add_argument('--fade', type=float, default=1.0, help='Fade in/out duration in seconds')
    
    args = parser.parse_args()
    
    print("🎬 Video Audio Combiner")
    print("=" * 30)
    
    # Check if moviepy is installed
    try:
        import moviepy
    except ImportError:
        print("❌ Error: moviepy is not installed.")
        print("Please install it using: pip install moviepy")
        sys.exit(1)
    
    selected_files = {}
    
    # Use command line arguments if provided
    if args.video and args.audio:
        selected_files['video'] = Path(args.video)
        selected_files['audio'] = Path(args.audio)
        if args.bgm:
            selected_files['bgm'] = Path(args.bgm)
    else:
        # Auto-detect files in Downloads folder
        print("Searching for files in Downloads folder...")
        files = find_files_in_downloads()
        
        if files is None:
            sys.exit(1)
        
        list_found_files(files)
        
        if not files['video'] or not files['audio']:
            print("\n❌ Error: Need at least one video file and one audio file.")
            sys.exit(1)
        
        selected_files = select_files(files)
    
    # Verify required files exist
    if 'video' not in selected_files or 'audio' not in selected_files:
        print("❌ Error: Video and audio files are required.")
        sys.exit(1)
    
    # Set up parameters
    video_path = selected_files['video']
    audio_path = selected_files['audio']
    bgm_path = selected_files.get('bgm')
    output_path = Path(args.output) if args.output else None
    
    # Combine the files
    result = combine_audio_video(
        video_path=video_path,
        audio_path=audio_path,
        bgm_path=bgm_path,
        output_path=output_path,
        audio_volume=args.audio_volume,
        bgm_volume=args.bgm_volume,
        fade_duration=args.fade
    )
    
    if result:
        print(f"\n🎉 Final video is ready: {result}")
        print("\nYou can now use your combined video!")
    else:
        print("\n❌ Failed to create combined video.")
        sys.exit(1)

if __name__ == "__main__":
    main()