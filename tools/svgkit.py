from fontTools.ttLib import TTFont
from fontTools.varLib import instancer
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.normpath(os.path.join(HERE, "..", "assets"))


def _load(path, wght=None):
    f = TTFont(os.path.join(HERE, path))
    if wght is not None:
        f = instancer.instantiateVariableFont(f, {"wght": wght})
    return f


class Font:
    def __init__(self, key, path, wght=None):
        self.key = key
        self.f = _load(path, wght)
        self.upm = self.f["head"].unitsPerEm
        self.cmap = self.f.getBestCmap()
        self.gs = self.f.getGlyphSet()
        self.hmtx = self.f["hmtx"]

    def advance(self, ch, size):
        g = self.cmap.get(ord(ch))
        if g is None:
            g = self.cmap[ord("?")]
        return self.hmtx[g][0] * size / self.upm

    def width(self, text, size, tracking=0.0):
        return sum(self.advance(c, size) + tracking for c in text) - (tracking if text else 0)

    def glyph_d(self, ch, size):
        g = self.cmap.get(ord(ch))
        if g is None:
            return ""
        s = size / self.upm
        pen = SVGPathPen(self.gs, ntos=lambda v: f"{v:.1f}".rstrip("0").rstrip("."))
        tp = TransformPen(pen, (s, 0, 0, -s, 0, 0))
        self.gs[g].draw(tp)
        return pen.getCommands()


class Glyphs:

    def __init__(self):
        self.defs = {}

    def _id(self, font, size, ch):
        return f"{font.key}{int(size*10)}_{ord(ch):x}"

    def run(self, font, text, x, y, size, fill=None, tracking=0.0, cls=None, opacity=None):
        parts = []
        edges = []
        cx = x
        for ch in text:
            adv = font.advance(ch, size)
            if ch != " ":
                gid = self._id(font, size, ch)
                if gid not in self.defs:
                    d = font.glyph_d(ch, size)
                    self.defs[gid] = f'<path id="{gid}" d="{d}"/>'
                parts.append(f'<use href="#{gid}" x="{cx:.1f}" y="{y:.1f}"/>')
            cx += adv + tracking
            edges.append(cx)
        attrs = []
        if fill:
            attrs.append(f'fill="{fill}"')
        if cls:
            attrs.append(f'class="{cls}"')
        if opacity is not None:
            attrs.append(f'opacity="{opacity}"')
        return f'<g {" ".join(attrs)}>' + "".join(parts) + "</g>", edges

    def defs_svg(self):
        return "".join(self.defs.values())


MONO = Font("m", "fonts/JBM-Regular.ttf")
MONOB = Font("mb", "fonts/JBM-Bold.ttf")
DISPLAY = Font("d", "fonts/BSD.ttf", wght=900)
DISPLAY_MED = Font("dm", "fonts/BSD.ttf", wght=600)

INK = "#0B1020"
PANEL = "#0E1328"
LINE = "#1E2547"
LINE2 = "#2A3160"
INDIGO = "#7C83FF"
INDIGO_DEEP = "#4A51B8"
TEAL = "#2EE6C5"
AMBER = "#FFB547"
TEXT = "#E9EBFF"
MUTED = "#8A90B8"
SOFT = "#A7ACD0"


def svg_doc(w, h, body, glyphs, extra_defs="", css="", title=""):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img">'
        + (f"<title>{title}</title>" if title else "")
        + f"<defs>{glyphs.defs_svg()}{extra_defs}</defs>"
        + (f"<style>{css}</style>" if css else "")
        + body
        + "</svg>"
    )


def kt(times, T):
    return ";".join(f"{min(max(t / T, 0), 1):.4f}".rstrip("0").rstrip(".") if t else "0" for t in times)


def typing_anim(edges, x0, t_start, per_char, T, t_delete=None, del_per_char=None, t_hide=None):
    times, vals = [0.0], [0.0]
    if t_start > 0:
        times.append(t_start)
        vals.append(0.0)
    for i, e in enumerate(edges):
        t = t_start + (i + 1) * per_char
        times.append(t)
        vals.append(e - x0 + 2)
    if t_delete is not None:
        n = len(edges)
        for i in range(n):
            t = t_delete + (i + 1) * del_per_char
            times.append(t)
            w = (edges[n - 2 - i] - x0 + 2) if n - 2 - i >= 0 else 0.0
            vals.append(w)
    elif t_hide is not None:
        times.append(t_hide)
        vals.append(0.0)
    out_t, out_v = [], []
    for t, v in zip(times, vals):
        if out_t and t <= out_t[-1]:
            t = out_t[-1] + 0.001
        out_t.append(t)
        out_v.append(v)
    return (
        f'<animate attributeName="width" dur="{T}s" repeatCount="indefinite" calcMode="discrete" '
        f'keyTimes="{kt(out_t, T)}" values="{";".join(f"{v:.1f}" for v in out_v)}"/>'
    ), out_t, out_v
