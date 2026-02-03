"""
Record audio from the default microphone. Cross-platform (Windows, Linux, macOS).
Uses sounddevice (PortAudio); same script works everywhere.
Usage: python record_audio.py <output.wav> [duration_seconds]
  If duration is omitted, records until you press Ctrl+C.
"""
import sys
import signal
import numpy as np
import sounddevice as sd
import soundfile as sf

SAMPLE_RATE = 44100
CHANNELS = 2

def main():
    if len(sys.argv) < 2:
        print("Usage: python record_audio.py <output.wav> [duration_seconds]")
        sys.exit(1)

    output_path = sys.argv[1]
    duration = None
    if len(sys.argv) >= 3:
        try:
            duration = float(sys.argv[2])
            if duration <= 0:
                raise ValueError("Duration must be positive")
        except ValueError as e:
            print(f"Invalid duration: {e}")
            sys.exit(1)

    if duration is not None:
        # Fixed-length recording
        print(f"Recording for {duration} seconds... Save to: {output_path}")
        frames = int(duration * SAMPLE_RATE)
        recording = sd.rec(frames, samplerate=SAMPLE_RATE, channels=CHANNELS, dtype="float32")
        sd.wait()
        sf.write(output_path, recording, SAMPLE_RATE)
        print(f"Done. Saved to: {output_path}")
    else:
        # Record until Ctrl+C
        recorded = []
        stream = None

        def stop(sig=None, frame=None):
            if stream is not None and stream.active:
                stream.stop()

        signal.signal(signal.SIGINT, stop)
        if hasattr(signal, "SIGBREAK"):
            signal.signal(signal.SIGBREAK, stop)

        def callback(indata, frames, time_info, status):
            if status:
                print(status, file=sys.stderr)
            recorded.append(indata.copy())

        print(f"Recording... Press Ctrl+C to stop. Save to: {output_path}")
        stream = sd.InputStream(samplerate=SAMPLE_RATE, channels=CHANNELS, callback=callback, dtype="float32")
        stream.start()
        try:
            while stream.active:
                sd.sleep(100)
        except KeyboardInterrupt:
            stop()
        stream.stop()
        stream.close()

        if not recorded:
            print("No audio recorded.")
            sys.exit(1)
        data = np.concatenate(recorded, axis=0)
        sf.write(output_path, data, SAMPLE_RATE)
        print(f"Done. Saved to: {output_path}")


if __name__ == "__main__":
    main()
