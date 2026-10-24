import os
import sys

from mistralai.client import Mistral

client = Mistral(api_key=os.environ["MISTRAL_API_KEY"])
path = sys.argv[1]

with open(path, "rb") as audio:
    result = client.audio.transcriptions.complete(
        model="voxtral-mini-transcribe-3",
        file={"file_name": os.path.basename(path), "content": audio},
        timestamp_granularities=["segment"],
        diarize=True,
    )

for seg in result.segments:
    print(f"[{seg.start:6.1f}s] {seg.speaker_id}: {seg.text.strip()}")

seconds = result.usage.prompt_audio_seconds
print(f"\n{seconds:.0f} s of audio, about ${seconds / 60 * 0.0035:.4f}")
