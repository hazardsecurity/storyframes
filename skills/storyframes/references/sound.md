# Sound

These films have no voiceover: picture, text, music and effects carry everything, so they work
muted on a feed and better with sound.

## Music bed (`kit/make_music.py`)
```bash
python3 -I scripts/make_music.py assets/audio/music.wav DUR DRUMS HIT END
# e.g. a 36 s film: reveal at 14, payoff at 22, end card at 32
python3 -I scripts/make_music.py assets/audio/music.wav 36 14 22 32
```
- 120 bpm, C major I–vi–IV–V, one chord per 2 s bar, synthesised with numpy: no samples, nothing to license.
- Plucks and a pad from 0 s, quiet hats from 4 s, **drums and bass enter at DRUMS** (use the turn,
  when the product appears), a **snare roll speeds up into HIT** (the payoff), a **final hit at END**
  (the end card), a 1.5 s fade out.
- Change `CHORDS`, `BPM` or the patterns in the file for a different mood; keep scenes on bar lines.
- Add it in `index.html` as `<audio id="music" ... data-track-index="20">` for the whole film.

## Effects (`kit/sfx.py`)
A small kit covers almost everything:

| Name | Use |
| --- | --- |
| `whoosh` / `whoosh-short` | scene exits, panels sliding in, line swaps |
| `pop` | chips, tags, toasts, stamps (several in a stagger: raise volume slightly each time) |
| `click` / `click-soft` | taps and button presses |
| `sparkle` | a reveal or highlight |
| `impact` | the payoff landing (with the music's HIT) |
| `typing`, `key-press`, `notification`, `riser` | chat, counters, messages, a build into a reveal |

Get them from a library you're allowed to use (the HyperFrames `media-use` skill, Pixabay's sound
effects, freesound.org with a CC0 filter) and save them as `assets/sfx/<name>.mp3`. Don't commit
effects you don't have the rights to redistribute.

Cue them in `build.py` as `(picture_time, name, volume)`. `cue_tags` measures each file's peak once
(cached in `assets/sfx/peaks.json`) and starts it `peak − 1 frame` early so the loudest moment lands
on the picture. Start at volumes 0.25–0.5; music should stay audible under effects.

Check where sounds actually land: `npx hyperframes audio` reports onsets and hits in film time.

## Final mix
Normalise after rendering:
```bash
ffmpeg -i renders/film.mp4 -c:v copy -af "loudnorm=I=-16:TP=-1.5:LRA=11,alimiter=limit=0.89" renders/film-final.mp4
```
Target about −16 LUFS integrated and below −1 dBTP true peak (good for social feeds and YouTube).
Measure: `ffmpeg -i renders/film-final.mp4 -af ebur128=peak=true -f null - 2>&1 | tail -12`.
If you can't listen, say the sound was measured, not heard.
