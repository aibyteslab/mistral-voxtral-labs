# Voxtral 3: transcribe audio in Python

Companion code for the video **Transcribe Audio with Mistral Voxtral 3 in 5
Minutes (Python)**. Two scripts, about 60 lines in total:

| File | What it does | Model |
|---|---|---|
| `transcribe.py` | Transcribes a recorded file and prints every segment with its start time and speaker label, plus the seconds of audio billed and an estimated cost | `voxtral-mini-transcribe-3` |
| `realtime.py` | Streams a WAV file in 100 ms chunks at real-time speed, like a microphone, and prints text as it arrives | `voxtral-mini-transcribe-realtime-3` |

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt        # mistralai with the realtime extra
export MISTRAL_API_KEY="YOUR_API_KEY"
```

The realtime client needs the `realtime` extra. A plain `pip install mistralai`
is not enough for `realtime.py`.

## Run

```bash
python transcribe.py speech.mp3
python realtime.py clip.wav
```

The video uses the two sample clips from Mistral's audio documentation
(docs.mistral.ai, Audio section): a 203 s single-speaker speech for
`transcribe.py`, and a 20 s WAV for `realtime.py`. They are not included here,
so download them from the docs or use your own audio.

`realtime.py` sends raw 16-bit signed little-endian PCM and reads the sample
rate from the WAV header. The input must be a **mono, 16-bit WAV**. To convert
any file:

```bash
ffmpeg -i input.mp3 -ac 1 -ar 16000 -sample_fmt s16 clip.wav
```

To use a live microphone instead, replace the `live()` generator with one that
yields 100 ms chunks from your audio input. Nothing else changes.

## Caveats (as of 2026-10-24)

- **Preview.** Voxtral 3 is in public preview since 2026-10-20; model names
  and prices may change.
- **Cost line.** `transcribe.py` estimates cost with Mistral's list price for
  Mini Transcribe 3 ($0.0035/min on 2026-10-24). It is an estimate, not your
  bill.
- **Timestamps** are per segment; word-level timestamps aren't available.
- **`diarize=True`** only works with segment timestamps turned on.
- **Realtime:** you can't use speaker labels and turn detection in the same
  session.
- Accuracy and latency numbers are Mistral's own. Test on your audio.

## License

MIT, see [`LICENSE`](../LICENSE).
