import math
import random
import struct
import wave
from pathlib import Path

# Generate an original cyberpunk-style background soundtrack.
SAMPLE_RATE = 22050
DURATION = 16
OUTPUT = Path(__file__).parent / "cyberpunk_theme.wav"

random.seed(7)


def synthesize():
    total_samples = SAMPLE_RATE * DURATION
    audio = []

    # Low ambient notes and a repeating electronic arpeggio.
    bass_notes = [55.0, 65.41, 73.42, 82.41]
    lead_notes = [220.0, 261.63, 329.63, 392.0, 329.63, 293.66, 261.63, 220.0]

    for i in range(total_samples):
        t = i / SAMPLE_RATE
        beat = int(t * 2) % len(lead_notes)
        bass = bass_notes[int(t / 4) % len(bass_notes)]
        lead = lead_notes[beat]

        # Soft low-frequency ambience.
        low = (
            math.sin(2 * math.pi * bass * t) * 0.24
            + math.sin(2 * math.pi * bass * 0.5 * t) * 0.10
        )

        # Short, pulsing synth notes.
        pulse = (t * 2) % 1
        envelope = max(0.0, 1.0 - pulse) ** 2
        synth = math.sin(2 * math.pi * lead * t) * envelope * 0.16

        # Subtle high-frequency futuristic texture.
        texture = math.sin(2 * math.pi * 880 * t) * 0.018

        # Gentle fade at the beginning and end.
        fade_in = min(1.0, t / 1.5)
        fade_out = min(1.0, (DURATION - t) / 1.5)
        fade = max(0.0, min(fade_in, fade_out))

        sample = (low + synth + texture) * fade
        sample = max(-1.0, min(1.0, sample))
        audio.append(struct.pack("<h", int(sample * 32767)))

    return b"".join(audio)


def main():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)

    with wave.open(str(OUTPUT), "wb") as music:
        music.setnchannels(1)
        music.setsampwidth(2)
        music.setframerate(SAMPLE_RATE)
        music.writeframes(synthesize())

    print(f"Cyberpunk soundtrack created: {OUTPUT}")


if __name__ == "__main__":
    main()
