from svgkit import *

W, H = 1200, 456
G = Glyphs()
T = 17.0
FS = 17
LH = 30
X = 44
Y0 = 92

lines = [
    ("cmd", "whoami"),
    ("out", [("Mazin Shamshad, assistant system engineer at TCS", SOFT)]),
    ("out", [("B.Tech ECE, Jamia Millia Islamia", SOFT)]),
    ("cmd", "cat focus.txt"),
    ("out", [("Backends that stay correct under concurrency: locks, queues, idempotency.", SOFT)]),
    ("cmd", "tail -3 now.log"),
    ("out", [("[work]  ", INDIGO), ("multi-tenant security posture dashboard, React + Node + PostgreSQL", SOFT)]),
    ("out", [("[study] ", INDIGO), ("low-level design in Java, machine coding", SOFT)]),
    ("out", [("[build] ", INDIGO), ("ScaleSeats → DocQuery → CogniBase", SOFT)]),
    ("cmd", "echo $GOAT"),
    ("out", [("Cristiano Ronaldo. Not taking questions.", TEXT)]),
    ("cmd", None),
]

extra = f'<clipPath id="win"><rect width="{W}" height="{H}" rx="14"/></clipPath>'
body = []
body.append(f'<g clip-path="url(#win)"><rect width="{W}" height="{H}" fill="{PANEL}"/>'
            f'<rect width="{W}" height="44" fill="#11173A"/><line x1="0" y1="44.5" x2="{W}" y2="44.5" stroke="{LINE}"/></g>')
body.append(f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="14" fill="none" stroke="{LINE}"/>')
for i, c in enumerate([LINE2, LINE2, LINE2]):
    body.append(f'<circle cx="{26 + i*20}" cy="22" r="6" fill="{c}"/>')
tt = "mazin@github: ~"
s, _ = G.run(MONO, tt, W / 2 - MONO.width(tt, 13) / 2, 27, 13, fill=MUTED)
body.append(s)

PROMPT = "~ $ "
pw = MONO.width(PROMPT, FS)
t = 0.7
live = []
cur_t, cur_x, cur_y = [0.0], [X + pw], [Y0]
k = 0
for idx, (kind, content) in enumerate(lines):
    y = Y0 + idx * LH
    if kind == "cmd":
        pr, _ = G.run(MONO, PROMPT, X, y, FS, fill=TEAL)
        live.append(f'<g opacity="0"><animate attributeName="opacity" dur="{T}s" repeatCount="indefinite" calcMode="discrete" keyTimes="0;{t/T:.4f}" values="0;1"/>{pr}</g>')
        cur_t.append(t); cur_x.append(X + pw); cur_y.append(y)
        if content is None:
            break
        t += 0.45
        run, edges = G.run(MONO, content, X + pw, y, FS, fill=TEXT)
        anim, ts, vs = typing_anim(edges, X + pw, t, 0.055, T)
        cid = f"c{k}"; k += 1
        extra += f'<clipPath id="{cid}"><rect x="{X+pw}" y="{y-20}" width="0" height="28">{anim}</rect></clipPath>'
        live.append(f'<g class="clip" clip-path="url(#{cid})">{run}</g>')
        for tt_, v in zip(ts[1:], vs[1:]):
            cur_t.append(tt_); cur_x.append(X + pw + v); cur_y.append(y)
        t = ts[-1] + 0.35
    else:
        cx = X
        parts = []
        for text, col in content:
            r, e = G.run(MONO, text, cx, y, FS, fill=col)
            parts.append(r)
            cx = e[-1]
        live.append(f'<g opacity="0"><animate attributeName="opacity" dur="{T}s" repeatCount="indefinite" calcMode="discrete" keyTimes="0;{t/T:.4f}" values="0;1"/>{"".join(parts)}</g>')
        t += 0.13
        if idx + 1 < len(lines) and lines[idx + 1][0] == "cmd":
            t += 0.55
end_t = t
ct, cx_, cy_ = [], [], []
for a, b, c in zip(cur_t, cur_x, cur_y):
    if ct and a <= ct[-1]:
        a = ct[-1] + 0.001
    ct.append(a); cx_.append(b); cy_.append(c)
cursor = (f'<rect class="blink" x="{X+pw}" y="{Y0-15}" width="10" height="19" rx="1.5" fill="{TEAL}">'
          f'<animate attributeName="x" dur="{T}s" repeatCount="indefinite" calcMode="discrete" keyTimes="{kt(ct, T)}" values="{";".join(f"{v+1:.1f}" for v in cx_)}"/>'
          f'<animate attributeName="y" dur="{T}s" repeatCount="indefinite" calcMode="discrete" keyTimes="{kt(ct, T)}" values="{";".join(f"{v-15:.1f}" for v in cy_)}"/></rect>')

fade = (f'<animate attributeName="opacity" dur="{T}s" repeatCount="indefinite" '
        f'keyTimes="0;{(T-0.9)/T:.4f};{(T-0.3)/T:.4f};1" values="1;1;0;0"/>')
body.append(f'<g class="live">{fade}{"".join(live)}{cursor}</g>')

still = []
for idx, (kind, content) in enumerate(lines):
    y = Y0 + idx * LH
    if kind == "cmd":
        r, _ = G.run(MONO, PROMPT, X, y, FS, fill=TEAL); still.append(r)
        if content:
            r, _ = G.run(MONO, content, X + pw, y, FS, fill=TEXT); still.append(r)
    else:
        cx = X
        for text, col in content:
            r, e = G.run(MONO, text, cx, y, FS, fill=col); still.append(r); cx = e[-1]
still.append(f'<rect x="{X+pw+1}" y="{Y0 + (len(lines)-1)*LH - 15}" width="10" height="19" rx="1.5" fill="{TEAL}"/>')
body.append(f'<g class="still">{"".join(still)}</g>')

css = (".blink{animation:b 1.05s steps(1) infinite}@keyframes b{50%{opacity:0}}"
       ".still{display:none}@media (prefers-reduced-motion:reduce){.live{display:none}.still{display:inline}}")
svg = svg_doc(W, H, "".join(body), G, extra_defs=extra, css=css,
              title="Terminal: whoami — Mazin Shamshad, assistant system engineer at TCS. Focus: backends that stay correct under concurrency.")
open(ASSETS + "/terminal.svg", "w").write(svg)
print("terminal bytes", len(svg), "sequence ends", round(end_t, 2))
