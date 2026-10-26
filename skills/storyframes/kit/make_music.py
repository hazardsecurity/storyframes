# storyframes music bed: a bright 120 bpm loop synthesised from scratch (no samples, no licence questions).
# C major I-vi-IV-V, one chord a bar (a bar is 2 s, so scenes cut on even seconds).
# A soft pad and plucks under the hook, hats from 4 s, drums and bass drop in at DRUMS,
# a snare roll that speeds up into HIT (your payoff moment), and a held final hit at END (the end card).
# Run: python3 -I make_music.py assets/audio/music.wav DUR DRUMS HIT END   (seconds, ideally even numbers)
# Needs numpy.
import sys
import wave

import numpy as np

SR = 44100
BPM = 120
BEAT = 60 / BPM
OUT, DUR, DRUMS, HIT, END = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5])
N = int(SR * DUR)
rng = np.random.default_rng(7)

left = np.zeros(N)
right = np.zeros(N)


def note_hz(midi):
    return 440.0 * 2 ** ((midi - 69) / 12)


def add(sig, start, pan=0.0, gain=1.0):
    i = int(start * SR)
    if i >= N:
        return
    sig = sig[: N - i] * gain
    left[i : i + len(sig)] += sig * (1 - max(pan, 0))
    right[i : i + len(sig)] += sig * (1 + min(pan, 0))


def env(n, a, d, s, r, sustain_len):
    a, d, r = int(a * SR), int(d * SR), int(r * SR)
    sl = max(int(sustain_len * SR) - a - d, 0)
    e = np.concatenate([
        np.linspace(0, 1, max(a, 1)),
        np.linspace(1, s, max(d, 1)),
        np.full(sl, s),
        np.linspace(s, 0, max(r, 1)),
    ])
    return e[:n] if len(e) >= n else np.pad(e, (0, n - len(e)))


def pluck(midi, length=0.4):
    n = int(SR * (length + 0.3))
    t = np.arange(n) / SR
    f = note_hz(midi)
    tone = 0.6 * np.sin(2 * np.pi * f * t) + 0.25 * np.sin(2 * np.pi * 2 * f * t) + 0.1 * np.sin(2 * np.pi * 3 * f * t)
    return tone * np.exp(-t * 7.5)


def pad(midis, length):
    n = int(SR * (length + 0.6))
    t = np.arange(n) / SR
    s = np.zeros(n)
    for m in midis:
        f = note_hz(m)
        for det in (-0.12, 0.0, 0.12):
            s += np.sin(2 * np.pi * f * (1 + det / 100) * t + rng.uniform(0, 6))
    s /= len(midis) * 3
    return s * env(n, 0.35, 0.3, 0.8, 0.6, length)


def bass(midi, length):
    n = int(SR * (length + 0.05))
    t = np.arange(n) / SR
    f = note_hz(midi)
    s = np.sin(2 * np.pi * f * t) + 0.3 * np.sin(2 * np.pi * 2 * f * t)
    return np.tanh(1.6 * s) * env(n, 0.005, 0.08, 0.7, 0.05, length)


def kick():
    n = int(SR * 0.35)
    t = np.arange(n) / SR
    f = 50 + 110 * np.exp(-t * 30)
    ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(ph) * np.exp(-t * 9)


def clap():
    n = int(SR * 0.25)
    t = np.arange(n) / SR
    noise = rng.uniform(-1, 1, n)
    # band-limit roughly with a difference filter
    noise = np.diff(np.concatenate([[0], noise]))
    return noise * np.exp(-t * 18) * 0.6


def hat(open_=False):
    n = int(SR * (0.18 if open_ else 0.05))
    t = np.arange(n) / SR
    noise = rng.uniform(-1, 1, n)
    noise = np.diff(np.concatenate([[0], noise]))
    noise = np.diff(np.concatenate([[0], noise]))
    return noise * np.exp(-t * (14 if open_ else 70)) * 0.25


# I - vi - IV - V in C, one chord a bar (2 s)
CHORDS = [
    (48, [60, 64, 67, 72]),  # C
    (45, [57, 60, 64, 69]),  # Am
    (41, [53, 57, 60, 65]),  # F
    (43, [55, 59, 62, 67]),  # G
]
BAR = 4 * BEAT
bars = int(DUR / BAR)

for b in range(bars):
    t0 = b * BAR
    root, chord = CHORDS[b % 4]
    last = t0 >= END - 2
    # pad everywhere, longer under the end card
    add(pad(chord, BAR if not last else DUR - t0), t0, gain=0.16 if t0 < DRUMS else 0.11)
    if last and t0 > END - 2:
        continue
    # plucked arpeggio: 8ths, from the top of the film
    pattern = [0, 2, 1, 3, 2, 1, 3, 2]
    for k, idx in enumerate(pattern):
        tt = t0 + k * BEAT / 2
        if tt >= END:
            break
        pan = -0.35 if k % 2 == 0 else 0.35
        add(pluck(chord[idx] + 12), tt, pan=pan, gain=0.10 if t0 < DRUMS else 0.13)
    if t0 >= 4 and t0 < END:
        # quiet hats from the tension onwards
        for k in range(8):
            add(hat(open_=(k % 4 == 3)), t0 + k * BEAT / 2, pan=0.25, gain=0.45 if t0 < DRUMS else 0.6)
    if DRUMS <= t0 < END:
        # groove: kick on 1, the "and" of 2, and 3; clap on 2 and 4; bass on the kicks
        for beat_pos in (0, 1.5, 2):
            add(kick(), t0 + beat_pos * BEAT, gain=0.9)
            add(bass(root - 12 + (7 if beat_pos == 1.5 else 0), BEAT * 0.9), t0 + beat_pos * BEAT, gain=0.32)
        add(bass(root - 12, BEAT * 0.4), t0 + 3.5 * BEAT, gain=0.25)
        for beat_pos in (1, 3):
            add(clap(), t0 + beat_pos * BEAT, gain=0.55)
        # shaker 16ths
        for k in range(16):
            add(hat() * 0.5, t0 + k * BEAT / 4, pan=-0.3, gain=0.35)

# build into the payoff: a snare roll over the 4 s before HIT that speeds up, then a big kick on HIT
t = HIT - 4
step = BEAT / 2
while t < HIT:
    add(clap() * (0.3 + 0.5 * (t - (HIT - 4)) / 4), t, gain=0.6)
    t += step
    if t > HIT - 2:
        step = BEAT / 4
add(kick() * 1.4, HIT, gain=1.0)

# final chord hit under the end card
add(kick() * 1.2, END, gain=1.0)
add(bass(36, 3.0), END, gain=0.35)

mix = np.stack([left, right], axis=1)
# fade in 0.3 s, fade out over the last 1.5 s
fade_in = np.linspace(0, 1, int(0.3 * SR))
mix[: len(fade_in)] *= fade_in[:, None]
fade_out = np.linspace(1, 0, int(1.5 * SR))
mix[-len(fade_out) :] *= fade_out[:, None]
# soft clip and normalise to about -1 dBFS peak
mix = np.tanh(mix * 1.1)
mix /= np.max(np.abs(mix)) / 0.89

out = OUT
with wave.open(out, "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes((mix * 32767).astype("<i2").tobytes())
print("wrote", out)
