"""
Transcribe audio to text using faster-whisper (free, runs locally).
Usage: python transcribe.py [audio_file.mp3]
"""
import os
import sys
import argparse
from faster_whisper import WhisperModel

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Transcribe an audio file (MP3/WAV/etc) to a text transcript using faster-whisper."
    )
    parser.add_argument("audio_file", help="Path to the input audio file")
    parser.add_argument(
        "--out-dir",
        default="outputs",
        help='Base output directory (default: "outputs")',
    )
    parser.add_argument(
        "--model",
        default="base",
        help='Whisper model size (default: "base"; try "small" or "medium" for better accuracy)',
    )
    parser.add_argument(
        "--device",
        default="cpu",
        help='Device to run on (default: "cpu"; use "cuda" if available)',
    )
    return parser.parse_args()

args = parse_args()
audio_path = args.audio_file

if not os.path.exists(audio_path):
    print(f"Error: Audio file not found: {audio_path}")
    sys.exit(1)

# Output: outputs/transcripts/<base>.txt by default
base_name = os.path.splitext(os.path.basename(audio_path))[0]
transcript_dir = os.path.join(args.out_dir, "transcripts")
os.makedirs(transcript_dir, exist_ok=True)
output_path = os.path.join(transcript_dir, base_name + ".txt")

print(f"Loading Whisper model (first run downloads ~150MB)...")
model = WhisperModel(args.model, device=args.device)

print(f"Transcribing: {audio_path}")
print("(On CPU this can take a while for long files; you'll see progress below.)")
segments, info = model.transcribe(audio_path)

with open(output_path, "w", encoding="utf-8") as f:
    for i, segment in enumerate(segments):
        f.write(segment.text.strip() + "\n")
        # Progress: show every 10th segment or first few so it's clear something is happening
        if i < 3 or (i + 1) % 10 == 0 or segment.end and segment.end > 0:
            mins = int(segment.end // 60) if segment.end else 0
            secs = int(segment.end % 60) if segment.end else 0
            print(f"  ... segment {i + 1} (up to ~{mins}:{secs:02d})")

print(f"Done. Transcript saved to: {os.path.abspath(output_path)}")
