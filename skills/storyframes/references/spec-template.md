# SPEC template

Copy into the film folder as `SPEC.md` and fill every line before writing `build.py`.
This is the one the meetadev launch film was built from, abridged, as an example of the detail level.

```
# SPEC — <product>, storyline <A> "<name>"

GOAL:    <who> ends the film knowing <the one thing>, and wants to <action, usually open the URL>.
OUTPUT:  HyperFrames, 1920 x 1080, 30 fps   (1080 x 1920 for vertical; then everything moves to a column)
TIME:    <N> s x 30 = <frames>; 120 bpm, 15 frames a beat, 60 frames a bar; scenes start on bar lines.

LOOK:    ground #ffffff and wash #f8f9fa; ink #202124, muted #5f6368, line #dadce0.
         Brand colours as flat fields and fills only: <list with hex>. Soft tints: <list>.
         Accent per shot: one colour field, one highlighted word.
         Display: <font> 700, 84–148 px, tracking -0.035em. UI at 1.8x product size (body >= 30 px).
         Meta labels: <mono font> 600 uppercase +0.08em, >= 28 px.
         Medium: the product's own surfaces: white cards, 3 px border, 7–9 px bottom edge, radius 26–34 px;
         buttons with a darker bottom edge that press down.
OBJECTS: <every object that appears: the phone, cards, badges, the mascot, the logo mark ...>
MOTION:  enter expo.out 0.45–0.6 s; move power3.inOut 0.5 s; exit power2.in 0.3 s; camera sine.inOut;
         springs back.out(1.6–2) on chips and buttons (scale/position only); staggers 0.12–0.2 s.
         Hits land on beats (multiples of 0.5 s); moves start 0.1 s early.
SHOTS:
  s1 0–8     Hook. <what we see, what moves, the line on screen>. Exit: <how it hands off>.
  s2 8–14    Tension. ...
  s3 14–25   Proof. ...
  s4 25–32   Payoff. ...
  s5 32–36   End card. Logo builds; "<tagline>"; <URL> holds 2.5 s.
SOUND:   music bed: drums enter at <t>, build into <payoff t>, final hit at <end card t>.
         effects: whoosh on moves, pop on chips, click on taps, sparkle on reveals, impact on the payoff.
BANNED:  dark void; glow/particles/confetti; purple-blue gradients; glass cards;
         three cards entering together; title over a dimmed screenshot; logo docked in a corner;
         text moving while read; invented features; numbers not from the product.
QA:      0.0 (thumbnail not empty), then the middle of every shot and 0.2 s before every cut.
```
