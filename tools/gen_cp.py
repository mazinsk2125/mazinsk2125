from svgkit import *
import math

W, H = 1200, 244
G = Glyphs()
T = 10.0
body, live, still = [], [], []
extra = ""


def disc(attr, times, vals):
    return (f'<animate attributeName="{attr}" dur="{T}s" repeatCount="indefinite" calcMode="discrete" '
            f'keyTimes="{kt(times, T)}" values="{";".join(vals)}"/>')


def show_between(a, b):
    return disc("opacity", [0, a, b], ["0", "1", "0"])


body.append(f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="14" fill="{PANEL}" stroke="{LINE}"/>')
for x in (400, 800):
    body.append(f'<line x1="{x}" y1="28" x2="{x}" y2="{H-28}" stroke="{LINE}"/>')

cols = [44, 444, 844]
RESET = T - 0.6


def head(x, platform, rank):
    s1, _ = G.run(MONO, platform, x, 60, 14, fill=MUTED)
    s2, _ = G.run(DISPLAY, rank, x - 2, 132, 64, fill=TEXT, tracking=1)
    body.append(s1 + s2)


x = cols[0]
head(x, "LeetCode", "Knight")
steps = list(range(0, 2001, 100))
t0, dt = 0.4, 0.06
for i, n in enumerate(steps):
    label = f"{n}+" if n == 2000 else f"{n}"
    r, _ = G.run(MONOB, label, x, 190, 30, fill=TEAL)
    a = t0 + i * dt
    b = t0 + (i + 1) * dt if n != 2000 else RESET
    live.append(f'<g opacity="0">{show_between(a, b)}{r}</g>')
r, _ = G.run(MONOB, "2000+", x, 190, 30, fill=TEAL)
still.append(r)
cap = "problems solved"
r, _ = G.run(MONO, cap, x + MONOB.width("2000+", 30) + 12, 190, 14, fill=SOFT)
body.append(r)

x = cols[1]
head(x, "Codeforces", "Specialist")
ranks = [("newbie", "#8C8C8C"), ("pupil", "#3FB950"), ("specialist", "#03A89E"),
         ("expert", "#4C7DFF"), ("cm", "#B35CFF")]
bw, gap = 44, 16
base = 200
for i, (name, col) in enumerate(ranks):
    bx = x + i * (bw + gap)
    h = 18 + i * 9
    y = base - h
    body.append(f'<rect x="{bx}" y="{y}" width="{bw}" height="{h}" rx="4" fill="none" stroke="{LINE2}" stroke-width="1.5"/>')
    lab = name if name != "specialist" else "spec"
    r, _ = G.run(MONO, lab, bx + bw / 2 - MONO.width(lab, 11) / 2, base + 18, 11, fill=MUTED if i != 2 else TEXT)
    body.append(r)
    if i <= 2:
        a = 0.5 + i * 0.35
        live.append(
            f'<rect x="{bx}" y="{base}" width="{bw}" height="0" rx="4" fill="{col}">'
            f'<animate attributeName="height" dur="{T}s" repeatCount="indefinite" keyTimes="{kt([0, a, a + 0.35, RESET, RESET + 0.3, T], T)}" '
            f'values="0;0;{h};{h};0;0" calcMode="spline" keySplines="0 0 1 1;0.2 0.7 0.3 1;0 0 1 1;0.4 0 1 1;0 0 1 1"/>'
            f'<animate attributeName="y" dur="{T}s" repeatCount="indefinite" keyTimes="{kt([0, a, a + 0.35, RESET, RESET + 0.3, T], T)}" '
            f'values="{base};{base};{y};{y};{base};{base}" calcMode="spline" keySplines="0 0 1 1;0.2 0.7 0.3 1;0 0 1 1;0.4 0 1 1;0 0 1 1"/></rect>')
        still.append(f'<rect x="{bx}" y="{y}" width="{bw}" height="{h}" rx="4" fill="{col}"/>')
        if i == 2:
            ap = a + 0.4
            kts = kt([0, ap, ap + 0.9, T], T)
            def grow(attr, v0, v1):
                return (f'<animate attributeName="{attr}" dur="{T}s" repeatCount="indefinite" '
                        f'keyTimes="{kts}" values="{v0};{v0};{v1};{v1}"/>')
            live.append(
                f'<rect x="{bx}" y="{y}" width="{bw}" height="{h}" rx="5" fill="none" stroke="{col}" stroke-width="2" opacity="0">'
                f'<animate attributeName="opacity" dur="{T}s" repeatCount="indefinite" keyTimes="{kt([0, ap, ap + 0.01, ap + 0.9, T], T)}" values="0;0;.9;0;0"/>'
                + grow("x", bx, bx - 8) + grow("y", y, y - 8) + grow("width", bw, bw + 16) + grow("height", h, h + 16)
                + '</rect>')

x = cols[2]
head(x, "CodeChef", "4 star")


def star(cx, cy, R, r=None):
    r = r or R * 0.45
    pts = []
    for k in range(10):
        ang = -math.pi / 2 + k * math.pi / 5
        rad = R if k % 2 == 0 else r
        pts.append(f"{cx + rad*math.cos(ang):.1f},{cy + rad*math.sin(ang):.1f}")
    return " ".join(pts)


for i in range(7):
    cx = x + 17 + i * 44
    cy = 180
    pts = star(cx, cy, 17)
    body.append(f'<polygon points="{pts}" fill="none" stroke="{LINE2}" stroke-width="1.5" stroke-linejoin="round"/>')
    if i < 4:
        a = 0.6 + i * 0.28
        live.append(
            f'<polygon points="{pts}" fill="{INDIGO}" stroke="{INDIGO}" stroke-width="1.5" stroke-linejoin="round" opacity="0">'
            f'<animate attributeName="opacity" dur="{T}s" repeatCount="indefinite" keyTimes="{kt([0, a, a + 0.25, RESET, RESET + 0.3, T], T)}" values="0;0;1;1;0;0"/></polygon>')
        still.append(f'<polygon points="{pts}" fill="{INDIGO}" stroke="{INDIGO}" stroke-width="1.5" stroke-linejoin="round"/>')

cap = "4 of 7 stars"
r, _ = G.run(MONO, cap, x, 226, 12, fill=MUTED)
body.append(r)

body.append(f'<g class="live">{"".join(live)}</g><g class="still">{"".join(still)}</g>')
css = ".still{display:none}@media (prefers-reduced-motion:reduce){.live{display:none}.still{display:inline}}"
svg = svg_doc(W, H, "".join(body), G, extra_defs=extra, css=css,
              title="Competitive programming: LeetCode Knight with 2000+ problems solved, Codeforces Specialist, CodeChef 4 star.")
open(ASSETS + "/cp.svg", "w").write(svg)
print("cp bytes", len(svg))
