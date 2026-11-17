#!/usr/bin/env python3
"""
Tartarus AI — GitHub brand asset generator.

Single source of truth for every SVG shown on the org profile and the repo
READMEs. Reuses the real production mark + wordmark geometry (src/*.svg),
recolours the accent to the live-site lime, and composes consistent banners,
a hero, an ecosystem diagram and feature cards.

Run:  python make-assets.py
Output is written next to the repos (../../<repo>/assets) and into
../profile/assets. Pure stdlib, no dependencies. Deterministic.
"""
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ORG_ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))   # tartarus-org/
PROFILE_ASSETS = os.path.join(HERE, "..", "profile", "assets")

# --- palette (lime accent + neutral darks) --------------------------------
BG0   = "#0B0D12"   # primary background
BG1   = "#151820"   # secondary surface
BG2   = "#1C2029"   # elevated surface
LINE  = "#2A2F3A"   # hairline border
LINE2 = "#363C47"   # brighter border
TXT   = "#F5F6F8"   # main text
MUT   = "#A5AAB5"   # secondary text
DIM   = "#6B7280"   # faint text
LIME  = "#A3E635"   # primary accent (matches live badges)
LIME2 = "#BEF264"   # light accent
LIME3 = "#84CC16"   # deep accent
LIMED = "#4D7C0F"   # deepest accent

SANS = "'Inter','Segoe UI',system-ui,-apple-system,Helvetica,Arial,sans-serif"
MONO = "'JetBrains Mono','SFMono-Regular',ui-monospace,Consolas,'Liberation Mono',monospace"


# --- reuse the real brand geometry ----------------------------------------
def load_art(name):
    """Return (inner_svg, vbW, vbH) for a source logo, relimed + de-classed."""
    with open(os.path.join(HERE, "src", name), "r", encoding="utf-8") as f:
        raw = f.read()
    m = re.search(r'viewBox="([\d.\s]+)"', raw)
    _, _, vbw, vbh = m.group(1).split()
    # drop xml decl, <defs>…</defs>, and the outer <svg>…</svg> shell
    body = re.sub(r'<\?xml.*?\?>', '', raw, flags=re.S)
    body = re.sub(r'<defs>.*?</defs>', '', body, flags=re.S)
    body = re.sub(r'<svg[^>]*>', '', body, count=1, flags=re.S)
    body = body.rsplit('</svg>', 1)[0]
    # classes -> presentation attributes (cls-1 white, cls-2 accent)
    body = body.replace('class="cls-1"', f'fill="{TXT}"')
    body = body.replace('class="cls-2"', f'fill="{LIME}"')
    return body.strip(), float(vbw), float(vbh)


MARK, MARK_W, MARK_H = load_art("logo-src.svg")
WORD, WORD_W, WORD_H = load_art("wordmark-src.svg")


def place(inner, vbw, vbh, x, y, h, fill=None):
    """Scale a loaded art block to height h and translate to (x,y)."""
    s = h / vbh
    recolor = f' fill="{fill}"' if fill else ''
    return (f'<g transform="translate({x:.2f},{y:.2f}) scale({s:.5f})"'
            f'{recolor}>{inner}</g>')


# --- shared primitives ----------------------------------------------------
def head(w, h, rid):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
            f'viewBox="0 0 {w} {h}" role="img" font-family="{SANS}">')


def defs_bg(w, h, rid):
    """Background: base fill, lime radial glow top-right, dot grid, border."""
    return f'''<defs>
  <radialGradient id="g{rid}" cx="82%" cy="12%" r="60%">
    <stop offset="0%" stop-color="{LIME}" stop-opacity="0.16"/>
    <stop offset="45%" stop-color="{LIME3}" stop-opacity="0.05"/>
    <stop offset="100%" stop-color="{LIME}" stop-opacity="0"/>
  </radialGradient>
  <linearGradient id="bar{rid}" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0%" stop-color="{LIMED}"/>
    <stop offset="50%" stop-color="{LIME}"/>
    <stop offset="100%" stop-color="{LIME2}"/>
  </linearGradient>
  <pattern id="dot{rid}" width="26" height="26" patternUnits="userSpaceOnUse">
    <circle cx="1.2" cy="1.2" r="1.2" fill="{TXT}" opacity="0.045"/>
  </pattern>
</defs>
<rect width="{w}" height="{h}" fill="{BG0}"/>
<rect width="{w}" height="{h}" fill="url(#dot{rid})"/>
<rect width="{w}" height="{h}" fill="url(#g{rid})"/>'''


def bottom_bar(w, h, rid, t=6):
    return f'<rect x="0" y="{h-t}" width="{w}" height="{t}" fill="url(#bar{rid})"/>'


def frame(w, h):
    return (f'<rect x="0.5" y="0.5" width="{w-1}" height="{h-1}" fill="none" '
            f'stroke="{LINE}" stroke-width="1"/>')


def text(x, y, s, size, fill=TXT, weight="400", anchor="start",
         family=SANS, spacing=None, opacity=None):
    extra = ''
    if spacing is not None:
        extra += f' letter-spacing="{spacing}"'
    if opacity is not None:
        extra += f' opacity="{opacity}"'
    s = (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))
    return (f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" '
            f'font-weight="{weight}" fill="{fill}" text-anchor="{anchor}"'
            f'{extra}>{s}</text>')


def chip(x, y, w, h, label, fill=LIME, txt=BG0, size=13):
    r = h / 2
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}"/>'
            + text(x + w/2, y + h/2 + size*0.35, label, size, txt, "700",
                   "middle", SANS, spacing="1.5"))


def ochip(x, y, w, h, label, stroke=LINE2, txt=TXT, size=13):
    """Outlined chip."""
    r = h / 2
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="none" '
            f'stroke="{stroke}" stroke-width="1.3"/>'
            + text(x + w/2, y + h/2 + size*0.35, label, size, txt, "600",
                   "middle", SANS, spacing="0.5"))


def terminal(x, y, w, h, lines, title="tartarus"):
    """A dark terminal card. lines = list of (text, kind)."""
    rid = f'{x}{y}'
    out = [f'<g>',
           f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{BG1}" '
           f'stroke="{LINE2}" stroke-width="1"/>',
           f'<rect x="{x}" y="{y}" width="{w}" height="38" rx="12" fill="{BG2}"/>',
           f'<rect x="{x}" y="{y+26}" width="{w}" height="12" fill="{BG2}"/>']
    for i, cx in enumerate((18, 38, 58)):
        col = ["#FF5F56", "#FFBD2E", LIME][i]
        out.append(f'<circle cx="{x+cx}" cy="{y+19}" r="6" fill="{col}"/>')
    out.append(text(x + w/2, y + 24, title, 13, MUT, "500", "middle", MONO))
    ly = y + 68
    for txt_line, kind in lines:
        if kind == "cmd":
            out.append(text(x+20, ly, "$ ", 15.5, LIME, "700", "start", MONO))
            out.append(text(x+36, ly, txt_line, 15.5, TXT, "500", "start", MONO))
        elif kind == "ok":
            out.append(text(x+20, ly, "✓ " + txt_line, 15, LIME, "600",
                            "start", MONO))
        elif kind == "run":
            out.append(text(x+20, ly, "● " + txt_line, 15, LIME2, "500",
                            "start", MONO))
        else:
            out.append(text(x+20, ly, txt_line, 15, MUT, "400", "start", MONO))
        ly += 30
    out.append('</g>')
    return "".join(out)


def write(path, body):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(body)
    print("  wrote", os.path.relpath(path, ORG_ROOT), f"({len(body)} B)")


# --- assets ---------------------------------------------------------------
def gen_mark():
    pad = 20
    w = MARK_W + pad*2
    h = MARK_H + pad*2
    for variant, mfill in (("dark", None), ("light", BG0)):
        s = head(w, h, "m")
        s += place(MARK, MARK_W, MARK_H, pad, pad, MARK_H, fill=mfill)
        # keep the two accent dots lime even on the light variant: redraw mark
        # already carries lime dots; for light we recolor whole mark then the
        # dot paths get overridden by their own fill attr, so dots stay lime.
        s += '</svg>'
        write(os.path.join(HERE, "..", "profile", "assets",
                           f"tartarus-mark-{variant}.svg"), s)


def gen_wordmark():
    pad = 24
    h = 120
    scale = h / WORD_H
    w = WORD_W * scale + pad*2
    s = head(round(w), h + pad*2, "w")
    s += place(WORD, WORD_W, WORD_H, pad, pad, h)
    s += '</svg>'
    write(os.path.join(HERE, "..", "profile", "assets", "tartarus-wordmark.svg"), s)


def gen_hero():
    w, h = 1600, 500
    s = head(w, h, "h")
    s += defs_bg(w, h, "h")
    # wordmark, upper-left
    s += place(WORD, WORD_W, WORD_H, 70, 70, 92)
    # headline + sub
    s += text(72, 250, "The uncensored AI coding agent.", 54, TXT, "800")
    s += text(74, 300, "Ships the code other assistants refuse, straight from your",
              23, MUT, "400")
    s += text(74, 332, "terminal, an OpenAI-compatible API, or your editor.",
              23, MUT, "400")
    # quick chips
    s += ochip(74, 372, 150, 40, "pip install", LINE2, TXT, 15)
    s += ochip(236, 372, 196, 40, "OpenAI-compatible", LINE2, TXT, 15)
    s += ochip(444, 372, 150, 40, "crypto · no KYC", LINE2, TXT, 15)
    # terminal card, right
    s += terminal(930, 92, 600, 320, [
        ("pip install tartarus-console", "cmd"),
        ("tartarus login", "cmd"),
        ("authenticated as you@dev", "ok"),
        ('tartarus "add retry + backoff to the api client"', "cmd"),
        ("editing   src/client.ts", "run"),
        ("running   npm test", "run"),
        ("12 passing · changes written", "ok"),
    ])
    s += bottom_bar(w, h, "h")
    s += '</svg>'
    write(os.path.join(HERE, "..", "profile", "assets", "hero.svg"), s)


def box(x, y, w, h, title, sub, accent=False):
    stroke = LIME if accent else LINE2
    tfill = LIME if accent else TXT
    out = (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="{BG1}" '
           f'stroke="{stroke}" stroke-width="{1.6 if accent else 1}"/>')
    out += text(x + w/2, y + 34, title, 19, tfill, "700", "middle", MONO)
    for i, line in enumerate(sub):
        out += text(x + w/2, y + 58 + i*21, line, 13.5, MUT, "400", "middle")
    return out


def arrow(x1, y1, x2, y2, rid):
    return (f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{LIME3}" '
            f'stroke-width="2" marker-end="url(#ah{rid})"/>')


def gen_ecosystem():
    w, h = 1400, 720
    s = head(w, h, "e")
    s += defs_bg(w, h, "e")
    s += (f'<defs><marker id="ahe" markerWidth="9" markerHeight="9" refX="7" '
          f'refY="3" orient="auto"><path d="M0,0 L7,3 L0,6 Z" fill="{LIME}"/>'
          f'</marker></defs>')
    s += place(WORD, WORD_W, WORD_H, 54, 48, 54)
    s += text(56, 150, "How the pieces fit", 30, TXT, "800")
    s += text(58, 184, "Every client talks to one OpenAI-compatible backend. "
              "Nothing calls the model directly.", 17, MUT, "400")
    # client row
    cy = 240
    cw, ch, gap = 300, 108, 40
    cx0 = 70
    clients = [
        ("tartarus-console", ["Terminal agent (CLI)"]),
        ("tartarus-sdk", ["Typed TypeScript client"]),
        ("tartarus-mcp", ["MCP server for editors"]),
    ]
    centers = []
    for i, (t, sub) in enumerate(clients):
        x = cx0 + i*(cw+gap)
        s += box(x, cy, cw, ch, t, sub)
        centers.append((x + cw/2, cy + ch))
    # cookbook aside
    s += box(cx0 + 3*(cw+gap), cy, cw-40, ch, "tartarus-cookbook",
             ["Copy-paste recipes"])
    # backend
    by = 430
    bw, bh = 760, 120
    bx = (w - bw) / 2
    s += box(bx, by, bw, bh, "api.tartarusai.dev  ·  /v1", [
        "Sanctum auth  ·  rate limit  ·  plan quota  ·  upstream bearer"], accent=True)
    s += text(bx + bw/2, by + 96, "OpenAI-compatible  ·  chat, streaming, tool-calling",
              13.5, MUT, "400", "middle")
    for (mx, my) in centers:
        s += arrow(mx, my + 4, w/2, by - 6, "e")
    # model
    my0 = 610
    mw = 420
    mx = (w - mw) / 2
    s += box(mx, my0, mw, 84, "Tartarus Coder", ["Hosted model · no GPU on your side"],
             accent=False)
    s += arrow(w/2, by + bh + 2, w/2, my0 - 6, "e")
    s += bottom_bar(w, h, "e")
    s += '</svg>'
    write(os.path.join(HERE, "..", "profile", "assets", "ecosystem.svg"), s)


# per-repo banner motifs (simple geometric glyphs, no emoji) ----------------
def motif(kind, cx, cy):
    g = f'<g transform="translate({cx},{cy})" fill="none" stroke="{LIME}" ' \
        f'stroke-width="6" stroke-linecap="round" stroke-linejoin="round">'
    if kind == "cli":
        g += f'<rect x="-70" y="-54" width="140" height="108" rx="12" ' \
             f'stroke="{LINE2}"/>' \
             f'<path d="M-40,-18 L-14,2 L-40,22"/><path d="M-2,26 L40,26" stroke="{LIME}"/>'
    elif kind == "sdk":
        g += f'<path d="M-20,-52 C-54,-52 -54,-6 -54,0 C-54,6 -54,52 -20,52"/>' \
             f'<path d="M20,-52 C54,-52 54,-6 54,0 C54,6 54,52 20,52"/>' \
             f'<circle cx="0" cy="0" r="7" fill="{LIME}" stroke="none"/>'
    elif kind == "mcp":
        g += f'<circle cx="-34" cy="-20" r="20"/><circle cx="34" cy="-20" r="20"/>' \
             f'<circle cx="0" cy="34" r="20"/>' \
             f'<path d="M-20,-8 L-6,22 M20,-8 L6,22 M-16,-28 L16,-28"/>'
    elif kind == "book":
        g += f'<path d="M0,-50 L0,50"/><path d="M0,-46 C-26,-58 -54,-50 -54,-44 ' \
             f'L-54,40 C-54,34 -26,30 0,42"/>' \
             f'<path d="M0,-46 C26,-58 54,-50 54,-44 L54,40 C54,34 26,30 0,42"/>'
    elif kind == "bench":
        g += f'<path d="M-54,46 L54,46"/><rect x="-46" y="6" width="22" height="40" ' \
             f'fill="{LIME}" stroke="none"/>' \
             f'<rect x="-11" y="-20" width="22" height="66" fill="{LIME}" stroke="none" ' \
             f'opacity="0.55"/>' \
             f'<rect x="24" y="-42" width="22" height="88" fill="{LIME}" stroke="none"/>'
    elif kind == "guide":
        g += f'<rect x="-44" y="-54" width="88" height="108" rx="8" stroke="{LINE2}"/>' \
             f'<path d="M-26,-26 L26,-26 M-26,-4 L26,-4 M-26,18 L8,18" stroke="{LIME}"/>'
    elif kind == "list":
        g += f'<circle cx="-40" cy="-34" r="5" fill="{LIME}" stroke="none"/>' \
             f'<circle cx="-40" cy="0" r="5" fill="{LIME}" stroke="none"/>' \
             f'<circle cx="-40" cy="34" r="5" fill="{LIME}" stroke="none"/>' \
             f'<path d="M-20,-34 L52,-34 M-20,0 L52,0 M-20,34 L52,34" stroke="{LINE2}"/>'
    g += '</g>'
    return g


def gen_banner(repo, eyebrow, name, tagline, kind):
    w, h = 1400, 360
    s = head(w, h, "b")
    s += defs_bg(w, h, "b")
    s += frame(w, h)
    # mark, top-left chip
    s += f'<g transform="translate(64,54)"><rect width="150" height="150" rx="20" ' \
         f'fill="{BG1}" stroke="{LINE2}"/></g>'
    s += place(MARK, MARK_W, MARK_H, 64 + 32, 54 + 18, 114)
    tx = 250
    s += text(tx, 110, eyebrow, 16, LIME, "700", "start", SANS, spacing="3.5")
    s += text(tx, 176, name, 60, TXT, "800", "start", MONO)
    s += text(tx, 222, tagline, 22, MUT, "400")
    s += ochip(tx, 250, 230, 40, "github.com/TartarusAIDev", LINE2, MUT, 14)
    s += motif(kind, w - 150, h/2 - 6)
    s += bottom_bar(w, h, "b")
    s += '</svg>'
    write(os.path.join(ORG_ROOT, repo, "assets", "banner.svg"), s)


def gen_feature(fname, title, lines, kind):
    w, h = 560, 360
    s = head(w, h, "f")
    s += defs_bg(w, h, "f")
    s += frame(w, h)
    s += motif(kind, 110, 110)
    s += text(40, 232, title, 27, TXT, "800", "start", MONO)
    for i, ln in enumerate(lines):
        s += text(40, 272 + i*26, ln, 15.5, MUT, "400")
    s += bottom_bar(w, h, "f")
    s += '</svg>'
    write(os.path.join(PROFILE_ASSETS, fname), s)


def main():
    print("Tartarus brand assets ->")
    gen_mark()
    gen_wordmark()
    gen_hero()
    gen_ecosystem()
    gen_feature("feat-terminal.svg", "Terminal agent",
                ["The tartarus CLI reads and edits your",
                 "files and runs commands in your repo."], "cli")
    gen_feature("feat-api.svg", "Developer API",
                ["An OpenAI-compatible /v1 endpoint.",
                 "Point any OpenAI SDK at it."], "sdk")
    gen_feature("feat-integrations.svg", "Editor integrations",
                ["MCP server plus a typed SDK for",
                 "Claude Desktop, Cursor and Cline."], "mcp")
    banners = [
        ("tartarus-console", "TERMINAL AGENT", "tartarus-console",
         "An uncensored AI coding agent in your terminal", "cli"),
        ("tartarus-sdk", "TYPESCRIPT SDK", "tartarus-sdk",
         "Typed client: chat, streaming, tool-calling", "sdk"),
        ("tartarus-mcp", "MCP INTEGRATION", "tartarus-mcp",
         "Use the model as a tool in MCP-compatible editors", "mcp"),
        ("tartarus-cookbook", "EXAMPLES", "tartarus-cookbook",
         "Runnable recipes: Python, Node, curl", "book"),
        ("refusal-bench", "EVALUATION", "refusal-bench",
         "Measure a model's false-refusal rate", "bench"),
        ("uncensored-ai-guide", "GUIDE", "uncensored-ai-guide",
         "Abliteration, local vs hosted, tool-calling", "guide"),
        ("awesome-uncensored-ai", "CURATED LIST", "awesome-uncensored-ai",
         "Uncensored and locally-runnable AI tooling", "list"),
    ]
    for repo, eye, name, tag, kind in banners:
        gen_banner(repo, eye, name, tag, kind)
    print("done.")


if __name__ == "__main__":
    main()
