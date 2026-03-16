import os
import sys
import subprocess
import argparse
import imageio_ffmpeg

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Extract audio from a video file (MP4/MKV/etc) to an MP3."
    )
    parser.add_argument("video_file", help="Path to the input video file")
    parser.add_argument(
        "--out-dir",
        default="outputs",
        help='Base output directory (default: "outputs")',
    )
    parser.add_argument(
        "--bitrate",
        default="192k",
        help='MP3 audio bitrate (default: "192k")',
    )
    parser.add_argument(
        "--sample-rate",
        default=44100,
        type=int,
        help="Audio sample rate in Hz (default: 44100)",
    )
    return parser.parse_args()


args = parse_args()
video_path = args.video_file

# Output audio: outputs/audio/<base>.mp3 by default
base_name = os.path.splitext(os.path.basename(video_path))[0]
audio_dir = os.path.join(args.out_dir, "audio")
os.makedirs(audio_dir, exist_ok=True)
output_path = os.path.join(audio_dir, base_name + ".mp3")

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
        "-ab", args.bitrate,  # Audio bitrate
        "-ar", str(args.sample_rate),  # Sample rate
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

