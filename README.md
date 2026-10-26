# storyframes

A Claude Code skill for making **character-driven motion explainer videos** for your product, the
kind of film made for [meetadev](https://www.meetadev.xyz): flat illustrated people, a crowd that
fills a hall, your app's own screens rebuilt big, kinetic type, and a synthesised music bed, all
rendered to MP4 with [HyperFrames](https://hyperframes.heygen.com).

![The example film that ships with the kit](docs/example.gif)

*The 24-second example film in `skills/storyframes/kit/build.py`, untouched. Replace the brief at the top and
the scenes, and it becomes your film.*

## What you get

- **A method.** Story first: one person, one want, one payoff. Then a written spec, a 120 bpm
  timing grid, a build, checks, a look at real frames, and a render. Claude follows it step by step.
- **A character rig** (`rig.py`). Rigged SVG people with walk, wave, blink, faces, a phone and a
  name badge. It also draws seeded crowds of about 600 people that you can dim, highlight and tag.
- **A film generator** (`build.py`). Python writes every scene's HTML and GSAP timeline, so the
  film is deterministic and you change one file to change it.
- **Music with no licence questions** (`make_music.py`). A bright 120 bpm bed synthesised with numpy.
  Drums drop in at your reveal and build into your payoff.
- **Sound placement** (`sfx.py`). Each effect's loudest moment lands exactly on its picture.
- **References** for story structure, a spec template, motion timings, sound and review.

## Install

In Claude Code:

```
/plugin marketplace add hazardsecurity/storyframes
/plugin install storyframes@storyframes
```

Or copy the skill folder yourself:

```bash
git clone https://github.com/hazardsecurity/storyframes
cp -r storyframes/skills/storyframes ~/.claude/skills/
```

**You'll also need:**
- Node 22+ (for `npx hyperframes`)
- Python 3, with `numpy` for the music
- `ffmpeg`

The official HyperFrames agent skills are recommended alongside it. Install them with `npx hyperframes skills update`.

## Use

Ask Claude for a film, for example:

> Make a 30 second explainer video for my app, a budgeting tool for students. Use characters like the meetadev video.

Claude writes three storylines and recommends one. Then it writes a `SPEC.md`, builds the film
from the kit, checks it, shows you frames and renders an MP4.

To try the example by hand:

```bash
npx --yes hyperframes@latest init my-film --example blank --non-interactive
cd my-film && mkdir -p scripts assets/audio assets/sfx assets/fonts
cp ~/.claude/skills/storyframes/kit/*.py scripts/
python3 -I scripts/make_music.py assets/audio/music.wav 24 8 14 20
python3 -I scripts/build.py
npx hyperframes check
npx hyperframes render -o renders/example.mp4
```

Add sound effects named `whoosh.mp3`, `pop.mp3`, `click.mp3`, `sparkle.mp3` and `impact.mp3` to
`assets/sfx/` (from a library you're licensed to use), rebuild, and they're placed automatically.

## Layout

```
.claude-plugin/          plugin + marketplace manifests
skills/storyframes/
  SKILL.md               the method Claude follows
  references/            story, spec template, rig API, motion, sound, review
  kit/                   rig.py, build.py (example film), sfx.py, make_music.py
docs/                    the preview above and a frame sheet
```

## Licence

MIT, by [Hazardsecurity](https://hazardsecurity.xyz). The film you make is yours.
HyperFrames, GSAP and any fonts or sound effects you use have their own licences.
