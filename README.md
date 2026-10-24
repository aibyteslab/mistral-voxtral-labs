# Mistral Voxtral labs

Hands-on labs for **Voxtral**, Mistral AI's speech-to-text models.
Each lab goes with an AI Bytes Lab video and contains the code shown on screen,
so you can rerun every step from the video on your own audio.

## Labs

| Folder | Video | What you build | Tested with |
|---|---|---|---|
| [`voxtral3-transcribe/`](voxtral3-transcribe/) | [Transcribe Audio with Mistral Voxtral 3 in 5 Minutes (Python)](https://youtu.be/OgvltgAR66s) | Batch transcription with segment timestamps and speaker labels, then realtime streaming over a WebSocket | mistralai 3.4.0, Python 3.14, 2026-10-24 |

Each new video adds a folder here and a row to this table.

## Quick start

Requirements: Python 3.10 or newer and a Mistral API key from AI Studio.

```bash
git clone https://github.com/aibyteslab/mistral-voxtral-labs.git
cd mistral-voxtral-labs/voxtral3-transcribe
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export MISTRAL_API_KEY="YOUR_API_KEY"   # better: load it from your keychain or secret manager
python transcribe.py your-audio.mp3
```

The [lab README](voxtral3-transcribe/README.md) covers the realtime script,
the audio format it expects, and the caveats.

## Before you build on it

- Voxtral 3 was released on 2026-10-20 and is in **public preview**. Model
  names and prices may change. Check Mistral's docs before you rely on them.
- Accuracy and latency figures in the video are Mistral's own, not ours.
  Test on your own audio.
- Never commit your API key. `.gitignore` already excludes `.env` files.

Not affiliated with or sponsored by Mistral AI. Mistral and Voxtral are
trademarks of Mistral AI.

Powered by AI Bytes Lab™ · [aibyteslab.com](https://aibyteslab.com)
