"""storyframes sound placement: put each effect so its loudest moment lands on the picture.

A whoosh or pop file rarely peaks at 0 s. If you start it on the frame where the card lands,
the hit arrives late and the film feels sluggish. measure() finds each file's peak time and
length once (with ffmpeg) and caches them; cue_tags() starts every effect so its peak lands
one frame after its picture time, which is how hits feel "on" the cut.
"""
import json
import os
import struct
import subprocess

SR = 22050


def _decode(path):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "1", "-ar", str(SR), "-f", "s16le", "-"],
                         check=True, capture_output=True).stdout
    return struct.unpack(f"<{len(raw) // 2}h", raw)


def measure(sfx_dir):
    """{name: {"peak": seconds, "len": seconds}} for every .mp3/.wav in sfx_dir, cached in peaks.json."""
    cache_path = os.path.join(sfx_dir, "peaks.json")
    cache = json.load(open(cache_path)) if os.path.exists(cache_path) else {}
    changed = False
    for f in sorted(os.listdir(sfx_dir)):
        name, ext = os.path.splitext(f)
        if ext not in (".mp3", ".wav") or name in cache:
            continue
        samples = _decode(os.path.join(sfx_dir, f))
        if not samples:
            continue
        peak_i = max(range(len(samples)), key=lambda i: abs(samples[i]))
        cache[name] = {"peak": round(peak_i / SR, 3), "len": round(len(samples) / SR, 2), "file": f}
        changed = True
    if changed:
        json.dump(cache, open(cache_path, "w"), indent=1)
    return cache


def cue_tags(cues, sfx_dir, film_len, fps=30, first_track=21, lanes=4):
    """cues: [(picture_time, name, volume), ...]. Returns <audio> tags for index.html.
    Cues whose file is missing are skipped (and listed), so a film still builds before its sounds exist."""
    if not os.path.isdir(sfx_dir):
        return [], sorted({c[1] for c in cues})
    info = measure(sfx_dir)
    tags, used, missing = [], {}, set()
    for i, (t, name, vol) in enumerate(cues):
        if name not in info:
            missing.add(name)
            continue
        m = info[name]
        start = round(max(0.0, t - m["peak"] + 1 / fps), 3)
        dur = round(min(m["len"], film_len - start), 2)
        if dur <= 0:
            continue
        used[name] = used.get(name, 0) + 1
        tags.append(f'      <audio id="sfx-{name}-{used[name]}" src="assets/sfx/{m["file"]}" data-start="{start}" data-duration="{dur}" '
                    f'data-track-index="{first_track + i % lanes}" data-volume="{vol}"></audio>')
    return tags, sorted(missing)
