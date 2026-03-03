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
model = WhisperModel("base", device="cpu")  # Use "cuda" when CUDA 12 is installed (see README)

print(f"Transcribing: {audio_path}")
print("(On CPU this can take a while for long files; you'll see progress below.)")
segments, info = model.transcribe(audio_path)

with open(output_path, "w", encoding="utf-8") as f:
    for i, segment in enumerate(segments):
        f.write(segment.text)
        # Progress: show every 10th segment or first few so it's clear something is happening
        if i < 3 or (i + 1) % 10 == 0 or segment.end and segment.end > 0:
            mins = int(segment.end // 60) if segment.end else 0
            secs = int(segment.end % 60) if segment.end else 0
            print(f"  ... segment {i + 1} (up to ~{mins}:{secs:02d})")

print(f"Done. Transcript saved to: {os.path.abspath(output_path)}")
