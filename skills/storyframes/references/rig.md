# Rig: characters and crowds (`kit/rig.py`)

## A character

```python
from rig import person
TOLU = dict(skin="#8d5524", hair="#202124", shirt="#4285f4", pants="#3c4043", style="braids", badge="#4285f4")
html = f'<div id="s-tolu" class="wrap" style="left:560px; top:210px; width:330px">{person("tolu1", **TOLU)}</div>'
```

- `style`: `short`, `fade`, `afro`, `bun`, `braids`, `wrap` (head wrap, coloured by `wrap=`), `bald`.
- Extras: `glasses=True`, `beard=True`, `jacket="#hex"` (a blazer over the shirt).
- The viewBox is 160 × 360; the wrapper's width sets the size (330 px wide ≈ 740 px tall).
- Move the **wrapper** (`#s-tolu`) for position and scale; animate the **parts** for acting.
- Leads are written by hand as dicts so they look the same in every scene. `random_cast(seed, n)`
  makes extras.
- Represent the audience: vary skin, hair and dress on purpose. The default palettes are built for it.

### Parts and their pivots
| Part | Animate | svgOrigin |
| --- | --- | --- |
| `#{id}-legL` / `-legR` | rotation (walk) | `63 236` / `97 236` |
| `#{id}-armL` / `-armR` | rotation (wave, point, handshake) | `46 140` / `114 140` |
| `#{id}-head` | rotation (look around, shake), y (nod) | `80 120` |
| `#{id}-eyes` | scaleY (blink) | `80 75` |
| `#{id}-m-smile` `-m-open` `-m-worried` `-m-flat` | opacity, one at a time (use `face`) | — |
| `#{id}-brows-worried`, `#{id}-sweat` | opacity (sweat: then `y` down) | — |
| `#{id}-phone` | opacity (use `holdPhone`) | — |
| `#{id}-badge` | scale / fill (a badge that pings) | — |

Always pass `svgOrigin` when rotating SVG parts; `transformOrigin` is unreliable inside SVG.

### Acting helpers (from `RIG_JS`, pasted into every scene)
```js
face(tl, "tolu1", "worried", 6.25);   // smile | open | worried | flat
blink(tl, "tolu1", 5.0);              // a blink every 2–4 s keeps a held character alive
walk(tl, "tolu4", 0.1, 1.5, 3);       // limbs and bob; move the wrapper's x at the same time
wave(tl, "ada4", 1.95, 2);
holdPhone(tl, "tolu2", 4.1);          // arm up, phone on, head tilts down: "the idea"
nod(tl, "ada4", 3.0); lookAround(tl, "tolu1", 5.1);
pop(tl, "#chip", 2.0);                // springy scale-in for chips and tags
countUp(tl, "#h-num", 2000, 0.7, 1.9, "+");
```

Acting tips:
- Faces change *on* beats, a few frames before the line that explains them.
- A worried character + sweat drop + head shake = the problem. Phone out + smile = the turn.
- Handshake: right arm of the left character to −78°, left arm of the right character to +78°, then
  four small shakes of ±8°.

## A crowd

```python
from rig import crowd, highlight_layer, head_of
svg, people = crowd("hc", seed=11)        # about 600 people; back rows small, front rows large
good = [p for p in people if 4 <= p["row"] <= 8][:30]
layer = highlight_layer("hc-good", "hc", good, halo="#fde293")
```

- `people` entries: `id, x, y (feet), s (scale), row, sk, shirt`. Filter them to pick who matters.
- Same `seed` in every scene = the same room, so a person picked in scene 2 is in the same seat in
  scene 4. Give each scene its own `cid` (`hc`, `fc`, `mc`) because ids must be unique per document.
- **The selection move:** dim the base crowd to 0.16 opacity, fade a highlight layer of the chosen
  people to 1, then narrow to fewer with a second layer, then pin name tags with `head_of(p, scale)`.
- To show the crowd small inside a panel, wrap each layer in a div whose svg has
  `transform: scale(0.5); transform-origin: 0 0` and use `head_of(p, 0.5)` for tag positions.
- **The dive:** scale the panel ×3 toward one person's head (`transformOrigin: "0 0"`, x/y = −head × (scale − 1))
  as the scene's exit, then open the next scene on that person.
- Mark crowd containers `data-layout-ignore` (they are texture, not layout).
- Pick tagged people from separate x bands so their tags never collide (see the example's `best`).
