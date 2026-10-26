"""storyframes rig: flat SVG characters and crowds for HyperFrames films.

Everything is generated into static HTML/SVG at build time (seeded), so the render is
deterministic and every part has a stable id that a GSAP timeline can animate.

person(pid, ...) -> an <svg> character, 160 x 360 viewBox, with animatable parts:
  #{pid}                    the whole character (move it with x / y / scale)
  #{pid}-legL #{pid}-legR   rotate around the hips      (svgOrigin "63 236" / "97 236")
  #{pid}-armL #{pid}-armR   rotate around the shoulders (svgOrigin "46 140" / "114 140")
  #{pid}-head               tilt around the neck        (svgOrigin "80 120")
  #{pid}-eyes               scaleY for blinks           (svgOrigin "80 75")
  #{pid}-m-smile / -m-open / -m-worried / -m-flat   mouth states (toggle opacity, see face())
  #{pid}-brows-worried      opacity
  #{pid}-sweat              opacity, then drop it with y
  #{pid}-phone              inside the right arm, opacity (see holdPhone())
  #{pid}-badge              the name badge on the chest (tint it, pop it)

crowd(cid, ...) -> (svg, people): a room full of people built from one <symbol>, back rows
small and front rows large. people is a list of dicts (id, x, y, s, row, sk, shirt) you can
filter to pick "these ones" and redraw them on top with highlight_layer().

RIG_JS is pasted into every scene's <script>: face, blink, walk, wave, holdPhone, nod, pop.
Each helper adds tweens to the paused scene timeline at an absolute time, so every frame is a
pure function of time (seekable, which HyperFrames requires).
"""
import os
import random

INK = "#202124"
SKINS = ["#8d5524", "#a0673f", "#6b4226", "#c68642", "#5a3825", "#7a4a2a", "#b5774a", "#e0ac69", "#f1c27d"]
# Default shirt palette. Pass your brand's colours to crowd(shirts=[...]) instead.
SHIRTS = ["#4285f4", "#ea4335", "#fbbc05", "#34a853", "#5f6368", "#2f6fd6", "#c5291b", "#23853d", "#9aa0a6", "#202124", "#fef7e0", "#e8f0fe"]
HAIR_STYLES = ["short", "fade", "afro", "bun", "braids", "wrap", "bald"]


def _hair(style, hair, wrap):
    back, front = "", ""
    if style == "short":
        front = f'<path d="M40 66 Q40 24 80 24 Q120 24 120 66 Q112 44 80 42 Q48 44 40 66 Z" fill="{hair}"/>'
    elif style == "fade":
        front = f'<path d="M42 58 Q46 28 80 28 Q114 28 118 58 Q108 42 80 40 Q52 42 42 58 Z" fill="{hair}"/>'
    elif style == "afro":
        back = f'<circle cx="80" cy="54" r="54" fill="{hair}"/>'
        front = f'<path d="M38 62 Q44 30 80 30 Q116 30 122 62 Q104 48 80 48 Q56 48 38 62 Z" fill="{hair}"/>'
    elif style == "bun":
        back = f'<circle cx="80" cy="18" r="17" fill="{hair}"/>'
        front = f'<path d="M40 66 Q40 24 80 24 Q120 24 120 66 Q110 40 80 40 Q50 40 40 66 Z" fill="{hair}"/>'
    elif style == "braids":
        back = (f'<path d="M36 60 Q34 120 46 150 L60 150 Q52 110 54 70 Z" fill="{hair}"/>'
                f'<path d="M124 60 Q126 120 114 150 L100 150 Q108 110 106 70 Z" fill="{hair}"/>')
        front = f'<path d="M38 66 Q38 22 80 22 Q122 22 122 66 Q112 40 80 40 Q48 40 38 66 Z" fill="{hair}"/>'
    elif style == "wrap":
        back = f'<ellipse cx="80" cy="22" rx="30" ry="18" fill="{wrap}"/>'
        front = (f'<path d="M34 66 Q28 14 80 10 Q132 14 126 66 Q104 40 80 42 Q56 40 34 66 Z" fill="{wrap}"/>'
                 f'<path d="M50 30 Q80 18 112 34" stroke="rgba(0,0,0,.18)" stroke-width="4" fill="none" stroke-linecap="round"/>')
    return back, front


def person(pid, skin="#8d5524", hair="#202124", shirt="#4285f4", pants="#3c4043", style="short",
           badge="#4285f4", wrap="#ea4335", glasses=False, jacket=None, beard=False, cls=""):
    """One character. Put it in a sized wrapper (e.g. <div style="width:330px">) and animate the ids."""
    back, front = _hair(style, hair, wrap)
    shade = "rgba(0,0,0,.14)"
    jacket_svg = ""
    if jacket:
        jacket_svg = (f'<path d="M36 164 Q36 128 64 128 L72 128 L80 180 L88 128 L96 128 Q124 128 124 164 L124 250 L36 250 Z" fill="{jacket}"/>'
                      f'<path d="M72 128 L80 180 L88 128" fill="none" stroke="rgba(0,0,0,.25)" stroke-width="3"/>')
    glasses_svg = ('<g fill="none" stroke="#202124" stroke-width="3.5"><circle cx="66" cy="74" r="11"/><circle cx="94" cy="74" r="11"/>'
                   '<path d="M77 74 L83 74"/></g>') if glasses else ""
    beard_svg = f'<path d="M50 88 Q52 118 80 120 Q108 118 110 88 Q100 106 80 106 Q60 106 50 88 Z" fill="{hair}"/>' if beard else ""
    sleeve = jacket or shirt
    return f'''<svg id="{pid}" class="person {cls}" viewBox="0 0 160 360" aria-hidden="true" style="overflow:visible">
  <ellipse cx="80" cy="352" rx="46" ry="7" fill="{INK}" opacity=".12"/>
  <g id="{pid}-legL"><rect x="52" y="232" width="22" height="108" rx="11" fill="{pants}"/><ellipse cx="60" cy="342" rx="17" ry="9" fill="{INK}"/></g>
  <g id="{pid}-legR"><rect x="86" y="232" width="22" height="108" rx="11" fill="{pants}"/><ellipse cx="100" cy="342" rx="17" ry="9" fill="{INK}"/></g>
  <g id="{pid}-body">
    <rect x="36" y="128" width="88" height="122" rx="34" fill="{shirt}"/>
    {jacket_svg}
    <path d="M62 132 L80 182 L98 132" fill="none" stroke="{badge}" stroke-width="4" stroke-linecap="round"/>
    <g id="{pid}-badge"><rect x="66" y="178" width="28" height="34" rx="5" fill="#fff" stroke="#dadce0" stroke-width="2"/>
      <rect x="66" y="178" width="28" height="9" rx="4" fill="{badge}"/></g>
  </g>
  <g id="{pid}-armL"><rect x="30" y="134" width="22" height="96" rx="11" fill="{sleeve}"/><circle cx="41" cy="228" r="12" fill="{skin}"/></g>
  <g id="{pid}-armR"><rect x="108" y="134" width="22" height="96" rx="11" fill="{sleeve}"/><circle cx="119" cy="228" r="12" fill="{skin}"/>
    <g id="{pid}-phone" opacity="0"><rect x="104" y="196" width="32" height="54" rx="7" fill="{INK}"/><rect x="108" y="201" width="24" height="42" rx="3" fill="{badge}"/></g></g>
  <rect x="70" y="102" width="20" height="30" rx="6" fill="{skin}"/><rect x="70" y="102" width="20" height="12" fill="{shade}"/>
  <g id="{pid}-head">
    {back}
    <circle cx="40" cy="78" r="9" fill="{skin}"/><circle cx="120" cy="78" r="9" fill="{skin}"/>
    <ellipse cx="80" cy="72" rx="40" ry="44" fill="{skin}"/>
    {front}
    {beard_svg}
    <ellipse cx="58" cy="90" rx="7" ry="4" fill="#ea4335" opacity=".22"/><ellipse cx="102" cy="90" rx="7" ry="4" fill="#ea4335" opacity=".22"/>
    <g id="{pid}-eyes"><ellipse cx="66" cy="75" rx="5" ry="6.5" fill="{INK}"/><ellipse cx="94" cy="75" rx="5" ry="6.5" fill="{INK}"/>
      <circle cx="67.5" cy="72.5" r="1.8" fill="#fff"/><circle cx="95.5" cy="72.5" r="1.8" fill="#fff"/></g>
    {glasses_svg}
    <g id="{pid}-brows-worried" opacity="0"><path d="M56 64 L72 57" stroke="{INK}" stroke-width="3.5" stroke-linecap="round"/><path d="M104 64 L88 57" stroke="{INK}" stroke-width="3.5" stroke-linecap="round"/></g>
    <path id="{pid}-m-smile" d="M68 93 Q80 104 92 93" stroke="{INK}" stroke-width="4" fill="none" stroke-linecap="round"/>
    <ellipse id="{pid}-m-open" cx="80" cy="97" rx="8" ry="7" fill="{INK}" opacity="0"/>
    <path id="{pid}-m-worried" d="M70 100 Q80 92 90 100" stroke="{INK}" stroke-width="4" fill="none" stroke-linecap="round" opacity="0"/>
    <path id="{pid}-m-flat" d="M70 97 L90 97" stroke="{INK}" stroke-width="4" fill="none" stroke-linecap="round" opacity="0"/>
    <path id="{pid}-sweat" d="M124 52 Q130 62 124 68 Q118 62 124 52 Z" fill="#8ab4f8" opacity="0"/>
  </g>
</svg>'''


def random_cast(seed, n, shirts=SHIRTS):
    """n distinct-looking character kwargs, seeded. Handy for extras; write your leads by hand."""
    rng = random.Random(seed)
    out = []
    for _ in range(n):
        out.append(dict(skin=rng.choice(SKINS), hair=rng.choice(["#202124", "#3b2a20", "#5a3825"]), shirt=rng.choice(shirts),
                        pants=rng.choice(["#3c4043", "#202124", "#1f3a68"]), style=rng.choice(HAIR_STYLES),
                        badge=rng.choice(shirts), wrap=rng.choice(shirts), glasses=rng.random() < 0.25, beard=rng.random() < 0.15))
    return out


def crowd(cid, width=1920, top=330, bottom=1120, rows=11, seed=7, base_scale=0.5, front_scale=1.7, shirts=SHIRTS):
    """A room full of people, back rows small, front rows large (simple perspective).
    Returns (svg, people). About 600 people at the defaults; one <symbol> keeps it cheap to render."""
    rng = random.Random(seed)
    people = []
    parts = [f'<svg id="{cid}" viewBox="0 0 {width} {bottom}" width="{width}" height="{bottom}" aria-hidden="true" style="overflow:visible">',
             '<defs><symbol id="%s-fig" viewBox="0 0 40 60" overflow="visible">'
             '<path d="M1 60 Q1 30 20 28 Q39 30 39 60 Z" fill="currentColor"/>'
             '<circle cx="20" cy="14" r="11" fill="var(--sk)"/></symbol></defs>' % cid]
    n = 0
    for r in range(rows):
        t = r / (rows - 1)
        s = base_scale + (front_scale - base_scale) * (t ** 1.6)
        y = top + (bottom - top) * (t ** 1.25)
        step = 40 * s * 1.08
        x = -step * 0.5 + (step * 0.5 if r % 2 else 0)
        while x < width + step:
            jx = rng.uniform(-0.18, 0.18) * step
            jy = rng.uniform(-6, 6) * s
            people.append({"id": f"{cid}-p{n}", "x": x + jx, "y": y + jy, "s": s, "row": r,
                           "sk": rng.choice(SKINS), "shirt": rng.choice(shirts)})
            n += 1
            x += step
    for p in people:
        w, h = 40 * p["s"], 60 * p["s"]
        parts.append(f'<use href="#{cid}-fig" x="{p["x"]:.1f}" y="{p["y"] - h:.1f}" width="{w:.1f}" height="{h:.1f}" style="color:{p["shirt"]};--sk:{p["sk"]}"/>')
    parts.append("</svg>")
    return "".join(parts), people


def highlight_layer(lid, cid, people, color=None, width=1920, bottom=1120, halo=None):
    """The same people drawn again on top ("these ones match"), optionally recoloured, with an
    optional soft disc behind each so they still read when the crowd is shown small.
    Dim the base crowd and fade this layer in to make a selection."""
    out = [f'<svg id="{lid}" viewBox="0 0 {width} {bottom}" width="{width}" height="{bottom}" aria-hidden="true" style="overflow:visible">']
    if halo:
        for p in people:
            out.append(f'<circle cx="{p["x"] + 20 * p["s"]:.1f}" cy="{p["y"] - 34 * p["s"]:.1f}" r="{40 * p["s"]:.1f}" fill="{halo}" opacity=".85"/>')
    for p in people:
        w, h = 40 * p["s"], 60 * p["s"]
        out.append(f'<use href="#{cid}-fig" x="{p["x"]:.1f}" y="{p["y"] - h:.1f}" width="{w:.1f}" height="{h:.1f}" style="color:{color or p["shirt"]};--sk:{p["sk"]}"/>')
    out.append("</svg>")
    return "".join(out)


def head_of(p, scale=1.0):
    """Frame position of a crowd person's head (for pinning a name tag or a camera dive)."""
    return (p["x"] + 20 * p["s"]) * scale, (p["y"] - 46 * p["s"]) * scale


def font_faces(project_dir, display="Display", mono="Mono"):
    """@font-face rules for assets/fonts/display.woff2 and assets/fonts/mono.woff2 if present.
    Renders are offline, so ship the font files with the project (any OFL font, e.g. Inter or Space Grotesk)."""
    rules = []
    for fam, file in ((display, "display.woff2"), (mono, "mono.woff2")):
        if os.path.exists(os.path.join(project_dir, "assets", "fonts", file)):
            rules.append(f'@font-face {{ font-family: "{fam}"; src: url("assets/fonts/{file}") format("woff2"); font-weight: 300 800; }}')
    return "\n    ".join(rules)


RIG_JS = '''
    // --- storyframes rig: every move is a tween on the scene timeline at an absolute time ---
    const face = (tl, p, mood, t) => {
      for (const m of ["smile", "open", "worried", "flat"]) tl.set(`#${p}-m-${m}`, { opacity: m === mood ? 1 : 0 }, t);
      tl.set(`#${p}-brows-worried`, { opacity: mood === "worried" ? 1 : 0 }, t);
    };
    const blink = (tl, p, t) => tl.to(`#${p}-eyes`, { scaleY: 0.1, svgOrigin: "80 75", duration: 0.06, yoyo: true, repeat: 1, ease: "power1.inOut" }, t);
    const walk = (tl, p, t, dur, steps) => {
      const d = dur / (steps * 2), r = steps * 2 - 1;
      tl.to(`#${p}-legL`, { rotation: 14, svgOrigin: "63 236", duration: d, yoyo: true, repeat: r, ease: "sine.inOut" }, t);
      tl.to(`#${p}-legR`, { rotation: -14, svgOrigin: "97 236", duration: d, yoyo: true, repeat: r, ease: "sine.inOut" }, t);
      tl.to(`#${p}-armL`, { rotation: -12, svgOrigin: "46 140", duration: d, yoyo: true, repeat: r, ease: "sine.inOut" }, t);
      tl.to(`#${p}-armR`, { rotation: 12, svgOrigin: "114 140", duration: d, yoyo: true, repeat: r, ease: "sine.inOut" }, t);
      tl.to(`#${p}`, { y: "-=8", duration: d, yoyo: true, repeat: r, ease: "sine.inOut" }, t);
    };
    const wave = (tl, p, t, times = 2) => {
      tl.to(`#${p}-armR`, { rotation: -150, svgOrigin: "114 140", duration: 0.25, ease: "back.out(1.6)" }, t);
      tl.to(`#${p}-armR`, { rotation: -125, svgOrigin: "114 140", duration: 0.18, yoyo: true, repeat: times * 2 - 1, ease: "sine.inOut" }, t + 0.25);
      tl.to(`#${p}-armR`, { rotation: 0, svgOrigin: "114 140", duration: 0.3, ease: "power2.out" }, t + 0.25 + times * 0.36);
    };
    const holdPhone = (tl, p, t) => {
      tl.to(`#${p}-armR`, { rotation: -62, svgOrigin: "114 140", duration: 0.35, ease: "back.out(1.4)" }, t);
      tl.to(`#${p}-phone`, { opacity: 1, duration: 0.12 }, t + 0.1);
      tl.to(`#${p}-head`, { rotation: 8, svgOrigin: "80 120", duration: 0.35, ease: "power2.out" }, t + 0.05);
    };
    const nod = (tl, p, t, times = 2) => tl.to(`#${p}-head`, { y: 6, duration: 0.14, yoyo: true, repeat: times * 2 - 1, ease: "sine.inOut" }, t);
    const lookAround = (tl, p, t) => {
      tl.to(`#${p}-head`, { rotation: -10, svgOrigin: "80 120", duration: 0.4, ease: "sine.inOut" }, t);
      tl.to(`#${p}-head`, { rotation: 10, svgOrigin: "80 120", duration: 0.5, ease: "sine.inOut" }, t + 0.5);
      tl.to(`#${p}-head`, { rotation: 0, svgOrigin: "80 120", duration: 0.35, ease: "sine.inOut" }, t + 1.1);
    };
    const pop = (tl, sel, t, from = 0) => tl.fromTo(sel, { scale: from, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.4, ease: "back.out(1.9)" }, t);
    // A number that counts up. Formatting runs in onUpdate, so it stays a pure function of time.
    const countUp = (tl, sel, to, t, dur = 1.6, suffix = "") => {
      const c = { n: 0 };
      tl.fromTo(c, { n: 0 }, { n: to, duration: dur, ease: "power2.out",
        onUpdate: () => { document.querySelector(sel).textContent = Math.round(c.n).toLocaleString("en-US") + (c.n > to - 0.5 ? suffix : ""); } }, t);
    };
'''
