# Review: check, look, fix

## 1. The gate
```bash
python3 -I scripts/build.py && npx hyperframes check
```
Zero errors, zero warnings. Common ones and the real fix:

| Finding | Usually means | Fix |
| --- | --- | --- |
| `font_family_without_font_face` | a family is named without an `@font-face` | use only the kit's `Display`/`Mono` (with files) or Inter / JetBrains Mono |
| `text_box_overflow` / `container_overflow` on a masked line | the line is parked outside its mask | `opacity:0` while outside, plus `data-layout-allow-overflow` on that line |
| `container_overflow` on a character | they enter from off-frame | `data-layout-allow-overflow` on the wrapper |
| `text_occluded` | text under a card or panel | move it, raise it, or mark deliberate layering |
| overlap of two cards | real collision, or a deliberate deck | move one, or `data-layout-allow-overlap` on the deck |
| line-unread / too short | text isn't on screen long enough | hold it longer or say less |

## 2. Look at frames
```bash
npx hyperframes snapshot --at 0,2.5,6.5,12.5,18.6,22.5 --no-end -o shots
```
Open `shots/contact-sheet.jpg`. Check every scene's start (+0.3 s), middle, and the frame just
before its cut. `--review` captures that set automatically; `--zoom "#selector"` crops a detail.

Look for:
- the first frame (it's the thumbnail): never empty
- entrances peeking in at an edge before their cue
- text on text, text over a busy crowd without a card behind it
- a finger or cursor missing its button; a tag pointing at the wrong person
- feet or heads cut by the frame by accident
- two things competing; the eye should know where to go in under half a second
- small text: nothing under 28 px at 1080p
- untrue numbers, invented features, unlabelled demo data

## 3. Render and watch
```bash
npx hyperframes render -o renders/draft.mp4 --quality draft
```
Watch it start to finish at full speed. Note every moment you lose interest: those shots get cut
shorter, not decorated more.

## 4. REVIEW.md
- Creative calls: which storyline, why; what wasn't built.
- Measured vs looked at: check result, frames looked at, loudness numbers; sound measured or heard.
- The weakest shot and what you'd do with more time.
- Warnings kept on purpose, and why.
