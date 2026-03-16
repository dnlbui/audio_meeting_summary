# Audio Meeting Summary

Extract audio from video (e.g. OBS recordings) and transcribe it to text using free, local tools—no API keys required.

## What’s in this repo

- **`record_audio.py`** – Records from your microphone to a WAV file. **Cross-platform:** same script on Windows, Linux, and macOS (uses [sounddevice](https://python-sounddevice.readthedocs.io/) / PortAudio).
- **`extract_audio.py`** – Pulls audio from an MP4, MKV, or other video and saves it as MP3. Uses ffmpeg via `imageio_ffmpeg`.
- **`transcribe.py`** – Transcribes an audio file to a `.txt` transcript. Uses [faster-whisper](https://github.com/SYSTRAN/faster-whisper) (Whisper running locally on CPU or GPU).

## Install

### 1. Python

- Use **Python 3.10+**.
- Ensure `python` (Windows) or `python3` (Linux/macOS) and `pip` are on your PATH.

### 2. Virtual environment (recommended on Linux / macOS)

On Linux and macOS, the system Python is often **externally managed** (PEP 668), so `pip install` system-wide will fail. Create a virtual environment in the project directory:

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

On Windows (optional, but keeps things isolated):

```powershell
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt
```

Then run scripts with the venv Python:
- **Linux/macOS:** `.venv/bin/python script.py ...`
- **Windows:** `.venv\Scripts\python.exe script.py ...`

Or activate the venv first (`source .venv/bin/activate` on Linux/macOS, `.venv\Scripts\activate` on Windows), then use `python` as usual.

### 3. Dependencies (without venv, if your system allows)

If you're on Windows and prefer not to use a venv:

```bash
pip install -r requirements.txt
```

- `requirements.txt` pins stable, Python 3.10-compatible versions for this project.
- These pins were checked with `pip-audit` on **2026-02-03** and had **no known vulnerabilities** at that time.
- Re-run this check anytime with:

  ```bash
  python -m pip install --upgrade pip pip-audit
  python -m pip_audit -r requirements.txt
  ```
  (Use `.venv/bin/python -m pip` on Linux/macOS if using the venv.)

- **`sounddevice`** + **`soundfile`** – Used by `record_audio.py`. `sounddevice` uses PortAudio to capture from the microphone (same API on Windows, Linux, macOS). `soundfile` writes the recorded samples to WAV. No extra system install needed beyond pip.
- **`imageio-ffmpeg`** – Used by `extract_audio.py`. It ships a bundled ffmpeg binary so you don’t install ffmpeg yourself. It’s only used to extract audio from video.
- **`faster-whisper`** – Used by `transcribe.py`. It pulls in the Whisper model runtime (CTranslate2, ONNX, etc.) and Hugging Face Hub to download the model. The first time you run transcription, it will download the Whisper model (see below).

### 4. What gets downloaded (high level)

| When | What | Where it goes | What it’s for |
|------|------|----------------|---------------|
| `pip install sounddevice` | PortAudio bindings + Python wrapper | Your Python `site-packages` | Recording from the microphone in `record_audio.py` (same on Windows/Linux/Mac). |
| `pip install soundfile` | libsndfile wrapper | Your Python `site-packages` | Writing recorded samples to WAV in `record_audio.py`. |
| `pip install imageio-ffmpeg` | FFmpeg binary + Python bindings | Your Python `site-packages` | Extracting audio from video in `extract_audio.py`. |
| `pip install faster-whisper` | Python package + CTranslate2, ONNX Runtime, Hugging Face Hub, etc. | Your Python `site-packages` | Running Whisper and downloading the model in `transcribe.py`. |
| First run of `transcribe.py` | Whisper **“base” model** (~150 MB) | `~/.cache/huggingface/hub/` (or similar) | The actual speech-to-text model. Cached so later runs don’t re-download. |

So: **two kinds of downloads** — (1) **pip packages** (code + ffmpeg binary + Whisper runtime), and (2) the **Whisper model weights** the first time you transcribe.

## Usage

Pass the **full path** to the file (or, for recording, the desired output path). No default paths.

Use `python` or `python3` depending on your system. If you created a venv, use `.venv/bin/python` (Linux/macOS) or `.venv\Scripts\python.exe` (Windows) instead.

### Record from the microphone

**Linux/macOS:**
```bash
.venv/bin/python record_audio.py "/home/you/recordings/output.wav"
# or: python3 record_audio.py "/home/you/recordings/output.wav"
```

**Windows:**
```powershell
.venv\Scripts\python.exe record_audio.py "C:\path\to\output.wav"
# or: python record_audio.py "C:\path\to\output.wav"
```

- Records from the **default input device** until you press **Ctrl+C**. Output is WAV (e.g. for use with `transcribe.py`; you can transcribe WAV directly).

To record for a fixed length (e.g. 60 seconds):

```bash
.venv/bin/python record_audio.py "output.wav" 60
```

- Same script works on **Windows, Linux, and macOS**; PortAudio picks the right microphone API per OS.

### Extract audio from a video

**Linux/macOS:**
```bash
.venv/bin/python extract_audio.py "/path/to/recording.mp4"
# Supports MP4, MKV, and other formats ffmpeg handles
```

**Windows:**
```powershell
.venv\Scripts\python.exe extract_audio.py "C:\path\to\recording.mp4"
```

- Output: same directory as the script (current directory), same base name as the video, with `.mp3` (e.g. `recording.mp3`).
- Default output: `outputs/audio/<video_basename>.mp3` (use `--out-dir` to change).

### Transcribe audio to text

**Linux/macOS:**
```bash
.venv/bin/python transcribe.py "/path/to/audio.mp3"
```

**Windows:**
```powershell
.venv\Scripts\python.exe transcribe.py "C:\path\to\audio.mp3"
```

- Default output: `outputs/transcripts/<audio_basename>.txt` (use `--out-dir` to change).
- First run will download the Whisper model (~150 MB); later runs use the cache.

### Example workflow

**From a video file (Linux):**

```bash
.venv/bin/python extract_audio.py "/home/you/Videos/meeting.mkv"
.venv/bin/python transcribe.py "outputs/audio/meeting.mp3"
```

**From a video file (Windows):**

```powershell
.venv\Scripts\python.exe extract_audio.py "C:\Users\you\Videos\meeting.mp4"
.venv\Scripts\python.exe transcribe.py "C:\Users\you\Projects\audio_meeting_summary\meeting.mp3"
```

**From a live recording:**

```bash
.venv/bin/python record_audio.py "meeting.wav"
# ... speak, then press Ctrl+C ...
.venv/bin/python transcribe.py "meeting.wav"
```

## Notes

- **Transcription device:** The script uses `device="cpu"` by default. If you have an NVIDIA GPU, install the [CUDA Toolkit 12](https://developer.nvidia.com/cuda-downloads) (so CUDA libraries such as `cublas64_12.dll` on Windows or `libcublas.so` on Linux are available), then change to `device="cuda"` in `transcribe.py` for faster runs.
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
