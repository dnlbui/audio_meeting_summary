"""
Transcribe audio to text using faster-whisper (free, runs locally).
Usage: python transcribe.py [audio_file.mp3]
"""
import os
import sys
from faster_whisper import WhisperModel

# Require audio file path as argument
if len(sys.argv) < 2:
    print("Usage: python transcribe.py <audio_file>")
    sys.exit(1)

audio_path = sys.argv[1]

if not os.path.exists(audio_path):
    print(f"Error: Audio file not found: {audio_path}")
    sys.exit(1)

# Output: same base name, .txt
base_name = os.path.splitext(os.path.basename(audio_path))[0]
output_path = base_name + ".txt"

print(f"Loading Whisper model (first run downloads ~150MB)...")
model = WhisperModel("base", device="cpu")  # CPU mode; use "cuda" if you have NVIDIA GPU

print(f"Transcribing: {audio_path}")
segments, info = model.transcribe(audio_path)

with open(output_path, "w", encoding="utf-8") as f:
    for segment in segments:
        f.write(segment.text)

print(f"Done. Transcript saved to: {os.path.abspath(output_path)}")
