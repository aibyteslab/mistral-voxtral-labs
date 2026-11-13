# Voice assistant: Voxtral ears, Mistral Small brain, Voxtral voice

Companion code for the video
[**Build a Voice Assistant with Mistral Voxtral in Python**](https://youtu.be/t9ujkEutTOo). One script, about 50 lines:

| Step | What it does | Model |
|---|---|---|
| Ears | Transcribes your spoken question | `voxtral-mini-transcribe-3` |
| Brain | Answers in one or two short spoken sentences | `mistral-small-2603` (Mistral Small 4, `reasoning_effort="none"`) |
| Voice | Speaks the answer, saved as `answer1.wav`, `answer2.wav`, ... and played | `voxtral-mini-tts-3`, voice `voice_485` |

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
export MISTRAL_API_KEY="YOUR_API_KEY"   # better: load it from your keychain or secret manager
```

## Run

```bash
python assistant.py q1.wav q2.wav q3.wav   # recorded questions, one per turn
python assistant.py                        # microphone: pip install sounddevice first; Ctrl+C to stop
```

Each turn prints what it heard, the answer, how long each step took, and a
running cost estimate. Audio is played with the first player it finds:
`pw-play`, `aplay`, `afplay` or `ffplay`.

## How it works

- **Memory is just a list.** The chat API keeps no state between calls, so
  `chat` holds the whole conversation and is sent again with every question.
  That is why a follow-up like "and from the Moon?" works.
- **Audio comes back as text.** The speech endpoint returns the WAV as base64
  inside the JSON response; the script decodes it and writes the file.
- **Not streaming.** Each step waits for the full result before the next one
  starts.

## Caveats (as of 2026-11-13)

- **Preview.** Voxtral 3 is in public preview; model names and prices may
  change. Check Mistral's docs before you rely on them.
- **Cost line** is an estimate from list prices: $0.0035 per minute of audio
  (transcription), $0.15 / $0.60 per million input / output tokens (Mistral
  Small 4), $13 per million characters (Voxtral TTS, per its model card). It is
  not your bill.
- Step times in the video come from one run on our machine, not a benchmark.
- Tested with mistralai 3.7.0 and Python 3.14 on 2026-11-13.

## License

MIT, see [`LICENSE`](../LICENSE).
