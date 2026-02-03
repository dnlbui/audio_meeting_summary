# Audio Meeting Summary

Extract audio from video (e.g. OBS recordings) and transcribe it to text using free, local tools—no API keys required.

## What’s in this repo

- **`extract_audio.py`** – Pulls audio from an MP4 (or other video) and saves it as MP3. Uses ffmpeg via `imageio_ffmpeg`.
- **`transcribe.py`** – Transcribes an audio file to a `.txt` transcript. Uses [faster-whisper](https://github.com/SYSTRAN/faster-whisper) (Whisper running locally on CPU or GPU).

## Install

### 1. Python

- Use **Python 3.10+**.
- Ensure `python` and `pip` are on your PATH.

### 2. Dependencies for both scripts

```bash
pip install imageio-ffmpeg
pip install faster-whisper
```

- **`imageio-ffmpeg`** – Used by `extract_audio.py`. It ships a bundled ffmpeg binary so you don’t install ffmpeg yourself. It’s only used to extract audio from video.
- **`faster-whisper`** – Used by `transcribe.py`. It pulls in the Whisper model runtime (CTranslate2, ONNX, etc.) and Hugging Face Hub to download the model. The first time you run transcription, it will download the Whisper model (see below).

### 3. What gets downloaded (high level)

| When | What | Where it goes | What it’s for |
|------|------|----------------|---------------|
| `pip install imageio-ffmpeg` | FFmpeg binary + Python bindings | Your Python `site-packages` | Extracting audio from video in `extract_audio.py`. |
| `pip install faster-whisper` | Python package + CTranslate2, ONNX Runtime, Hugging Face Hub, etc. | Your Python `site-packages` | Running Whisper and downloading the model in `transcribe.py`. |
| First run of `transcribe.py` | Whisper **“base” model** (~150 MB) | `~/.cache/huggingface/hub/` (or similar) | The actual speech-to-text model. Cached so later runs don’t re-download. |

So: **two kinds of downloads** — (1) **pip packages** (code + ffmpeg binary + Whisper runtime), and (2) the **Whisper model weights** the first time you transcribe.

## Usage

Pass the **full path** to the file. No default paths.

### Extract audio from a video

```bash
python extract_audio.py "C:\path\to\your\recording.mp4"
```

- Output: same directory as the script, same base name as the video, with `.mp3` (e.g. `recording.mp3`).

### Transcribe audio to text

```bash
python transcribe.py "C:\path\to\your\audio.mp3"
```

- Output: same directory as the script, same base name as the audio, with `.txt` (e.g. `audio.txt`).
- First run will download the Whisper model; later runs use the cache.

### Example workflow

```bash
python extract_audio.py "C:\Users\you\Videos\meeting.mp4"
python transcribe.py "C:\Users\you\Documents\Personal_Project\audio_meeting_summary\meeting.mp3"
```

## Notes

- **Transcription device:** The script uses `device="cpu"` by default. If you have an NVIDIA GPU and CUDA set up, you can change to `device="cuda"` in `transcribe.py` for faster runs.
- **Model size:** The default Whisper model is `"base"`. For better accuracy (slower, more RAM), you can switch to `"small"` or `"medium"` in `transcribe.py`.
- **Speaker labels:** Whisper does not identify speakers. To get “Speaker 1 / Speaker 2” style output, you’d need to add a separate diarization step (e.g. pyannote-audio).

## Publish to GitHub

1. Create a **new repository** on [GitHub](https://github.com/new) (e.g. `audio_meeting_summary`). Do not add a README or .gitignore—this repo already has them.
2. In this folder, add the remote and push:

   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/audio_meeting_summary.git
   git branch -M main
   git push -u origin main
   ```

   Replace `YOUR_USERNAME` and `audio_meeting_summary` with your GitHub username and repo name. Use the SSH URL if you prefer: `git@github.com:YOUR_USERNAME/audio_meeting_summary.git`.

## License

Use and modify as you like.
