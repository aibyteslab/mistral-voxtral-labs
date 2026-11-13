"""Voice assistant: speak -> Voxtral transcribes -> Mistral Small answers -> Voxtral speaks the answer.

  python assistant.py                 # talk into the microphone (needs: pip install sounddevice)
  python assistant.py q1.wav q2.wav   # or feed recorded questions, one per turn
"""
import base64, os, shutil, subprocess, sys, tempfile, time, wave

from mistralai.client import Mistral

STT, LLM, TTS, VOICE = "voxtral-mini-transcribe-3", "mistral-small-2603", "voxtral-mini-tts-3", "voice_485"
PRICE_MIN, PRICE_IN, PRICE_OUT, PRICE_CHAR = 0.0035, 0.15e-6, 0.60e-6, 13e-6   # USD, from docs.mistral.ai

client = Mistral(api_key=os.environ["MISTRAL_API_KEY"])
chat = [{"role": "system", "content": "You are a voice assistant. Answer in one or two short spoken "
         "sentences. Plain words only: no lists, no markdown, no emoji."}]


def record(seconds=6, rate=16000):
    import sounddevice as sd                      # only needed for the microphone
    input(f"Press Enter and speak ({seconds} s)...")
    pcm = sd.rec(int(seconds * rate), samplerate=rate, channels=1, dtype="int16"); sd.wait()
    path = tempfile.mktemp(suffix=".wav")
    with wave.open(path, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(rate); w.writeframes(pcm.tobytes())
    return path


def play(path):
    player = next(p for p in ("pw-play", "aplay", "afplay", "ffplay") if shutil.which(p))
    subprocess.run([player, path] + (["-nodisp", "-autoexit"] if player == "ffplay" else []),
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def turn(path):
    t0 = time.time()
    with open(path, "rb") as f:
        heard = client.audio.transcriptions.complete(model=STT, file={"file_name": "q.wav", "content": f})
    print(f"\nYou:       {heard.text.strip()}   [{time.time() - t0:.1f} s]")
    chat.append({"role": "user", "content": heard.text})
    t1 = time.time()
    reply = client.chat.complete(model=LLM, messages=chat, reasoning_effort="none")   # fast replies
    answer = reply.choices[0].message.content.strip()
    chat.append({"role": "assistant", "content": answer})
    print(f"Assistant: {answer}   [{time.time() - t1:.1f} s]")
    t2 = time.time()
    speech = client.audio.speech.complete(model=TTS, input=answer, voice_id=VOICE, response_format="wav")
    out = f"answer{len(chat) // 2}.wav"           # answer1.wav, answer2.wav, ...
    open(out, "wb").write(base64.b64decode(speech.audio_data))
    print(f"           (speaking...)   [{time.time() - t2:.1f} s]")
    play(out)
    secs, u = heard.usage.prompt_audio_seconds, reply.usage
    return (secs / 60 * PRICE_MIN + u.prompt_tokens * PRICE_IN + u.completion_tokens * PRICE_OUT
            + len(answer) * PRICE_CHAR)


total, files = 0.0, sys.argv[1:]
for path in files or iter(record, None):          # microphone mode runs until Ctrl+C
    total += turn(path)
    print(f"           running cost: ${total:.5f}")
