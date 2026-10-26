---
name: storyframes
description: Make character-driven motion explainer videos for a product (flat illustrated people, crowds, the product's own UI rebuilt big, kinetic type, a synthesised music bed and placed sound effects), rendered to MP4 with HyperFrames. Use when someone asks for an animated product video, launch film, explainer, promo, "a video like the meetadev one", a story with characters using an app, or a crowd or event scene, and whenever they want to plan, build, review or render such a film.
---

# storyframes

The method behind the meetadev films: a short story about one person with a problem, told with
flat SVG characters and the product's own screens, cut to a 120 bpm music bed. Everything is
HTML + GSAP that HyperFrames renders frame by frame, so every frame is a pure function of time.

**The pipeline:** brief → storylines → SPEC → `build.py` generates the HTML → check → look at frames →
fix → render → finish the sound.

You write Python that *generates* the compositions. You never hand-edit the generated HTML.
Generating gives you seeded, repeatable crowds, stable ids on every body part, and one place to
change timing. Hand-edits also break when HyperFrames Studio adds `data-hf-id` attributes.

## 0. Setup (once per machine, then once per film)

Needs Node 22+, Python 3 with `numpy` (only for music), and `ffmpeg`.

```bash
npx --yes hyperframes@latest init my-film --example blank --non-interactive
cd my-film
mkdir -p scripts assets/audio assets/sfx assets/fonts
cp <this skill>/kit/*.py scripts/          # rig.py, sfx.py, make_music.py, build.py (the example)
python3 -I scripts/make_music.py assets/audio/music.wav 24 8 14 20
python3 -I scripts/build.py
npx hyperframes check
```

Pin the HyperFrames version in `package.json` once a film works. If the official HyperFrames
agent skills are not installed, run `npx hyperframes skills update` and use them alongside this
one. They own the render contract (`window.__timelines`, `data-*` attributes) and the CLI.

The example `build.py` is a complete 24 s film ("500 people, one room") that passes `check`.
Start every new film by copying it and replacing the scenes. Don't start from a blank page.

## 1. Story first (no code yet)

Read `references/story.md`. Then:

1. **Write the one thing** the viewer must leave with, in one sentence ("at a big event, meetadev
   tells you who to meet").
2. **Build a spine around one person.** Give them a name and a want (Tolu, Android dev, wants a mentor).
   Follow them from the problem to the payoff. Viewers care about a person, not a feature list.
3. **Write three storylines (A, B, C)** with different devices, and recommend one. Examples:
   a moment everyone knows, a number that lands, before and after.
4. **Write `SPEC.md`** from `references/spec-template.md`. It needs goal, output, timing grid,
   look, objects, motion, shot list with times, banned list and QA times. The shot list is the contract;
   build to it.

Ask the user only what changes the film: the product's real claims and numbers, the audience,
and the length. Never invent features, numbers or testimonials. If a number is demo data,
label it on screen ("ILLUSTRATIVE DATA").

## 2. The timing grid

- 30 fps, 120 bpm: a beat is 0.5 s and a bar is 2 s.
- **Scenes start on bar lines** (even seconds).
- Hits land on beats, and moves start about 0.1 s before the beat they land on.
- Typical sizes: a 24–36 s film has 4–5 scenes, and a 60 s film has 8–10.
- Give the end card at least 4 s and hold the URL for at least 2.5 s.
- Every line of text stays still long enough to read: about 0.25 s per word, plus 0.5 s.

## 3. Build with the kit

Read `references/rig.md` for the character and crowd API, and `references/motion.md` for the motion
vocabulary. The shape of `build.py`:

- **`scene(id, css, html, js, bg)`** returns one `<template>` sub-composition with its own paused
  timeline, registered as `window.__timelines[id]`. One scene equals one file in `compositions/`.
- **`person("tolu1", **TOLU)`** returns a rigged character. Ids must be unique per scene, so use
  `tolu1`, `tolu2` and so on for the same person in different scenes.
- **`crowd("hc", seed=11)`** returns a room of about 600 people plus their positions. Reuse the same
  seed in every scene so it's the same room. `highlight_layer` redraws chosen people on top,
  and `head_of` pins a name tag to someone.
- **`RIG_JS`** goes into every scene. It provides `face`, `blink`, `walk`, `wave`, `holdPhone`, `nod`,
  `lookAround`, `pop` and `countUp`. All of them take `(tl, id, time)` and add tweens at absolute times.
- **The product's UI is rebuilt in HTML** at about 1.8× real size: cards, buttons, chips, a phone.
  Use its real labels and colours. Never use a screenshot under a title.
- **`index.html`** hosts the scenes on track 1, music on track 20, and effects on tracks 21–24.

**Hard rules (the render breaks or lies otherwise):**
- No `Math.random()`, `Date.now()`, or timers at runtime. Randomness happens in Python with a seed.
- Every change is a tween or `tl.set` on the scene timeline. Counters update text in `onUpdate`.
- Name every font family with an `@font-face`. Without local font files the kit uses Inter and
  JetBrains Mono, which the renderer supplies itself.
- Text that slides out of a mask is set to `opacity: 0` whenever it is outside it.
- Deliberate overflow, overlap or occlusion is marked with `data-layout-allow-overflow`,
  `data-layout-allow-overlap` or `data-layout-allow-occlusion`. Mark decorative layers like
  crowds with `data-layout-ignore`. Mark nothing else; a warning you silence is a bug you keep.

## 4. Sound

Read `references/sound.md`.

- **Music.** `make_music.py OUT DUR DRUMS HIT END` synthesises a bed with no samples and no licence
  questions. Drums enter at the reveal, a snare roll builds into the payoff, and a final hit lands under the end card.
- **Effects.** Use whooshes, pops, clicks, a sparkle and an impact. Get them from a library you're
  licensed to use, for example the HyperFrames media skill or Pixabay. `sfx.cue_tags` measures each file's peak
  and starts it so the peak lands one frame after its picture time.
- **Final mix.** Aim for about −16 LUFS integrated and a −1 dBTP peak (see `references/sound.md`).

## 5. Check, look, fix

Read `references/review.md`.

1. **`npx hyperframes check`** must pass with zero errors and warnings. Read each warning's fix. Most are real.
2. **`npx hyperframes snapshot --at <QA times> --no-end -o shots`**, then open `shots/contact-sheet.jpg`.
   Look at every scene's start, middle, and the frame before it cuts.
3. **Look for these problems:**
   - entrances that peek in at the edges
   - text over text
   - a finger missing its button
   - a character's feet cut off by accident
   - two things competing for the eye
   - a number that isn't true
4. **Fix the problem in `build.py`, rebuild, and check again.** Repeat until every frame is one you'd post.

## 6. Render and finish

```bash
npx hyperframes render -o renders/film.mp4                # add --quality delivery for the final
ffmpeg -i renders/film.mp4 -c:v copy -af "loudnorm=I=-16:TP=-1.5:LRA=11,alimiter=limit=0.89" renders/film-final.mp4
ffmpeg -ss 21 -i renders/film-final.mp4 -frames:v 1 renders/poster.jpg
```

Write a short `REVIEW.md` covering:
- which storyline you built and why
- what you measured and what you only looked at
- the weakest shot, and what you'd do with more time
- any warnings you kept on purpose

Then tell the user the same, plainly.

## Taste (what made the meetadev films work)

- **One person, one want, one payoff.** The product shows up as the turn in their story, not as a tour.
- **The product's own surfaces, chunky and big.** White cards, 2–3 px borders, a thicker bottom edge,
  and buttons that press down. Use the brand's colours as flat fields, never gradients.
- **Every scene exits into the next through an object.** Push into the character, zoom into the phone,
  dive into a name tag. Avoid fade-to-white between unrelated shots.
- **One signature moment per scene.** Everything else stays calm.
- **Banned:**
  - a dark void with glowing particles
  - purple-blue gradients and glass cards
  - three cards entering at once (stagger them and make them differ)
  - text moving while it's read
  - a logo docked in a corner
  - stock "tech" clichés

See `references/motion.md` for durations and eases, and `references/story.md` for story devices.
