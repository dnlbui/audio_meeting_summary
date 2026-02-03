import os
import sys
import subprocess
import imageio_ffmpeg

# Require video file path as argument
if len(sys.argv) < 2:
    print("Usage: python extract_audio.py <video_file>")
    sys.exit(1)

video_path = sys.argv[1]

# Output audio: same base name as video, .mp3, in current directory
base_name = os.path.splitext(os.path.basename(video_path))[0]
output_path = base_name + ".mp3"

# Check if video file exists
if not os.path.exists(video_path):
    print(f"Error: Video file not found at {video_path}")
    exit(1)

print(f"Extracting audio from: {video_path}")
print("This may take a moment...")

try:
    # Get the ffmpeg executable path from imageio_ffmpeg
    ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()
    
    # Use ffmpeg to extract audio
    command = [
        ffmpeg_path,
        "-i", video_path,
        "-vn",  # No video
        "-acodec", "libmp3lame",  # MP3 codec
        "-ab", "192k",  # Audio bitrate
        "-ar", "44100",  # Sample rate
        "-y",  # Overwrite output file if it exists
        output_path
    ]
    
    # Run ffmpeg
    result = subprocess.run(command, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"\nSuccess! Audio extracted to: {os.path.abspath(output_path)}")
    else:
        print(f"Error extracting audio:")
        print(result.stderr)
        exit(1)
    
except Exception as e:
    print(f"Error extracting audio: {e}")
    exit(1)

