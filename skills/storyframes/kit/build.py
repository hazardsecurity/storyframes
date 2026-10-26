# storyframes example film: "500 people, one room" (24 s, 1920 x 1080, 30 fps).
# Generates compositions/*.html and index.html for a HyperFrames project. Edit this file and
# re-run it; never hand-edit the generated HTML (it is overwritten on every build).
#
# Run from the project folder:  python3 -I scripts/build.py
# Music (optional):             python3 -I scripts/make_music.py assets/audio/music.wav 24 8 14 20
# Effects (optional):           drop whoosh.mp3, pop.mp3, click.mp3, sparkle.mp3, impact.mp3 into assets/sfx/
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from rig import RIG_JS, crowd, font_faces, head_of, highlight_layer, person  # noqa: E402
from sfx import cue_tags  # noqa: E402

OUT = os.path.abspath(os.path.join(HERE, ".."))
os.makedirs(os.path.join(OUT, "compositions"), exist_ok=True)

# ---------------------------------------------------------------- the brief (change these first)
PRODUCT = "yourapp"
URL = "www.yourapp.com"
TAGLINE = 'Skip the small talk. Meet <em>the right people</em>'
ROOM = "Tech Summit 2026"
HEADCOUNT = 500
INK, MUTED, LINE, WASH = "#202124", "#5f6368", "#dadce0", "#f8f9fa"
BLUE, BLUE_DK, RED, YELLOW, GREEN = "#4285f4", "#2f6fd6", "#ea4335", "#fbbc05", "#34a853"
FILM = 24  # seconds; scenes below start on even seconds (bar lines at 120 bpm)

# Your own fonts: put display.woff2 / mono.woff2 in assets/fonts/. Without them the film uses Inter and
# JetBrains Mono, which the HyperFrames renderer supplies itself. Every family named here must be one of the two.
FONTS = font_faces(OUT)
SANS = '"Display", sans-serif' if "Display" in FONTS else '"Inter", sans-serif'
MONO = '"Mono", monospace' if "Mono" in FONTS else '"JetBrains Mono", monospace'


def scene(sid, css, html, js, bg="#ffffff"):
    """One sub-composition: a <template> with its own styles and a paused timeline registered by id."""
    return f'''<template>
  <style>
    {FONTS}
    #root {{ position: absolute; inset: 0; overflow: hidden; background: {bg}; font-family: {SANS}; color: {INK}; }}
    .t-big {{ font-weight: 700; letter-spacing: -0.04em; line-height: 1.04; }}
    .mono {{ font-family: {MONO}; font-weight: 600; letter-spacing: 0.08em; text-transform: uppercase; }}
    .wrap {{ position: absolute; }}
    .wrap svg.person {{ width: 100%; height: auto; display: block; }}
    .card {{ position: absolute; background: #fff; border: 3px solid {LINE}; border-bottom-width: 9px; border-radius: 34px; }}
    em {{ font-style: normal; }}
    {css}
  </style>
  <div id="root" data-composition-id="{sid}" data-width="1920" data-height="1080">
{html}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
    {RIG_JS}
{js}
    window.__timelines["{sid}"] = tl;
  </script>
</template>
'''


# ---------------------------------------------------------------- cast and crowd (seeded: same film every build)
LEAD = dict(skin="#8d5524", hair=INK, shirt=BLUE, pants="#3c4043", style="braids", badge=BLUE)
MATCH = dict(skin="#6b4226", hair=INK, shirt=RED, pants=INK, style="wrap", wrap=YELLOW, badge=RED, glasses=True)

hall_crowd, people = crowd("hc", seed=11)
find_crowd, _ = crowd("fc", seed=11)          # same seed = the same people, so scenes agree
meet_crowd, _ = crowd("mc", seed=11)
rng = random.Random(5)
middle = [p for p in people if 4 <= p["row"] <= 8 and 260 < p["x"] < 1660]
good = rng.sample(middle, 24)                     # people worth meeting
best = []                                         # three, spread across the room so their tags never overlap
for lo, hi in ((330, 720), (820, 1120), (1220, 1600)):
    band = [p for p in middle if 5 <= p["row"] <= 7 and lo < p["x"] < hi]
    best.append(band[len(band) // 2])
good += [p for p in best if p not in good]

# ---------------------------------------------------------------- scene 1: the room (0-8)
hall_css = f'''
    #h-wall {{ position: absolute; left: 0; right: 0; top: 0; height: 360px; background: #e8eaed; }}
    #h-stage {{ position: absolute; left: 360px; right: 360px; top: 250px; height: 70px; background: {BLUE_DK}; border-radius: 10px 10px 0 0; }}
    #h-screen {{ position: absolute; left: 640px; top: 40px; width: 640px; height: 200px; background: #fff; border: 6px solid {INK}; border-radius: 14px; display: grid; place-items: center; text-align: center; }}
    #h-screen b {{ display: block; font-size: 52px; letter-spacing: -0.03em; }}
    #h-screen span {{ font-size: 28px; color: {MUTED}; }}
    #h-cam {{ position: absolute; inset: 0; }}
    #h-crowd {{ position: absolute; left: 0; top: 0; }}
    #h-count {{ position: absolute; right: 60px; top: 400px; padding: 22px 34px; background: {INK}; color: #fff; border-radius: 26px; box-shadow: 0 8px 0 rgba(0,0,0,.25); text-align: right; }}
    #h-count .mono {{ font-size: 28px; color: #9aa0a6; }}
    #h-num {{ font-weight: 700; font-size: 104px; letter-spacing: -0.04em; line-height: 1; font-variant-numeric: tabular-nums; }}
    #h-band {{ left: 90px; top: 420px; width: 1060px; height: 240px; overflow: hidden; }}
    .h-line {{ position: absolute; left: 44px; top: 70px; width: 980px; font-size: 84px; white-space: nowrap; }}
    .h-line em {{ color: {RED}; }}
    #h-lead {{ left: 1170px; top: 1200px; width: 330px; }}
'''
hall_html = f'''
    <div id="h-cam" data-layout-allow-overflow>
      <div id="h-wall"></div>
      <div id="h-screen"><div><b>{ROOM}</b><span class="mono">Main hall</span></div></div>
      <div id="h-stage"></div>
      <div id="h-crowd" data-layout-ignore>{hall_crowd}</div>
    </div>
    <div id="h-count"><div class="mono">In the room</div><div id="h-num">0</div></div>
    <div id="h-band" class="card">
      <div id="h-l1" class="h-line t-big" data-layout-allow-overflow data-layout-allow-occlusion>{HEADCOUNT:,} people. One room.</div>
      <div id="h-l2" class="h-line t-big" data-layout-allow-overflow data-layout-allow-occlusion>You came to meet <em>a few</em></div>
    </div>
    <div id="h-lead" class="wrap" data-layout-allow-overflow>{person("lead1", **LEAD)}</div>
'''
hall_js = f'''
    tl.fromTo("#h-cam", {{ y: 60 }}, {{ y: -40, duration: 7.4, ease: "sine.inOut" }}, 0);           // slow camera tilt
    tl.fromTo("#h-band", {{ scale: 1.08, transformOrigin: "0% 50%" }}, {{ scale: 1, duration: 0.5, ease: "expo.out" }}, 0);
    tl.fromTo("#h-count", {{ x: 500 }}, {{ x: 0, duration: 0.55, ease: "expo.out" }}, 0.4);
    countUp(tl, "#h-num", {HEADCOUNT}, 0.7, 1.9, "+");
    // line swap on the bar: a line is hidden (opacity 0) whenever it is outside its mask, so checks stay clean
    tl.set("#h-l2", {{ opacity: 0 }}, 0);
    tl.to("#h-l1", {{ yPercent: -170, duration: 0.35, ease: "power2.in" }}, 3.4);
    tl.set("#h-l1", {{ opacity: 0 }}, 3.75);
    tl.fromTo("#h-l2", {{ yPercent: 170, opacity: 1 }}, {{ yPercent: 0, duration: 0.5, ease: "expo.out" }}, 3.6);
    tl.fromTo("#h-lead", {{ y: 0 }}, {{ y: -830, duration: 0.7, ease: "expo.out" }}, 4.3);          // the lead rises into frame
    face(tl, "lead1", "flat", 0);
    blink(tl, "lead1", 5.0);
    lookAround(tl, "lead1", 5.1);
    face(tl, "lead1", "worried", 6.25);
    tl.to(["#h-band", "#h-count"], {{ opacity: 0, duration: 0.25 }}, 7.35);                          // exit: push in on the lead
    tl.to("#h-lead", {{ scale: 1.6, x: -300, duration: 0.5, ease: "power3.in", transformOrigin: "50% 30%" }}, 7.5);
'''

# ---------------------------------------------------------------- scene 2: the right three light up (8-14)
S = 0.5  # the crowd drawn at half size inside the panel
tags = []
names = [("Ada", "Mentor"), ("Bayo", "Hiring"), ("Zainab", "Co-founder")]
for i, (p, (nm, why)) in enumerate(zip(best, names)):
    x, y = head_of(p, S)
    ty = y + 60 if i == 1 else y - 120   # the middle tag sits below its person
    tags.append(f'<div id="f-tag{i}" class="f-tag" style="left:{x - 115:.0f}px; top:{ty:.0f}px"><b>{nm}</b><span>{why}</span></div>')
ada_x, ada_y = head_of(best[0], S)

find_css = f'''
    #f-lead {{ left: 140px; top: 170px; width: 380px; }}
    #f-head {{ position: absolute; left: 700px; top: 70px; width: 1100px; height: 170px; overflow: hidden; }}
    .f-label {{ position: absolute; left: 0; top: 0; width: 1100px; }}
    .f-label .mono {{ font-size: 28px; color: {MUTED}; }}
    .f-label b {{ display: block; font-weight: 700; font-size: 84px; letter-spacing: -0.04em; line-height: 1.05; }}
    .f-label b em {{ color: {BLUE_DK}; }}
    #f-panel {{ left: 700px; top: 260px; width: {int(1920 * S) + 40}px; height: {int(1120 * S) - 110}px; padding: 20px; background: #e8eaed; overflow: hidden; }}
    #f-inner {{ position: absolute; left: 20px; top: -130px; width: {1920 * S}px; height: {1120 * S}px; }}
    #f-inner > div {{ position: absolute; left: 0; top: 0; }}
    .f-layer svg {{ transform: scale({S}); transform-origin: 0 0; }}
    .f-tag {{ position: absolute; width: 230px; padding: 10px 14px; background: #fff; border: 3px solid {INK}; border-radius: 18px; text-align: center; box-shadow: 0 6px 0 rgba(0,0,0,.18); }}
    .f-tag b {{ display: block; font-size: 30px; }} .f-tag span {{ font-size: 28px; color: {MUTED}; }}
'''
find_html = f'''
    <div id="f-lead" class="wrap">{person("lead2", **LEAD)}</div>
    <div id="f-head" data-layout-allow-overflow data-layout-allow-occlusion>
      <div id="f-lab0" class="f-label" data-layout-allow-occlusion><div class="mono">Everyone here</div><b>{HEADCOUNT:,} strangers</b></div>
      <div id="f-lab1" class="f-label" data-layout-allow-occlusion><div class="mono">{PRODUCT} reads every badge</div><b><em>The right three</em>, lit up</b></div>
    </div>
    <div id="f-panel" class="card" data-layout-ignore>
      <div id="f-inner">
        <div id="f-base" class="f-layer">{find_crowd}</div>
        <div id="f-good" class="f-layer">{highlight_layer("f-good-svg", "fc", good, halo="#fde293")}</div>
        <div id="f-best" class="f-layer">{highlight_layer("f-best-svg", "fc", best, halo=GREEN)}</div>
        {"".join(tags)}
      </div>
    </div>
'''
find_js = f'''
    tl.fromTo("#f-lead", {{ scale: 1.5, x: 200 }}, {{ scale: 1, x: 0, duration: 0.6, ease: "expo.out", transformOrigin: "50% 30%" }}, 0);
    face(tl, "lead2", "worried", 0);
    tl.fromTo("#f-panel", {{ x: 1200 }}, {{ x: 0, duration: 0.6, ease: "expo.out" }}, 0.25);
    tl.set(["#f-good", "#f-best", ".f-tag"], {{ opacity: 0 }}, 0);
    tl.set("#f-lab1", {{ yPercent: 230, opacity: 0 }}, 0);
    tl.fromTo("#f-lab0", {{ yPercent: 230 }}, {{ yPercent: 0, duration: 0.45, ease: "expo.out" }}, 0.45);
    holdPhone(tl, "lead2", 1.6);                                                                    // the idea: phone out
    face(tl, "lead2", "smile", 1.7);
    tl.to("#f-base", {{ opacity: 0.16, duration: 0.35, ease: "power2.out" }}, 2.0);                // dim the room, light the good ones
    tl.to("#f-good", {{ opacity: 1, duration: 0.2 }}, 2.0);
    tl.to("#f-lab0", {{ yPercent: -230, duration: 0.3, ease: "power2.in" }}, 2.0);
    tl.to("#f-lab1", {{ yPercent: 0, opacity: 1, duration: 0.45, ease: "expo.out" }}, 2.15);
    tl.to("#f-good", {{ opacity: 0.35, duration: 0.3 }}, 3.4);                                     // narrow to the best three
    tl.to("#f-best", {{ opacity: 1, duration: 0.25 }}, 3.4);
    tl.fromTo([".f-tag"], {{ opacity: 0, scale: 0.4, y: 30 }}, {{ opacity: 1, scale: 1, y: 0, duration: 0.45, ease: "back.out(1.8)", stagger: 0.15 }}, 3.5);
    blink(tl, "lead2", 4.4);
    tl.to(["#f-lead", "#f-head"], {{ x: -1300, duration: 0.45, ease: "power3.in" }}, 5.45);       // exit: dive into Ada's tag
    tl.to("#f-panel", {{ scale: 3.2, x: {-(ada_x * 2.2):.0f}, y: {-(ada_y * 2.2) + 200:.0f}, duration: 0.5, ease: "power3.in", transformOrigin: "0 0" }}, 5.5);
'''

# ---------------------------------------------------------------- scene 3: they meet (14-20)
meet_css = f'''
    #m-back {{ position: absolute; left: 0; top: -60px; opacity: 0.32; }}
    #m-floor {{ position: absolute; left: 0; right: 0; top: 800px; bottom: 0; background: linear-gradient(#f1f3f4, #e8eaed); }}
    #m-lead {{ left: 560px; top: 210px; width: 330px; }}
    #m-match {{ left: 1030px; top: 210px; width: 330px; }}
    #m-title {{ position: absolute; left: 0; right: 0; top: 70px; text-align: center; font-size: 84px; }}
    #m-title em {{ color: {GREEN}; }}
    #m-chip {{ position: absolute; left: 0; right: 0; top: 940px; text-align: center; font-weight: 700; font-size: 56px; color: #18733a; }}
'''
meet_html = f'''
    <div id="m-back" data-layout-ignore>{meet_crowd}</div>
    <div id="m-floor"></div>
    <div id="m-title" class="t-big">From {HEADCOUNT:,} strangers to <em>the right people</em></div>
    <div id="m-chip">✓ Met in person</div>
    <div id="m-lead" class="wrap">{person("lead3", **LEAD)}</div>
    <div id="m-match" class="wrap">{person("ada3", **MATCH)}</div>
'''
meet_js = '''
    tl.fromTo("#root", { scale: 1.15 }, { scale: 1, duration: 0.6, ease: "expo.out" }, 0);
    tl.fromTo("#m-lead", { x: -900 }, { x: 0, duration: 1.6, ease: "power2.out" }, 0.1);              // walk in from both sides
    tl.fromTo("#m-match", { x: 900 }, { x: 0, duration: 1.6, ease: "power2.out" }, 0.2);
    walk(tl, "lead3", 0.1, 1.5, 3);
    walk(tl, "ada3", 0.2, 1.5, 3);
    face(tl, "lead3", "smile", 0); face(tl, "ada3", "smile", 0);
    wave(tl, "ada3", 1.95, 2);
    face(tl, "lead3", "open", 2.0); blink(tl, "lead3", 2.3); face(tl, "lead3", "smile", 2.6);
    tl.fromTo("#m-title", { opacity: 0, filter: "blur(8px)" }, { opacity: 1, filter: "blur(0px)", duration: 0.2 }, 2.4);
    tl.to("#lead3-armR", { rotation: -78, svgOrigin: "114 140", duration: 0.4, ease: "back.out(1.4)" }, 3.6);   // handshake on the bar
    tl.to("#ada3-armL", { rotation: 78, svgOrigin: "46 140", duration: 0.4, ease: "back.out(1.4)" }, 3.65);
    tl.to("#lead3-armR", { rotation: -70, svgOrigin: "114 140", duration: 0.12, yoyo: true, repeat: 3, ease: "sine.inOut" }, 4.05);
    tl.to("#ada3-armL", { rotation: 70, svgOrigin: "46 140", duration: 0.12, yoyo: true, repeat: 3, ease: "sine.inOut" }, 4.05);
    face(tl, "ada3", "open", 4.1); face(tl, "ada3", "smile", 4.6);
    tl.fromTo("#m-chip", { opacity: 0, scale: 0.4, y: 30 }, { opacity: 1, scale: 1, y: 0, duration: 0.4, ease: "back.out(2)" }, 4.3);
    tl.to("#root", { opacity: 0, scale: 0.94, duration: 0.35, ease: "power2.in" }, 5.65);
'''

# ---------------------------------------------------------------- scene 4: end card (20-24)
end_css = f'''
    #e-word-mask {{ position: absolute; left: 0; right: 0; top: 300px; overflow: hidden; text-align: center; }}
    #e-word {{ display: inline-block; font-weight: 700; font-size: 140px; letter-spacing: -0.045em; line-height: 1.1; }}
    #e-line {{ position: absolute; left: 0; right: 0; top: 540px; text-align: center; font-weight: 700; font-size: 60px; letter-spacing: -0.02em; }}
    #e-line em {{ color: {BLUE}; }}
    #e-cta {{ position: absolute; left: 50%; top: 690px; width: 640px; margin-left: -320px; height: 120px; border-radius: 28px; background: {BLUE}; box-shadow: 0 9px 0 {BLUE_DK}; color: #fff; display: grid; place-items: center; font-weight: 700; font-size: 50px; }}
'''
end_html = f'''
    <div id="e-word-mask"><div id="e-word" data-layout-allow-overflow>{PRODUCT}</div></div>
    <div id="e-line">{TAGLINE}</div>
    <div id="e-cta">{URL}</div>
'''
end_js = '''
    tl.fromTo("#e-word", { yPercent: 110 }, { yPercent: 0, duration: 0.55, ease: "expo.out" }, 0.2);
    tl.fromTo("#e-line", { opacity: 0, y: 24 }, { opacity: 1, y: 0, duration: 0.4, ease: "expo.out" }, 0.7);
    tl.fromTo("#e-cta", { scale: 0.5, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.45, ease: "back.out(1.8)" }, 1.0);
    tl.set({}, {}, 4);   // hold to the end of the scene
'''

# ---------------------------------------------------------------- assemble
scenes = [  # id, start, duration, css, html, js, background
    ("hall", 0, 8, hall_css, hall_html, hall_js, WASH),
    ("find", 8, 6, find_css, find_html, find_js, "#fef7e0"),
    ("meet", 14, 6, meet_css, meet_html, meet_js, "#ffffff"),
    ("endcard", 20, 4, end_css, end_html, end_js, "#ffffff"),
]
assert sum(s[2] for s in scenes) == FILM
for sid, _, _, css, html, js, bg in scenes:
    open(os.path.join(OUT, "compositions", f"{sid}.html"), "w").write(scene(sid, css, html, js, bg))

# sound: (picture time in the film, effect name, volume). Each lands its peak on the picture.
cues = [
    (0.05, "whoosh", 0.35), (0.45, "pop", 0.35), (3.5, "whoosh", 0.28), (4.45, "whoosh", 0.4), (7.7, "whoosh", 0.5),
    (8.15, "whoosh", 0.35), (9.6, "click", 0.45), (10.0, "sparkle", 0.3), (11.5, "pop", 0.3), (11.65, "pop", 0.32), (11.8, "pop", 0.34),
    (13.45, "whoosh", 0.5), (14.2, "whoosh", 0.3), (18.05, "impact", 0.45), (18.3, "pop", 0.4), (19.65, "whoosh", 0.4),
    (20.2, "whoosh", 0.3), (20.75, "pop", 0.4), (21.0, "pop", 0.45),
]
sfx_tags, missing = cue_tags(cues, os.path.join(OUT, "assets", "sfx"), FILM)
music = os.path.exists(os.path.join(OUT, "assets", "audio", "music.wav"))
music_tag = f'      <audio id="music" src="assets/audio/music.wav" data-start="0" data-duration="{FILM}" data-track-index="20" data-volume="1"></audio>' if music else ""

hosts = "\n".join(
    f'      <div id="{sid}" data-composition-id="{sid}" data-composition-src="compositions/{sid}.html" data-start="{st}" '
    f'data-duration="{du}" data-track-index="1" data-track-kind="graphics" data-width="1920" data-height="1080"></div>'
    for sid, st, du, *_ in scenes)
index = f'''<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1920, height=1080" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
      {FONTS}
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ margin: 0; width: 1920px; height: 1080px; overflow: hidden; background: #ffffff; }}
      #root {{ position: relative; width: 1920px; height: 1080px; overflow: hidden; font-family: {SANS}; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{FILM}" data-width="1920" data-height="1080">
{hosts}
{music_tag}
{chr(10).join(sfx_tags)}
    </div>
    <script>
      window.__timelines = window.__timelines || {{}};
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
'''
open(os.path.join(OUT, "index.html"), "w").write(index)
print(f"built {len(scenes)} scenes, {len(people)} people in the room, {len(sfx_tags)} sounds, music: {'yes' if music else 'no'}")
if missing:
    print("no file yet for effects:", ", ".join(missing), "(add them to assets/sfx/ and rebuild)")
