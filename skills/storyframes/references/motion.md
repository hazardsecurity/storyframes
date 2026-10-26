# Motion vocabulary

## Durations and eases
| Move | Duration | Ease |
| --- | --- | --- |
| Enter (cards, panels, characters) | 0.45–0.6 s | `expo.out` |
| Move across the frame | 0.4–0.5 s | `power3.inOut` |
| Exit | 0.3–0.45 s | `power2.in` / `power3.in` |
| Camera drift (whole scene) | the scene length | `sine.inOut`, 60–100 px total |
| Chips, tags, buttons, stamps | 0.35–0.45 s | `back.out(1.6–2.2)`, scale and position only |
| Text reveal in a mask | 0.45–0.55 s | `expo.out` on `yPercent` from 110–230 |
| Staggers | 0.12–0.2 s between items | — |
| Button press | 0.08 s down, yoyo | drop `y` by the bottom-edge size, shrink the shadow |

Enter fast, settle slow; leave faster than you arrived.

## Patterns that carry these films
- **Masked line swap.** A card with `overflow:hidden`; the old line exits up (`yPercent:-170`), the
  new one enters from below. Hide each line with `opacity:0` while it's outside the mask.
- **Counter.** `countUp` with `power2.out` over 1.5–2 s; tabular numbers; a suffix ("+") only at the end.
- **Selection in a crowd.** Dim → highlight many → narrow to a few → tags pop with a stagger → a
  lock or tick icon on one tag as its state changes.
- **Swipe card.** Finger (a translucent circle) travels to the card, drags; a MEET/PASS stamp
  appears at 25% of the drag; the card flies off with ±20° rotation; the next card springs up.
- **Toast/notification.** Slides up 30 px with `back.out(1.6)`, holds long enough to read, fades.
- **Phone push-in.** Scene opens with the phone at scale 1.7 and settles to 1: we've "zoomed into" it
  from the previous scene's exit.
- **Hand-offs between scenes.** Exit by pushing into the thing the next scene is about: the
  character's face, their phone, a name tag in the crowd. The next scene opens slightly over-scaled
  (1.15 → 1) so the cut feels continuous.
- **Blur-in titles.** `opacity 0, filter: blur(8px)` → clear in 0.2 s for a line that appears over a
  busy background.
- **Logo build.** Strokes draw (`strokeDashoffset`), dots drop in with `back.out`, the mark slides
  aside and the wordmark wipes out from behind it.

## Rules
- Nothing moves while it's being read. Move, settle, then hold.
- One signature moment per scene; secondary elements enter calmly or are already there.
- Don't enter three things identically at once: stagger them and vary the direction or size.
- Motion should *mean* something: a card flying left is "pass", right is "meet"; a tick turning green
  is "they agreed". If a move has no meaning, cut it.
- Keep important text at least 60 px from frame edges and out of the bottom 10% if the film will be
  posted with platform captions.
