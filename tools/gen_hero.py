from svgkit import *
import math

W, H = 1200, 420
G = Glyphs()
body = []

extra = f'''
<pattern id="dots" width="24" height="24" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1" fill="#1A2144"/></pattern>
<radialGradient id="vign" cx="72%" cy="50%" r="60%"><stop offset="0" stop-color="#141B3D" stop-opacity=".9"/><stop offset="1" stop-color="{INK}" stop-opacity="0"/></radialGradient>
<clipPath id="frame"><rect width="{W}" height="{H}" rx="18"/></clipPath>
'''
body.append(f'<g clip-path="url(#frame)"><rect width="{W}" height="{H}" fill="{INK}"/>'
            f'<rect width="{W}" height="{H}" fill="url(#dots)"/><rect width="{W}" height="{H}" fill="url(#vign)"/></g>')
body.append(f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="18" fill="none" stroke="{LINE}"/>')

X0 = 64
s, _ = G.run(DISPLAY, "MAZIN", X0, 176, 140, fill=TEXT, tracking=3)
body.append(s)
s, _ = G.run(DISPLAY, "SHAMSHAD", X0, 306, 140, fill=TEXT, tracking=3)
body.append(s)

TY = 368
FS = 20
s, _ = G.run(MONO, "$", X0 + 2, TY, FS, fill=TEAL)
body.append(s)
TX = X0 + 2 + 2 * MONO.advance("a", FS)
phrases = [
    "backend & distributed systems",
    "assistant system engineer at TCS",
    "LeetCode Knight, Codeforces Specialist",
    "one seat, one booking, zero races",
]
T2 = 18.0
win = T2 / len(phrases)
cursor_pts = []
live_typing = []
for k, ph in enumerate(phrases):
    run, edges = G.run(MONO, ph, TX, TY, FS, fill=SOFT)
    st = k * win + 0.25
    anim, ts, vs = typing_anim(edges, TX, st, 0.05, T2, t_delete=k * win + 3.55, del_per_char=0.016)
    cid = f"tp{k}"
    extra += f'<clipPath id="{cid}"><rect x="{TX}" y="{TY-22}" width="0" height="30">{anim}</rect></clipPath>'
    live_typing.append(f'<g clip-path="url(#{cid})">{run}</g>')
    for t, v in zip(ts, vs):
        if k > 0 and t == 0:
            continue
        cursor_pts.append((t, v))
cursor_pts.sort()
ct, cv = [], []
for t, v in cursor_pts:
    if ct and t <= ct[-1]:
        t = ct[-1] + 0.001
    ct.append(t); cv.append(v)
cur = (f'<rect class="blink" x="{TX}" y="{TY-17}" width="11" height="21" rx="1.5" fill="{TEAL}">'
       f'<animate attributeName="x" dur="{T2}s" repeatCount="indefinite" calcMode="discrete" '
       f'keyTimes="{kt(ct, T2)}" values="{";".join(f"{TX + v + 1:.1f}" for v in cv)}"/></rect>')

T = 6.0
LX, LY = 990, 210
CONV = (954, LY)
DBX = 1124
lanes = [110, 160, 210, 260, 310]
OX = 690

scene_static = []
for y in lanes:
    scene_static.append(f'<line x1="{OX}" y1="{y}" x2="{CONV[0]}" y2="{CONV[1]}" stroke="{LINE2}" stroke-width="1.5" stroke-dasharray="2 7" stroke-linecap="round"/>')
    scene_static.append(f'<circle cx="{OX}" cy="{y}" r="5" fill="{PANEL}" stroke="{LINE2}" stroke-width="1.5"/>')
scene_static.append(f'<line x1="1014" y1="{LY}" x2="{DBX-20}" y2="{LY}" stroke="{LINE2}" stroke-width="1.5" stroke-dasharray="2 7" stroke-linecap="round"/>')

lbl = "SET lock:seat:14A NX PX 3000"
lw = MONO.width(lbl, 13)
s, _ = G.run(MONO, lbl, LX - lw / 2, 160, 13, fill=MUTED)
scene_static.append(s)
s, _ = G.run(MONO, "seats", DBX - MONO.width("seats", 12) / 2, 262, 12, fill=MUTED)
scene_static.append(s)
punch = "5 requests. 1 booking. 0 double-bookings."
pw = MONO.width(punch, 14)
s, _ = G.run(MONO, punch, 925 - pw / 2, TY, 14, fill=MUTED)
scene_static.append(s)


def spline_anim(attr, keytimes, values, T, typ=None, splines=None):
    kts = kt(keytimes, T)
    t = f' type="{typ}"' if typ else ""
    if splines:
        return (f'<animateTransform attributeName="transform"{t} dur="{T}s" repeatCount="indefinite" '
                f'calcMode="spline" keyTimes="{kts}" keySplines="{";".join(splines)}" values="{";".join(values)}"/>')
    return (f'<animate attributeName="{attr}" dur="{T}s" repeatCount="indefinite" '
            f'keyTimes="{kts}" values="{";".join(values)}"/>')


def discrete(attr, keytimes, values, T):
    return (f'<animate attributeName="{attr}" dur="{T}s" repeatCount="indefinite" calcMode="discrete" '
            f'keyTimes="{kt(keytimes, T)}" values="{";".join(values)}"/>')


LIN = "0 0 1 1"
EASE_IN = "0.5 0 0.9 0.6"
EASE_OUT = "0.2 0.7 0.3 1"
EASE = "0.45 0 0.2 1"

packets = []
WIN_LANE = 2
arrivals = {2: 1.5, 1: 1.72, 3: 1.9, 0: 2.05, 4: 2.2}
for i, y in enumerate(lanes):
    A = arrivals[i]
    L = A - 1.0
    ox, oy = OX, y
    dx, dy = CONV[0] - ox, CONV[1] - oy
    ln = math.hypot(dx, dy)
    ux, uy = dx / ln, dy / ln
    if i == WIN_LANE:
        pts = [(ox, oy), (ox, oy), CONV, (DBX - 20, LY), (DBX - 20, LY)]
        times = [0, L, A, A + 0.7, T]
        spl = [LIN, EASE_IN, LIN, LIN]
        fill = discrete("fill", [0, A], [INDIGO, TEAL], T)
        op_t = [0, L, L + 0.08, A + 0.7, A + 0.95, T]
        op_v = ["0", "0", "1", "1", "0", "0"]
    else:
        stop = (CONV[0] - ux * 30, CONV[1] - uy * 30)
        back = (stop[0] - ux * 70, stop[1] - uy * 70)
        pts = [(ox, oy), (ox, oy), stop, back, back]
        times = [0, L, A, A + 0.45, T]
        spl = [LIN, EASE_IN, EASE_OUT, LIN]
        fill = discrete("fill", [0, A], [INDIGO, AMBER], T)
        op_t = [0, L, L + 0.08, A + 0.6, A + 1.0, T]
        op_v = ["0", "0", "1", "1", "0", "0"]
    vals = [f"{p[0]:.1f} {p[1]:.1f}" for p in pts]
    mv = spline_anim(None, times, vals, T, typ="translate", splines=spl)
    op = spline_anim("opacity", op_t, op_v, T)
    packets.append(
        f'<g opacity="0">{mv}{op}<rect x="-10" y="-6" width="20" height="12" rx="3" fill="{INDIGO}">{fill}</rect></g>')

ACQ, REL = 1.5, 3.4
lock_fill = discrete("fill", [0, ACQ, REL], [PANEL, TEAL, PANEL], T)
lock_stroke = discrete("stroke", [0, ACQ, REL], [INDIGO, TEAL, INDIGO], T)
shackle_move = (f'<animateTransform attributeName="transform" type="translate" dur="{T}s" repeatCount="indefinite" '
                f'calcMode="spline" keyTimes="{kt([0, ACQ - 0.05, ACQ + 0.12, REL, REL + 0.2, T], T)}" '
                f'keySplines="{LIN};{EASE};{LIN};{EASE};{LIN}" values="0 -7;0 -7;0 0;0 0;0 -7;0 -7"/>')
shackle_stroke = discrete("stroke", [0, ACQ, REL], [INDIGO, TEAL, INDIGO], T)
lock = (
    f'<circle cx="{LX}" cy="{LY+4}" r="24" fill="none" stroke="{TEAL}" stroke-width="2" opacity="0">'
    f'{spline_anim("r", [0, ACQ, ACQ + 0.6, T], ["24", "24", "62", "62"], T)}'
    f'{spline_anim("opacity", [0, ACQ, ACQ + 0.01, ACQ + 0.6, T], ["0", "0", ".7", "0", "0"], T)}</circle>'
    f'<g><path d="M{LX-10} {LY-4} v-9 a10 10 0 0 1 20 0 v9" fill="none" stroke="{INDIGO}" stroke-width="3.5" stroke-linecap="round">{shackle_stroke}</path>{shackle_move}</g>'
    f'<rect x="{LX-18}" y="{LY-5}" width="36" height="30" rx="6" fill="{PANEL}" stroke="{INDIGO}" stroke-width="2.5">{lock_fill}{lock_stroke}</rect>'
    f'<circle cx="{LX}" cy="{LY+8}" r="3.2" fill="{INDIGO}">{discrete("fill", [0, ACQ, REL], [INDIGO, INK, INDIGO], T)}</circle>'
    f'<rect x="{LX-1.3}" y="{LY+9}" width="2.6" height="7" rx="1" fill="{INDIGO}">{discrete("fill", [0, ACQ, REL], [INDIGO, INK, INDIGO], T)}</rect>'
)

DB_HIT = arrivals[WIN_LANE] + 0.7
db_col = discrete("stroke", [0, DB_HIT, DB_HIT + 1.1], [INDIGO, TEAL, INDIGO], T)
db = (f'<g fill="{PANEL}" stroke="{INDIGO}" stroke-width="2.5">{db_col}'
      f'<path d="M{DBX-16} {LY-16} v32 a16 5.5 0 0 0 32 0 v-32"/>'
      f'<ellipse cx="{DBX}" cy="{LY-16}" rx="16" ry="5.5"/>'
      f'<path d="M{DBX-16} {LY} a16 5.5 0 0 0 32 0" fill="none"/></g>')
db_glow = (f'<ellipse cx="{DBX}" cy="{LY}" rx="16" ry="22" fill="{TEAL}" opacity="0">'
           f'{spline_anim("opacity", [0, DB_HIT, DB_HIT + 0.01, DB_HIT + 1.0, T], ["0", "0", ".35", "0", "0"], T)}</ellipse>')

ok_run, _ = G.run(MONO, "OK", LX - MONO.width("OK", 14) / 2, 262, 14, fill=TEAL)
nil_txt = "(nil) ×4"
nil_run, _ = G.run(MONO, nil_txt, LX - MONO.width(nil_txt, 13) / 2, 284, 13, fill=AMBER)
results = (f'<g opacity="0">{discrete("opacity", [0, ACQ, REL + 0.3], ["0", "1", "0"], T)}{ok_run}</g>'
           f'<g opacity="0">{discrete("opacity", [0, arrivals[4] + 0.1, REL + 0.3], ["0", "1", "0"], T)}{nil_run}</g>')

live = (f'<g class="live">{"".join(live_typing)}{cur}{"".join(packets)}{lock}{db_glow}{db}{results}</g>')

ph0, _ = G.run(MONO, phrases[0], TX, TY, FS, fill=SOFT)
ok2, _ = G.run(MONO, "OK", LX - MONO.width("OK", 14) / 2, 262, 14, fill=TEAL)
nil2, _ = G.run(MONO, nil_txt, LX - MONO.width(nil_txt, 13) / 2, 284, 13, fill=AMBER)
still = (f'<g class="still">{ph0}'
         f'<path d="M{LX-10} {LY-4} v-9 a10 10 0 0 1 20 0 v9" fill="none" stroke="{TEAL}" stroke-width="3.5" stroke-linecap="round"/>'
         f'<rect x="{LX-18}" y="{LY-5}" width="36" height="30" rx="6" fill="{TEAL}" stroke="{TEAL}" stroke-width="2.5"/>'
         f'<circle cx="{LX}" cy="{LY+8}" r="3.2" fill="{INK}"/><rect x="{LX-1.3}" y="{LY+9}" width="2.6" height="7" rx="1" fill="{INK}"/>'
         f'<g fill="{PANEL}" stroke="{TEAL}" stroke-width="2.5"><path d="M{DBX-16} {LY-16} v32 a16 5.5 0 0 0 32 0 v-32"/>'
         f'<ellipse cx="{DBX}" cy="{LY-16}" rx="16" ry="5.5"/><path d="M{DBX-16} {LY} a16 5.5 0 0 0 32 0" fill="none"/></g>'
         f'{ok2}{nil2}</g>')

body += scene_static
body.append(live)
body.append(still)

css = (".blink{animation:b 1.05s steps(1) infinite}@keyframes b{50%{opacity:0}}"
       ".still{display:none}"
       "@media (prefers-reduced-motion:reduce){.live{display:none}.still{display:inline}}")

svg = svg_doc(W, H, "".join(body), G, extra_defs=extra, css=css,
              title="Mazin Shamshad. Five requests race for one seat lock: one gets OK and books the seat, four get nil. Zero double-bookings.")
open(ASSETS + "/hero.svg", "w").write(svg)
print("hero bytes", len(svg))
