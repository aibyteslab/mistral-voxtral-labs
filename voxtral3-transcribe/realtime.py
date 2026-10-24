import asyncio
import os
import sys
import wave

from mistralai.client import Mistral
from mistralai.client.models import (
    AudioFormat,
    RealtimeTranscriptionError,
    TranscriptionStreamDone,
    TranscriptionStreamTextDelta,
)


async def live(path):
    # play a WAV file in 100 ms chunks, at real-time speed, like a microphone
    with wave.open(path, "rb") as wav:
        while chunk := wav.readframes(wav.getframerate() // 10):
            yield chunk
            await asyncio.sleep(0.1)


async def main():
    client = Mistral(api_key=os.environ["MISTRAL_API_KEY"])
    with wave.open(sys.argv[1], "rb") as wav:
        rate = wav.getframerate()
    async for event in client.audio.realtime.transcribe_stream(
        audio_stream=live(sys.argv[1]),
        model="voxtral-mini-transcribe-realtime-3",
        audio_format=AudioFormat(encoding="pcm_s16le", sample_rate=rate),
    ):
        if isinstance(event, TranscriptionStreamTextDelta):
            print(event.text, end="", flush=True)
        elif isinstance(event, TranscriptionStreamDone):
            print("\n--- done")
        elif isinstance(event, RealtimeTranscriptionError):
            print("\nerror:", event.error.message)


asyncio.run(main())
