from svgkit import *
import math, random

W, H = 590, 236
CSS = ".still{display:none}@media (prefers-reduced-motion:reduce){.live{display:none}.still{display:inline}}"


def disc(attr, times, vals, T):
    return (f'<animate attributeName="{attr}" dur="{T}s" repeatCount="indefinite" calcMode="discrete" '
            f'keyTimes="{kt(times, T)}" values="{";".join(vals)}"/>')


def lin(attr, times, vals, T):
    return (f'<animate attributeName="{attr}" dur="{T}s" repeatCount="indefinite" '
            f'keyTimes="{kt(times, T)}" values="{";".join(str(v) for v in vals)}"/>')


def card(G, name, desc, chips, pill=None):
    out = [f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="14" fill="{PANEL}" stroke="{LINE}"/>']
    s, e = G.run(DISPLAY, name, 32, 80, 46, fill=TEXT, tracking=0.5)
    out.append(s)
    if pill:
        px = e[-1] + 14
        pw = MONO.width(pill, 12) + 18
        out.append(f'<rect x="{px}" y="52" width="{pw}" height="24" rx="12" fill="none" stroke="{AMBER}" stroke-opacity=".6"/>')
        s, _ = G.run(MONO, pill, px + 9, 68, 12, fill=AMBER)
        out.append(s)
    for i, line in enumerate(desc):
        s, _ = G.run(MONO, line, 32, 120 + i * 22, 14, fill=SOFT)
        out.append(s)
    cx = 32
    for c in chips:
        cw = MONO.width(c, 12) + 20
        out.append(f'<rect x="{cx}" y="176" width="{cw}" height="26" rx="6" fill="none" stroke="{LINE2}" stroke-width="1.2"/>')
        s, _ = G.run(MONO, c, cx + 10, 193.5, 12, fill=SOFT)
        out.append(s)
        cx += cw + 8
    assert cx < 390, (name, cx)
    return "".join(out)


def write(fname, G, body, title):
    svg = svg_doc(W, H, body, G, css=CSS, title=title)
    open(f"{ASSETS}/projects/{fname}.svg", "w").write(svg)
    print(fname, len(svg))


def scaleseats():
    G = Glyphs(); T = 8.0
    b = [card(G, "ScaleSeats", ["Seat booking that survives a stampede.", "One seat, one booking, every time."],
              ["Redis locks", "BullMQ", "idempotency", "k6"])]
    cols, rows, sw, sh, gx, gy = 6, 4, 18, 16, 9, 12
    x0 = 420; y0 = 62
    rnd = random.Random(7)
    order = [(r, c) for r in range(rows) for c in range(cols)]
    target = (0, 3)
    order.remove(target)
    rnd.shuffle(order)
    live, still = [], []
    for r in range(rows):
        s, _ = G.run(MONO, "ABCD"[r], x0 - 18, y0 + r * (sh + gy) + 12, 11, fill=MUTED)
        b.append(s)
    for c in range(cols):
        lab = str(11 + c)
        s, _ = G.run(MONO, lab, x0 + c * (sw + gx) + sw / 2 - MONO.width(lab, 10) / 2, y0 + rows * (sh + gy) + 6, 10, fill=MUTED)
        b.append(s)
    RESET = T - 0.7
    for r in range(rows):
        for c in range(cols):
            x = x0 + c * (sw + gx); y = y0 + r * (sh + gy)
            b.append(f'<rect x="{x}" y="{y}" width="{sw}" height="{sh}" rx="4" fill="none" stroke="{LINE2}" stroke-width="1.4"/>')
            if (r, c) == target:
                ts = [0, 1.3, 1.5, 1.8, 2.0, 2.4, RESET]
                vs = ["0", "1", "0", "1", "0", "1", "0"]
                fills = disc("fill", [0, 1.3, 2.4], [AMBER, AMBER, TEAL], T)
                live.append(f'<rect x="{x}" y="{y}" width="{sw}" height="{sh}" rx="4" fill="{AMBER}" opacity="0">{fills}{disc("opacity", ts, vs, T)}</rect>')
                still.append(f'<rect x="{x}" y="{y}" width="{sw}" height="{sh}" rx="4" fill="{TEAL}"/>')
            else:
                idx = order.index((r, c))
                if idx < 17:
                    a = 0.4 + idx * 0.26
                    live.append(f'<rect x="{x}" y="{y}" width="{sw}" height="{sh}" rx="4" fill="{INDIGO_DEEP}" opacity="0">'
                                f'{lin("opacity", [0, a, a + 0.18, RESET, RESET + 0.3, T], [0, 0, 1, 1, 0, 0], T)}</rect>')
                    still.append(f'<rect x="{x}" y="{y}" width="{sw}" height="{sh}" rx="4" fill="{INDIGO_DEEP}"/>')
    s, _ = G.run(MONO, "14A", x0 + 3 * (sw + gx) - 2, y0 - 10, 10, fill=TEAL)
    live.append(f'<g opacity="0">{disc("opacity", [0, 2.4, RESET], ["0", "1", "0"], T)}{s}</g>')
    b.append(f'<g class="live">{"".join(live)}</g><g class="still">{"".join(still)}</g>')
    write("scaleseats", G, "".join(b), "ScaleSeats: seat booking that survives a stampede. Redis locks, BullMQ, idempotency keys, k6 load tests.")


def docquery():
    G = Glyphs(); T = 7.0
    b = [card(G, "DocQuery", ["Ask questions of your documents and", "get answers grounded in what's there."],
              ["RAG", "pgvector"])]
    rnd = random.Random(11)
    pts = []
    while len(pts) < 30:
        p = (rnd.uniform(418, 562), rnd.uniform(48, 196))
        if not (455 < p[0] < 525 and 128 < p[1] < 150) and all(math.hypot(p[0] - q[0], p[1] - q[1]) > 17 for q in pts):
            pts.append(p)
    q = (488, 118)
    nn = sorted(pts, key=lambda p: math.hypot(p[0] - q[0], p[1] - q[1]))[:3]
    RESET = T - 0.7
    live, still = [], []
    for p in pts:
        b.append(f'<circle cx="{p[0]:.1f}" cy="{p[1]:.1f}" r="3.2" fill="{INDIGO_DEEP}"/>')
    for i, p in enumerate(nn):
        L = math.hypot(p[0] - q[0], p[1] - q[1])
        a = 1.3 + i * 0.18
        live.append(f'<line x1="{q[0]}" y1="{q[1]}" x2="{p[0]:.1f}" y2="{p[1]:.1f}" stroke="{TEAL}" stroke-width="1.5" '
                    f'stroke-dasharray="{L:.1f}" stroke-dashoffset="{L:.1f}">'
                    f'{lin("stroke-dashoffset", [0, a, a + 0.35, RESET, RESET + 0.3, T], [f"{L:.1f}", f"{L:.1f}", 0, 0, f"{L:.1f}", f"{L:.1f}"], T)}</line>')
        live.append(f'<circle cx="{p[0]:.1f}" cy="{p[1]:.1f}" r="4.5" fill="{TEAL}" opacity="0">'
                    f'{lin("opacity", [0, a + 0.3, a + 0.45, RESET, RESET + 0.3, T], [0, 0, 1, 1, 0, 0], T)}</circle>')
        still.append(f'<line x1="{q[0]}" y1="{q[1]}" x2="{p[0]:.1f}" y2="{p[1]:.1f}" stroke="{TEAL}" stroke-width="1.5"/>'
                     f'<circle cx="{p[0]:.1f}" cy="{p[1]:.1f}" r="4.5" fill="{TEAL}"/>')
    live.append(f'<circle cx="{q[0]}" cy="{q[1]}" r="6" fill="none" stroke="{TEAL}" stroke-width="1.5" opacity="0">'
                f'{lin("r", [0, 0.8, 1.4, T], [6, 6, 26, 26], T)}{lin("opacity", [0, 0.8, 0.81, 1.4, T], [0, 0, 0.8, 0, 0], T)}</circle>')
    live.append(f'<circle cx="{q[0]}" cy="{q[1]}" r="6" fill="{TEAL}" opacity="0">'
                f'{lin("opacity", [0, 0.8, 0.95, RESET, RESET + 0.3, T], [0, 0, 1, 1, 0, 0], T)}</circle>')
    still.append(f'<circle cx="{q[0]}" cy="{q[1]}" r="6" fill="{TEAL}"/>')
    s, _ = G.run(MONO, "query", q[0] - 16, q[1] + 22, 10, fill=TEAL)
    live.append(f'<g opacity="0">{lin("opacity", [0, 0.9, 1.1, RESET, RESET + 0.3, T], [0, 0, 1, 1, 0, 0], T)}{s}</g>')
    still.append(s)
    b.append(f'<g class="live">{"".join(live)}</g><g class="still">{"".join(still)}</g>')
    write("docquery", G, "".join(b), "DocQuery: ask questions of your documents, answers grounded in them. RAG over pgvector.")


def cognibase():
    G = Glyphs(); T = 8.0
    b = [card(G, "CogniBase", ["Real-time collaboration where every", "client converges on the same state."],
              ["Socket.IO", "real-time sync"])]
    panes = [(404, 50), (494, 50)]
    pw_, ph = 72, 136
    base_w = [52, 40, 56, 30, 46]
    live, still = [], []
    for px, py in panes:
        b.append(f'<rect x="{px}" y="{py}" width="{pw_}" height="{ph}" rx="8" fill="{INK}" stroke="{LINE2}" stroke-width="1.4"/>')
        for i, w in enumerate(base_w):
            if i in (2, 4):
                continue
            b.append(f'<rect x="{px+10}" y="{py+16+i*22}" width="{w}" height="7" rx="3.5" fill="{LINE2}"/>')
    RESET = T - 0.7
    edits = [(0, 2, INDIGO, 0.6, 1), (1, 4, TEAL, 3.0, 0)]
    for src, line, col, t0, dst in edits:
        w = base_w[line]
        for pane_i, delay in ((src, 0.0), (dst, 1.0)):
            px, py = panes[pane_i]
            y = py + 16 + line * 22
            a = t0 + delay
            live.append(f'<rect x="{px+10}" y="{y}" width="0" height="7" rx="3.5" fill="{col}">'
                        f'{lin("width", [0, a, a + 0.6, RESET, RESET + 0.3, T], [0, 0, w, w, 0, 0], T)}</rect>')
            still.append(f'<rect x="{px+10}" y="{y}" width="{w}" height="7" rx="3.5" fill="{col}"/>')
            if delay == 0:
                live.append(f'<rect x="{px+10}" y="{y-4}" width="2" height="15" fill="{col}" opacity="0">'
                            f'{lin("x", [0, a, a + 0.6, T], [px + 10, px + 10, px + 12 + w, px + 12 + w], T)}'
                            f'{disc("opacity", [0, a, a + 0.9], ["0", "1", "0"], T)}</rect>')
        sx = panes[src][0] + (pw_ if src == 0 else 0)
        dx = panes[dst][0] + (pw_ if dst == 0 else 0)
        yy = panes[src][1] + 16 + line * 22 + 3.5
        a = t0 + 0.65
        live.append(f'<circle cx="{sx}" cy="{yy}" r="3.5" fill="{col}" opacity="0">'
                    f'{lin("cx", [0, a, a + 0.35, T], [sx, sx, dx, dx], T)}'
                    f'{lin("opacity", [0, a, a + 0.05, a + 0.3, a + 0.36, T], [0, 0, 1, 1, 0, 0], T)}</circle>')
    for i, (px, py) in enumerate(panes):
        lab = f"client {'ab'[i]}"
        s, _ = G.run(MONO, lab, px + pw_ / 2 - MONO.width(lab, 10) / 2, py + ph + 18, 10, fill=MUTED)
        b.append(s)
    b.append(f'<g class="live">{"".join(live)}</g><g class="still">{"".join(still)}</g>')
    write("cognibase", G, "".join(b), "CogniBase: real-time collaboration where every client converges on the same state. Socket.IO.")


def inference():
    G = Glyphs(); T = 2.8
    b = [card(G, "Inference", ["An LLM inference server with an eval", "harness to prove it's fast and right."],
              ["LLM serving", "evals"], pill="planned")]
    bx, by, bw, bh = 402, 78, 54, 80
    b.append(f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="10" fill="{INK}" stroke="{INDIGO}" stroke-width="1.6"/>')
    for i in range(4):
        for j in range(3):
            b.append(f'<circle cx="{bx+14+j*13}" cy="{by+18+i*15}" r="2.2" fill="{INDIGO_DEEP}"/>')
    lane_y = by + bh / 2
    b.append(f'<line x1="{bx+bw}" y1="{lane_y}" x2="566" y2="{lane_y}" stroke="{LINE2}" stroke-dasharray="2 6" stroke-linecap="round"/>')
    widths = [14, 22, 12, 18]
    live, still = [], []
    n = len(widths)
    for k, w in enumerate(widths):
        start = bx + bw + 4
        end = 566 - w
        begin = -k * T / n
        col = TEAL if k % 3 == 0 else INDIGO
        live.append(
            f'<rect x="{start}" y="{lane_y-6}" width="{w}" height="12" rx="4" fill="{col}">'
            f'<animate attributeName="x" dur="{T}s" begin="{begin:.2f}s" repeatCount="indefinite" values="{start};{end}"/>'
            f'<animate attributeName="opacity" dur="{T}s" begin="{begin:.2f}s" repeatCount="indefinite" keyTimes="0;.12;.8;1" values="0;1;1;0"/></rect>')
    xs = bx + bw + 10
    for w in widths[:3]:
        still.append(f'<rect x="{xs}" y="{lane_y-6}" width="{w}" height="12" rx="4" fill="{INDIGO}"/>')
        xs += w + 8
    for i in range(5):
        x = 480 + i * 16
        hs = [10, 22, 16, 28, 12, 24]
        rnd = hs[i:] + hs[:i]
        vals = ";".join(str(h) for h in rnd + [rnd[0]])
        yvals = ";".join(str(196 - h) for h in rnd + [rnd[0]])
        live.append(f'<rect x="{x}" y="{196-rnd[0]}" width="10" height="{rnd[0]}" rx="2" fill="{INDIGO_DEEP}">'
                    f'<animate attributeName="height" dur="{T*2}s" repeatCount="indefinite" values="{vals}"/>'
                    f'<animate attributeName="y" dur="{T*2}s" repeatCount="indefinite" values="{yvals}"/></rect>')
        still.append(f'<rect x="{x}" y="{196-rnd[0]}" width="10" height="{rnd[0]}" rx="2" fill="{INDIGO_DEEP}"/>')
    s, _ = G.run(MONO, "tok/s", 408, 194, 10, fill=MUTED)
    b.append(s)
    b.append(f'<g class="live">{"".join(live)}</g><g class="still">{"".join(still)}</g>')
    write("inference", G, "".join(b), "Inference engine (planned): an LLM inference server with an eval harness.")


scaleseats(); docquery(); cognibase(); inference()
