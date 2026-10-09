"""Generate one standalone HTML page per experiment day, in the AINumbers house style.

CSS tokens, nav chrome and footer chrome are lifted from the live AINumbers pages
(repo/index.html + repo/guides/*.html) and inlined so each page is self-contained.
Table styling follows the site's `.compare` idiom.

Run from the ASIC root:  python digest/report/build_days.py
"""
import os
import re

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "days")

# ----------------------------------------------------------------------------
# Design: the Agent Staircase explainer. KIT_CSS, KIT_JS, SCENE_CSS and
# SCENE_HEAD_JS are verbatim copies of the AINumbers explainer kit and scene kit
# (generated into _staircase_kit.py). ASIC_CSS below adds only the components
# these pages carry and the explainer does not: nav and footer chrome, the stat
# strip, the prompt roster, grader cards, tables, findings, the verdict pair,
# source chips, the purpose panel and the benchmark charts. Each page's animated
# scene comes from _day_scenes.py.
# ----------------------------------------------------------------------------
from _staircase_kit import KIT_CSS, KIT_JS, SCENE_CSS, SCENE_HEAD_JS
from _day_scenes import scene_html

ASIC_CSS = """
:root{--teal-glow:rgba(20,184,166,.06)}
button{font-family:inherit}

/* nav */
nav{padding:0 2rem;height:52px;border-bottom:1px solid var(--border);background:rgba(8,14,26,.92);position:sticky;top:0;z-index:200;backdrop-filter:blur(8px)}
.nav-inner{max-width:1180px;margin:0 auto;height:100%;display:flex;align-items:center;justify-content:space-between;gap:16px}
.logo{display:flex;align-items:center;gap:10px;flex-shrink:0}
.logo-text{display:flex;flex-direction:column;gap:.08rem}
.logo-name{font-family:'JetBrains Mono',monospace;font-size:.88rem;font-weight:600;color:var(--bright);line-height:1}
.logo-ai{color:var(--teal)}.logo-co{color:var(--muted);font-size:.8rem}
.logo-tag{font-family:'JetBrains Mono',monospace;font-size:.5rem;letter-spacing:.22em;text-transform:uppercase;color:var(--muted);line-height:1}
.nav-breadcrumb{font-family:'JetBrains Mono',monospace;font-size:.6rem;color:var(--muted);display:flex;align-items:center;gap:6px;white-space:nowrap}
.nav-breadcrumb a{color:var(--body);transition:color .15s}
.nav-breadcrumb a:hover{color:var(--teal)}
.nav-links{display:flex;align-items:center;gap:13px;flex-shrink:0}
.nav-links a{font-family:'JetBrains Mono',monospace;font-size:.58rem;letter-spacing:.08em;text-transform:uppercase;color:var(--muted);transition:color .2s}
.nav-links a:hover{color:var(--teal-lt)}
.nav-links a.on{color:var(--teal)}
.nav-links a.cta{color:var(--bg);background:var(--teal);border:1px solid var(--teal);padding:.28rem .8rem;border-radius:6px;font-weight:600}
.nav-links a.cta:hover{opacity:.85;color:var(--bg)}

/* stat strip (inside the explainer hero) */
.stats{display:flex;flex-wrap:wrap;gap:2.6rem;padding:1.6rem 0 0;margin-top:1.8rem;border-top:1px solid var(--border)}
.stat .n{font-family:'DM Serif Display',serif;font-size:1.9rem;color:var(--white);line-height:1.1}
.stat .l{font-family:'JetBrains Mono',monospace;font-size:.52rem;letter-spacing:.14em;text-transform:uppercase;color:var(--muted);margin-top:5px}

/* panel note (the explainer kit styles the panel itself) */
.sec-note{font-family:'JetBrains Mono',monospace;font-size:.68rem;color:var(--body);margin:.5rem 0 1.3rem;line-height:1.7}
.prose{max-width:780px}
.prose p{font-size:.9rem;color:var(--body);line-height:1.9;margin-bottom:1rem}
.prose p:last-child{margin-bottom:0}
.prose strong{color:var(--text);font-weight:500}
.prose em{color:var(--bright);font-style:italic}
.prose a{color:var(--teal-lt);border-bottom:1px solid rgba(45,212,191,.3)}
.prose a:hover{opacity:.75}
.prose code{font-size:.86em;color:var(--teal-lt);background:var(--teal-dim);padding:.05rem .3rem;border-radius:3px}
.prose ul{margin:.6rem 0 0 1.1rem;color:var(--body)}
.prose li{font-size:.85rem;line-height:1.85;margin-bottom:.5rem}

/* prompt highlights (the explainer kit styles the .prompt block) */
.prompt pre .q{color:var(--white)}
.prompt pre b{color:var(--white);font-weight:500}
.prompt-head .lvl{text-transform:none}

/* prompt roster */
.roster{display:flex;flex-wrap:wrap;gap:6px;margin-top:.9rem}
.pill{font-family:'JetBrains Mono',monospace;font-size:.56rem;letter-spacing:.04em;color:var(--body);border:1px solid var(--border-2);border-radius:12px;padding:.28rem .65rem;background:var(--bg-3)}
.pill.t{color:var(--teal);border-color:rgba(20,184,166,.4)}
.pill.g{color:var(--gold);border-color:rgba(212,168,71,.4)}
.pill.p{color:var(--purple);border-color:rgba(155,114,245,.4)}

/* grader block */
.grader{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:14px;margin-top:.4rem}
.gcard{background:var(--bg-2);border:1px solid var(--border);border-radius:var(--radius-lg);padding:1rem 1.15rem}
.gcard .who{font-size:.92rem;color:var(--bright);font-weight:500;margin-bottom:.35rem;line-height:1.4}
.gcard .role{font-family:'JetBrains Mono',monospace;font-size:.54rem;letter-spacing:.14em;text-transform:uppercase;color:var(--teal);margin-bottom:.5rem}
.gcard .what{font-size:.76rem;color:var(--body);line-height:1.7}
.gcard .src{font-family:'JetBrains Mono',monospace;font-size:.55rem;color:var(--muted);margin-top:.6rem;word-break:break-all}

/* tables, styled like the explainer's run tables */
.tbl-wrap{margin:1rem 0 .4rem;overflow-x:auto}
table.compare{width:100%;border-collapse:collapse;min-width:640px;font-size:.8rem}
table.compare caption{caption-side:top;text-align:left;padding:.2rem 0 .6rem;font-family:'JetBrains Mono',monospace;font-size:.56rem;letter-spacing:.14em;text-transform:uppercase;color:var(--body)}
table.compare th{font-family:'JetBrains Mono',monospace;font-size:.54rem;letter-spacing:.14em;text-transform:uppercase;color:var(--body);text-align:left;padding:.5rem .6rem;border-bottom:1px solid var(--border-2);white-space:nowrap;vertical-align:bottom}
table.compare td{padding:.55rem .6rem;border-bottom:1px solid var(--border);color:var(--text);vertical-align:top}
table.compare td:first-child{font-family:'JetBrains Mono',monospace;font-size:.72rem;color:var(--gold);white-space:nowrap}
table.compare tbody tr:hover td{background:rgba(20,184,166,.035)}
table.compare th.num,table.compare td.num{text-align:right;font-family:'JetBrains Mono',monospace}
table.compare th.hl{color:var(--teal)}
table.compare td.hl{background:var(--teal-glow)}
.mk{font-family:'JetBrains Mono',monospace;font-size:.72rem}
.ok{color:var(--green)}.bad{color:var(--red)}.mid{color:var(--gold)}.dim{color:var(--muted)}.teal{color:var(--teal-lt)}.pur{color:var(--purple)}
.legend{margin-top:.7rem;font-family:'JetBrains Mono',monospace;font-size:.55rem;color:var(--muted);line-height:1.8}

/* findings */
.findings{display:grid;gap:12px;margin-top:.4rem}
.finding{background:var(--bg-2);border:1px solid var(--border);border-left:2px solid var(--teal);border-radius:var(--radius);padding:.9rem 1.1rem}
.finding.warn{border-left-color:var(--gold)}
.finding.bad{border-left-color:var(--red)}
.finding .h{font-size:.88rem;color:var(--bright);font-weight:500;margin-bottom:.3rem;line-height:1.45}
.finding .b{font-size:.79rem;color:var(--body);line-height:1.8}
.finding .b code{font-size:.85em;color:var(--teal-lt);background:var(--teal-dim);padding:.05rem .28rem;border-radius:3px}
/* best / weakest pair */
.verdict-pair{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin:.4rem 0 1.4rem}
.vp{background:var(--bg-2);border:1px solid var(--border);border-radius:var(--radius);padding:.9rem 1.1rem}
.vp.best{border-left:2px solid var(--green)}
.vp.weak{border-left:2px solid var(--red)}
.vp .tag{font-family:'JetBrains Mono',monospace;font-size:.5rem;letter-spacing:.2em;text-transform:uppercase;color:var(--muted);margin-bottom:.4rem}
.vp.best .tag{color:var(--green)}
.vp.weak .tag{color:var(--red)}
.vp .model{font-size:.88rem;color:var(--bright);font-weight:500;margin-bottom:.35rem;line-height:1.45}
.vp .vp-why{font-size:.79rem;color:var(--body);line-height:1.8}
.vp .vp-why code{font-size:.85em;color:var(--teal-lt);background:var(--teal-dim);padding:.05rem .28rem;border-radius:3px}

/* source list */
.srcs{display:flex;flex-wrap:wrap;gap:6px;margin-top:.5rem}
.srcs span{font-family:'JetBrains Mono',monospace;font-size:.55rem;color:var(--muted);border:1px solid var(--border);border-radius:4px;padding:.2rem .5rem;background:var(--bg-2)}

/* closing purpose panel */
.purpose{margin-top:2.4rem;border:1px solid var(--border-2);border-left:2px solid var(--teal);border-radius:var(--radius-lg);background:var(--bg-2);padding:1.7rem 1.9rem}
.purpose .kicker{font-family:'JetBrains Mono',monospace;font-size:.52rem;letter-spacing:.16em;text-transform:uppercase;color:var(--teal);margin-bottom:.55rem}
.purpose h2{font-family:'DM Serif Display',serif;font-size:1.34rem;font-weight:400;color:var(--white);margin:0 0 .95rem;line-height:1.25}
.purpose p{font-size:.83rem;color:var(--text);line-height:1.8;margin:0 0 .85rem}
.purpose p:last-of-type{margin-bottom:0}
.purpose b,.purpose strong{color:var(--bright);font-weight:500}
.purpose code{font-family:'JetBrains Mono',monospace;font-size:.85em;color:var(--teal-lt);background:var(--teal-dim);padding:.05rem .28rem;border-radius:3px}
.purpose .statement{margin-top:1.2rem;padding-top:1.2rem;border-top:1px solid var(--border)}
.purpose .statement p{font-size:.86rem;line-height:1.82;margin:0 0 .8rem}
.purpose .statement p:last-child{margin-bottom:0}
.purpose .caveat{margin-top:1.3rem;padding-top:1.15rem;border-top:1px solid var(--border);font-family:'JetBrains Mono',monospace;font-size:.56rem;color:var(--muted);line-height:1.85}

/* benchmark charts — inline SVG, no JS */
.chart{background:var(--bg-2);border:1px solid var(--border);border-radius:var(--radius);padding:1.1rem 1.2rem 1rem;margin:.5rem 0 1.2rem}
.chart-title{font-family:'JetBrains Mono',monospace;font-size:.52rem;letter-spacing:.2em;text-transform:uppercase;color:var(--muted);margin-bottom:.45rem}
.chart-sub{font-size:.79rem;color:var(--body);line-height:1.72;margin-bottom:1rem;max-width:74ch}
.chart svg{display:block;width:100%;height:auto}
.chart-legend{display:flex;gap:16px;flex-wrap:wrap;font-family:'JetBrains Mono',monospace;font-size:.5rem;letter-spacing:.14em;text-transform:uppercase;color:var(--muted);margin-top:.85rem}
.chart-legend i{display:inline-block;width:9px;height:9px;border-radius:2px;margin-right:6px;vertical-align:-1px}
.chart-note{font-size:.73rem;color:var(--muted);line-height:1.75;margin-top:.85rem;border-top:1px solid var(--border);padding-top:.7rem}
.chart-note code{font-family:'JetBrains Mono',monospace;font-size:.88em;color:var(--teal-lt)}

/* footer */
footer{border-top:1px solid var(--border);background:var(--bg-2);padding:24px 0;margin-top:2rem}
.footer-inner{max-width:1180px;margin:0 auto;padding:0 24px;display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:16px}
.footer-brand{font-family:'JetBrains Mono',monospace;font-size:.8rem;font-weight:500;color:var(--bright)}
.footer-brand span{color:var(--muted)}
.footer-cc{font-size:.62rem;color:var(--muted);margin-top:4px}
.footer-nav{display:flex;gap:14px;flex-wrap:wrap}
.footer-nav a{font-family:'JetBrains Mono',monospace;font-size:.56rem;letter-spacing:.08em;text-transform:uppercase;color:var(--muted)}
.footer-nav a:hover{color:var(--teal)}

@media(max-width:820px){
  .nav-links a:not(.cta){display:none}
  .nav-breadcrumb{display:none}
  .stats{gap:1.6rem}
  .verdict-pair{grid-template-columns:1fr}
}
"""

CSS = "<style>\n" + KIT_CSS + "\n" + SCENE_CSS + "\n" + ASIC_CSS + "</style>"

DAYS = [("index", "Overview"), ("day1", "Day 1"), ("day2", "Day 2"), ("day3", "Day 3"),
        ("day4", "Day 4"), ("day5", "Day 5"), ("day6", "Day 6"), ("day7", "Day 7"),
        ("day8", "Day 8")]


def nav(active):
    out = []
    for fid, label in DAYS:
        cls = "cta" if fid == "index" else ("on" if fid == active else "")
        href = "index.html" if fid == "index" else "%s.html" % fid
        if fid == "index":
            label = "All days"
        c = ' class="%s"' % cls if cls else ""
        out.append('<a href="%s"%s>%s</a>' % (href, c, label))
    return "\n      ".join(out)


def page(fid, title, body):
    html = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>%(title)s | Free Web AI Red-Team Benchmark</title>
<meta name="description" content="Per-day record of a zero-spend, human-pasted benchmark of free web AI models on ASIC physical-design and regulatory-compliance tasks: the prompt, the grader, and how each model performed.">
<meta name="robots" content="index, follow">
<meta name="author" content="Post Oak Labs">
<link rel="icon" type="image/svg+xml" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 32 32'><rect width='32' height='32' rx='7' fill='%%23080E1A'/><text x='50%%25' y='56%%25' dominant-baseline='middle' text-anchor='middle' font-family='Sora,sans-serif' font-weight='600' font-size='13' fill='%%2314B8A6'>AI</text></svg>">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=Sora:wght@300;400;500;600&family=JetBrains+Mono:wght@300;400;500&display=swap" rel="stylesheet">
<script>%(head_js)s</script>
%(css)s
</head>
<body>
<nav aria-label="Site navigation">
  <div class="nav-inner">
    <div class="logo">
      <div class="logo-text">
        <div class="logo-name"><span class="logo-ai">AI</span>Numbers<span class="logo-co">.co</span></div>
        <div class="logo-tag">Free Web AI Benchmark</div>
      </div>
    </div>
    <div class="nav-breadcrumb"><a href="index.html">Benchmark</a> <span>&rarr;</span> %(title)s</div>
    <div class="nav-links">
      %(nav)s
    </div>
  </div>
</nav>
%(body)s
<footer>
  <div class="footer-inner">
    <div>
      <div class="footer-brand"><span style="color:var(--teal)">AI</span>Numbers<span>.co</span> &middot; Free Web AI Red-Team Benchmark</div>
      <div class="footer-cc">Every response was produced by a human pasting a prompt into a free web chat interface. No APIs, no harnesses, no automated scripts. Zero spend. One model in these tables, GLM 5.3 Flash, was also run separately through an API harness; the two deployments are not comparable and only the free web one is measured here.</div>
    </div>
    <div class="footer-nav">
      <a href="index.html">All days</a>
      <a href="day1.html">Day 1</a><a href="day2.html">Day 2</a><a href="day3.html">Day 3</a><a href="day4.html">Day 4</a>
      <a href="day5.html">Day 5</a><a href="day6.html">Day 6</a><a href="day7.html">Day 7</a><a href="day8.html">Day 8</a>
    </div>
  </div>
</footer>
<div class="pbar" id="pbar" role="toolbar" aria-label="Presenter controls">
  <button type="button" class="btn" id="pPrev" aria-label="Previous section">&#8592;</button>
  <span class="count" id="pCount">1 / 1</span>
  <button type="button" class="btn" id="pNext" aria-label="Next section">&#8594;</button>
  <div class="rail"><svg id="pRail" viewBox="0 0 1000 60" preserveAspectRatio="none" aria-hidden="true"></svg></div>
  <button type="button" class="btn" id="pAuto" aria-pressed="false">Autoplay</button>
  <button type="button" class="btn" id="pExit">Exit</button>
</div>
<script>%(kit_js)s</script>
</body>
</html>""" % dict(title=title, css=CSS, nav=nav(fid), body=body, head_js=SCENE_HEAD_JS, kit_js=KIT_JS)

    # Number the panels in page order; section() leaves a placeholder because it
    # is called while the page bodies are assembled, before a page exists.
    count = [0]

    def _number(_m):
        count[0] += 1
        return '<span class="stage-n">%d</span>' % count[0]
    return re.sub(r'<span class="stage-n">##</span>', _number, html)


def hero(eyebrow, h1, desc, stats):
    """The explainer hero: eyebrow, headline, stat strip, Present button and the section staircase."""
    s = "".join('<div class="stat"><div class="n">%s</div><div class="l">%s</div></div>' % (n, l)
                for n, l in stats)
    return ('<header class="hero"><div class="wrap">\n<div class="eyebrow">%s</div>\n<h1>%s</h1>\n'
            '<p>%s</p>\n<div class="stats">%s</div>\n'
            '<div class="hero-actions"><button type="button" class="btn btn-primary" id="btnPresent">Present this page</button>'
            '<span class="hint">Presenter mode shows one section per screen. Arrow keys move, A toggles autoplay, Esc exits.</span></div>\n'
            '<div class="stair-map" role="navigation" aria-label="Section map: every section on this page">'
            '<svg id="stairMap" viewBox="0 0 1000 260" aria-hidden="false" role="list"></svg></div>\n'
            '</div></header>' % (eyebrow, h1, desc, s))


# Short staircase labels and the part each section belongs to: 1 sets the task up,
# 2 reports the results, 3 draws the conclusions. Unlisted labels fall into part 2.
# Ranking opens every page as the headline, so it joins part 1 and the staircase
# colours rise in page order (teal, then gold, then purple).
STAIR = {"The prompt": ("Prompt", 1), "What graded it": ("Grader", 1), "What this is": ("About", 1),
         "How each model performed": ("Results", 2), "Ranking": ("Ranking", 1), "The eight days": ("Days", 2),
         "What it found": ("Findings", 3), "Three lessons beyond this corpus": ("Lessons", 3),
         "Source files": ("Sources", 3)}


def section(label, heading, body, note=None):
    """One explainer panel. The stage number is filled in by page(), in page order."""
    short, part = STAIR.get(label, (label, 2))
    sid = "s-" + re.sub(r"[^a-z0-9]+", "-", short.lower()).strip("-")
    n = '<div class="sec-note">%s</div>' % note if note else ""
    return ('<section class="panel" id="%s" data-stair="%s" data-part="%d"><div class="wrap">\n'
            '<div class="panel-head"><span class="stage-n">##</span><div><div class="kicker">%s</div><h2>%s</h2></div></div>\n'
            '%s\n%s\n</div></section>' % (sid, short, part, label, heading, n, body))


def prompt_card(pid, ver, body, foot):
    """The prompt as the explainer shows prompts: a purple-edged block, the text verbatim."""
    return ('<div class="prompt">\n<div class="prompt-head"><span>%s</span><span class="lvl">%s</span></div>\n'
            '<pre>%s</pre>\n<div class="answer">%s</div>\n</div>' % (pid, ver, body, foot))


def roster(pills):
    return '<div class="roster">%s</div>' % "".join(
        '<span class="pill%s">%s</span>' % ((" " + c) if c else "", t) for t, c in pills)


def table(caption, headers, rows, highlight_col=None):
    th = "".join('<th%s>%s</th>' % (' class="hl"' if i == highlight_col else "", h)
                 for i, h in enumerate(headers))
    tr = ""
    for r in rows:
        tds = ""
        for i, c in enumerate(r):
            cls = []
            if isinstance(c, tuple):
                c, extra = c
                if extra:
                    cls.append(extra)
            if i == highlight_col:
                cls.append("hl")
            tds += '<td%s>%s</td>' % (' class="%s"' % " ".join(cls) if cls else "", c)
        tr += "<tr>%s</tr>\n" % tds
    return ('<div class="tbl-wrap"><table class="compare"><caption>%s</caption>\n'
            '<thead><tr>%s</tr></thead>\n<tbody>\n%s</tbody></table></div>' % (caption, th, tr))


def findings(items):
    out = []
    for kind, h, b in items:
        out.append('<div class="finding%s"><div class="h">%s</div><div class="b">%s</div></div>'
                   % ((" " + kind) if kind else "", h, b))
    return '<div class="findings">%s</div>' % "".join(out)


def verdict_pair(best_model, best_why, weak_model, weak_why):
    """The two names a reader always asks for: strongest and weakest on this day.

    Each `why` is a measured fact, kept under 25 words so it reads at a glance.
    """
    return ('<div class="verdict-pair">\n'
            '<div class="vp best"><div class="tag">Best performer</div>'
            '<div class="model">%s</div><div class="vp-why">%s</div></div>\n'
            '<div class="vp weak"><div class="tag">Weakest performer</div>'
            '<div class="model">%s</div><div class="vp-why">%s</div></div>\n'
            '</div>' % (best_model, best_why, weak_model, weak_why))


def srcs(files):
    return '<div class="srcs">%s</div>' % "".join("<span>%s</span>" % f for f in files)


# ---------------------------------------------------------------------------
# Benchmark charts. Inline SVG so the pages stay self-contained: no JS, no
# chart library, no build step. Every chart plots one named metric that the
# day's own table already carries, and the caption says which one, so a bar
# can always be traced back to a measured row.
# ---------------------------------------------------------------------------

C_GREEN = "#22C55E"
C_RED = "#EF4444"
C_TEAL = "#14B8A6"
C_TEAL_LT = "#2DD4BF"
C_DIM = "#3A4761"
C_MUTED = "#7C8AA5"
C_TEXT = "#C3CDE0"
C_BRIGHT = "#E8EEF9"

# GLM 5.3 Flash appears in these charts as the free web chat model, which is the
# quantized build. The same model name also ran as an API harness agent under
# Zcode and scored very differently, so every chart that contains it carries an
# asterisk and this footnote rather than leaving the reader to assume the two
# numbers describe the same thing.
GLM_STAR = "*"
GLM_NOTE = ("%s The free web chat build of GLM 5.3 Flash, the quantized one. It is not the "
            "harness version run under Zcode, and the two do not score alike."
            % GLM_STAR)


def _mark_glm(rows):
    """Asterisk any GLM row and report whether one was present."""
    out, hit = [], False
    for label, value, display in rows:
        if label.lower().startswith("glm"):
            label, hit = label + GLM_STAR, True
        out.append((label, value, display))
    return out, hit


def _esc(t):
    return t


def bar_chart(title, subtitle, rows, note=None, legend=None, scale_max=None,
              width=680, neutral=False):
    """Horizontal bar chart, best first.

    `rows` is a list of (label, value, display). `value` drives bar length;
    `display` is what the reader sees at the bar's end. Colour marks the value
    groups, not the row positions: the top value group is green and the bottom
    value group is red, so models that tied always share a colour and a tie is
    never split into a winner and a loser by list order. Pass `neutral=True`
    when a longer bar is not better (Day 8 charts strictness, not accuracy),
    which draws every bar teal so the colour implies no verdict.
    """
    n = len(rows)
    row_h, gap = 22, 8
    top = 6
    label_w, val_w = 158, 62
    track_x = label_w + 10
    track_w = width - track_x - val_w
    height = top + n * (row_h + gap) + 4
    mx = scale_max if scale_max else max(r[1] for r in rows)
    hi, lo = max(r[1] for r in rows), min(r[1] for r in rows)

    # Asterisk the GLM row and add its footnote here, so every chart that
    # contains the model is marked without the caller having to remember.
    rows, has_glm = _mark_glm(rows)
    if has_glm:
        note = (note + " " if note else "") + GLM_NOTE

    parts = ['<svg viewBox="0 0 %d %d" role="img" aria-label="%s">' % (width, height, title)]
    for i, (label, value, display) in enumerate(rows):
        y = top + i * (row_h + gap)
        cy = y + row_h / 2.0
        if neutral:
            col = C_TEAL
        elif value == hi:
            col = C_GREEN
        elif value == lo:
            col = C_RED
        else:
            col = C_TEAL
        parts.append('<text x="%d" y="%.1f" text-anchor="end" font-family="JetBrains Mono, monospace" '
                     'font-size="10.5" fill="%s">%s</text>'
                     % (label_w, cy + 3.6, C_TEXT, label))
        parts.append('<rect x="%d" y="%d" width="%d" height="%d" rx="3" fill="%s" opacity="0.30"/>'
                     % (track_x, y, track_w, row_h, C_DIM))
        if value <= 0:
            # A legitimate zero. Draw a small hollow marker so the row reads as
            # "nothing here" instead of looking like a bar that failed to render.
            parts.append('<rect x="%d" y="%d" width="7" height="%d" rx="2" fill="none" stroke="%s" '
                         'stroke-width="1.2" opacity="0.75"/>' % (track_x, y, row_h, col))
        else:
            w = max(2.0, track_w * (value / mx if mx else 0))
            parts.append('<rect x="%d" y="%d" width="%.1f" height="%d" rx="3" fill="%s"/>'
                         % (track_x, y, w, row_h, col))
        parts.append('<text x="%d" y="%.1f" font-family="JetBrains Mono, monospace" font-size="10.5" '
                     'fill="%s">%s</text>'
                     % (track_x + track_w + 8, cy + 3.6, C_BRIGHT, display))
    parts.append('</svg>')

    lg = ""
    if legend:
        lg = ('<div class="chart-legend">%s</div>'
              % "".join('<span><i style="background:%s"></i>%s</span>' % (c, t) for c, t in legend))
    nt = '<div class="chart-note">%s</div>' % note if note else ""
    return ('<div class="chart"><div class="chart-title">%s</div>'
            '<div class="chart-sub">%s</div>%s%s%s</div>'
            % (title, subtitle, "".join(parts), lg, nt))


def chart_section(fid, charts):
    """One 'How the field ranked' section, built from the day's chart list."""
    if fid == "index":
        return section("Ranking", "How the field ranked across the eight days", "".join(charts))
    return section("Ranking", "How the field ranked on this day", "".join(charts))


# Day 1 and Day 7 recorded a couple of models under short spellings, and Day 4
# tagged one as "(prose)". Normalise so a traced line is one model, not two.
LABEL_FIX = {"glm 5.3": "glm 5.3 flash", "glm flash": "glm 5.3 flash",
             "solar pro": "solar", "mimo (prose)": "mimo"}

# Day 8's graded metric is schema compliance, which all three models passed
# 30/30. Its bar chart deliberately shows strictness instead, so ranking uses
# this explicit tie rather than the strictness numbers.
RANK_OVERRIDE = {"day8": [("deepseek", 100.0), ("kimi", 100.0), ("sonnet", 100.0)]}

DAY_ORDER = ["day1", "day2", "day3", "day4", "day5", "day6", "day7", "day8"]


def _norm(label):
    return LABEL_FIX.get(label, label)


def _scores(pairs):
    """Score out of 100 for each model, from where it placed in that day's field.

    100 means it beat every other model that ran that day; 0 means every other
    model beat it. Scoring inside the day is what makes the numbers comparable
    across days: a raw rank of 3 in a four-model day is near the bottom while a
    raw rank of 3 in a ten-model day is near the top, and the two must not be
    averaged as if they were the same standing. Ties share a score, so a tie is
    never split into a winner and a loser.
    """
    n = len(pairs)
    out = {}
    for m, v in pairs:
        if n < 2:
            out[m] = 100.0
            continue
        above = sum(1 for _, w in pairs if w > v)
        out[m] = 100.0 * (n - 1 - above) / (n - 1)
    return out


def index_charts():
    """The index bar chart: mean score across the days each model ran.

    Scoring inside each day is what makes a single ranking possible across days
    whose metrics differ: each model is scored only against the field it
    actually ran against that day, so no two different scales meet on one axis.

    A per-day line chart was tried here and removed. With eight models traced
    over eight days the lines crossed repeatedly and every model that topped a
    day stacked its endpoint label on the same pixel, so it could not be read.
    The bar chart carries the same information legibly.
    """
    per_day = {}
    for d in DAY_ORDER:
        pairs = RANK_OVERRIDE.get(d)
        if pairs is None:
            pairs = [(_norm(m), v) for m, v, _ in CHARTS[d]["rows"]]
        per_day[d] = _scores(pairs)

    # --- mean score bar chart ---
    seen = {}
    for d in DAY_ORDER:
        for m, r in per_day[d].items():
            seen.setdefault(m, []).append(r)
    # A model that ran once and did well would otherwise top this chart on a
    # single day's evidence, so the average is restricted to models with a
    # record long enough to average.
    MIN_DAYS = 3
    thin = sorted(m for m, rs in seen.items() if len(rs) < MIN_DAYS)
    mean = {m: sum(rs) / float(len(rs)) for m, rs in seen.items() if len(rs) >= MIN_DAYS}
    rows = []
    for m, mv in sorted(mean.items(), key=lambda kv: -kv[1]):
        rows.append((m, mv, "%.0f%%" % mv))
    bar = bar_chart(
        "Average score, best first",
        "How well each model did, on average. Every day the models are ranked against each other "
        "and scored out of 100, where 100 is the best result in that day&rsquo;s field and 0 is the "
        "worst. Each bar averages those scores over the days the model ran. A model that missed a "
        "day is not marked down for it.",
        rows, scale_max=100, neutral=False,
        note="The scores come from the day charts on this page, each worked out inside its own day. "
             "On Day 8 all three models passed the graded schema 30/30, so they score level. Day 1 "
             "had no ground truth, so its ordering is a tier order and is the weakest input to this "
             "average. Models with fewer than %d gradable days are left out rather than averaged on "
             "a thin record: %s."
             % (MIN_DAYS, ", ".join("<code>%s</code>" % m for m in thin)),
    )

    # A caveat the tables cannot carry themselves: the same model name appears
    # in two deployments with very different results, and only one is measured
    # on this page. The contrast is documented in the estate; the reason for it
    # is not, so the reason is attributed rather than asserted.
    glm = (
        '<div class="chart"><div class="chart-title">One model name, two deployments</div>'
        '<div class="chart-sub">GLM 5.3 Flash appears in the tables above as a free web chat model, '
        'and on most days it was among the weakest. The same model name was also run as an API '
        'harness agent on this project&rsquo;s own repository lane, where it did work of a different '
        'order. These are not the same measurement, and only the free web one is in the tables.'
        '</div>'
        '<div class="chart-note"><b>Free web chat.</b> It submitted the identical Alpha&nbsp;21264 '
        'recall text for eight different prompts, confirmed 2 of 20 claims on the Day&nbsp;4 recall '
        'slices (10%, the lowest of any model), and was suspended from the recall slices until the '
        'cause could be identified.<br><br>'
        '<b>API harness.</b> It re-derived the live state of 38 pull requests across three '
        'repositories from GitHub rather than trusting the handoff report it was given. It ran its '
        'own derivative-work check on a licence notice (upstream base 80 lines, branch 78, 32 lines '
        'in common), found a wrong verdict in an existing adjudication and corrected it in place, and '
        'wrote a report that passed five of five independent spot-checks. It merged nothing and '
        'pushed nothing, which its brief required.<br><br>'
        '<b>Why the gap.</b> The operator&rsquo;s account is that the harness runs used the maximum '
        'thinking level and a less quantized serving path. That is a plausible explanation rather '
        'than a measured one. Nothing in this corpus isolates either factor, so it is recorded as a '
        'caveat on reading the tables.</div></div>'
    )
    return [bar, glm]


def grader_cards(cards):
    return '<div class="grader">%s</div>' % "".join(
        '<div class="gcard"><div class="role">%s</div><div class="who">%s</div>'
        '<div class="what">%s</div><div class="src">%s</div></div>' % (role, who, what, src)
        for role, who, what, src in cards)


def S(t):
    """section wrapper shorthand"""
    return section(*t)


def purpose(kicker, heading, paras, caveat):
    """Closing panel: what this exercise was for, and why it is worth anything."""
    body = "".join("<p>%s</p>" % p for p in paras)
    return ('<section class="panel" id="s-purpose" data-stair="Purpose" data-part="3"><div class="wrap">\n'
            '<div class="purpose">\n<div class="kicker">%s</div>\n<h2>%s</h2>\n'
            '<div class="statement">%s</div>\n<div class="caveat">%s</div>\n</div>\n</div></section>'
            % (kicker, heading, body, caveat))


# ============================================================================
# CHART DATA
# ----------------------------------------------------------------------------
# One metric per day, taken from that day's own table. No composite score is
# invented and no two days' numbers are ever compared: the index chart plots
# a model's RANK inside each day, which is computable from heterogeneous
# metrics without pretending they share a scale.
# ============================================================================

CHARTS = {
    "day1": dict(
        title="Run-1 tier, T1 best",
        subtitle="Day 1 had no ground truth to grade against, so tier is the only ranking the day "
                 "supports. T1 = best of run, T2 = complete but generic, T3 = broke the output "
                 "contract. Bar length shows which tier each model reached.",
        scale_max=3,
        rows=[("opus 5", 3, "T1"), ("sonnet", 3, "T1"), ("kimi", 3, "T1"),
              ("glm 5.3", 2, "T2"), ("meta", 2, "T2"), ("chatgpt", 2, "T2"),
              ("mimo", 2, "T2"), ("minimax m3", 2, "T2"), ("tencent yunbao", 2, "T2"),
              ("deepseek", 1.5, "T2&ndash;T3"), ("gemini", 1.5, "T2&ndash;T3"),
              ("mistral", 1.5, "T2&ndash;T3"), ("qwen", 1.5, "T2&ndash;T3"),
              ("solar pro", 1, "T3")],
        note="The four models the log grouped as <code>T2&ndash;T3</code> are drawn at the midpoint "
             "and labelled as a group. <code>minimax (free)</code> is absent: a quota error returned "
             "no output, so it has no tier.",
    ),
    "day2": dict(
        title="JCS canonicalization: exact vectors passed",
        subtitle="Share of each model&rsquo;s own JCS vector set that canonicalized exactly under "
                 "RFC&nbsp;8785. Class-1 arithmetic saturated near 100% for most of the field, so "
                 "this is the slice where Day&nbsp;2 separates.",
        scale_max=100,
        rows=[("kimi", 100.0, "12/12"), ("sonnet", 100.0, "12/12"), ("meta", 100.0, "10/10"),
              ("chatgpt", 90.9, "10/11"), ("grok", 90.9, "10/11"), ("qwen", 90.0, "9/10"),
              ("solar", 89.5, "17/19"), ("deepseek", 86.7, "13/15"),
              ("mimo", 81.8, "9/11"), ("yuanbao", 81.8, "9/11"), ("glm 5.3 flash", 81.8, "9/11"),
              ("gemini", 75.0, "6/8"), ("minimax m3", 66.7, "6/9"),
              ("minimax 2.7", 50.0, "5/10"), ("mistral", 27.3, "3/11")],
        note="Denominators differ because models returned different numbers of vectors, so a short "
             "set and a long set are not the same test. <code>solar</code>&rsquo;s 17/19 is the "
             "largest set in the batch; <code>mistral</code>&rsquo;s 3/11 is six substantive "
             "failures.",
    ),
    "day3": dict(
        title="Boundary rules verified, of 7",
        subtitle="Verdicts on the inclusivity table that matched the operative regulatory text. "
                 "Seven rules per model, each graded against the clause it turns on.",
        scale_max=100,
        rows=[("deepseek", 100.0, "7/7"), ("glm 5.3 flash", 100.0, "7/7"), ("grok", 100.0, "7/7"),
              ("meta", 100.0, "7/7"), ("mimo", 100.0, "7/7"), ("qwen", 100.0, "7/7"),
              ("chatgpt", 85.7, "6/7"), ("gemini", 85.7, "6/7"), ("kimi", 85.7, "6/7 +S"),
              ("minimax 2.7", 85.7, "6/7 +S"), ("yuanbao", 85.7, "6/7 +S"),
              ("mistral", 71.4, "5/7 +S"), ("minimax m3", 71.4, "5/7 +I")],
        note="<code>+S</code> marks a self-inconsistency on one rule, <code>+I</code> an "
             "indeterminate verdict. Both are counted as a rule not verified.",
    ),
    "day4": dict(
        title="Recall confirmation rate",
        subtitle="Share of a model&rsquo;s graded claims that the source paper confirms. This is the "
                 "only day in the collection where a model is scored against the document rather "
                 "than against another model.",
        scale_max=100,
        rows=[("meta", 100.0, "25/25"), ("qwen", 100.0, "14/14"), ("sonnet", 100.0, "12/12"),
              ("chatgpt", 92.0, "23/25"), ("grok", 92.0, "23/25"), ("yuanbao", 92.0, "22/24"),
              ("gemini", 88.0, "14/16"), ("deepseek", 80.0, "20/25"), ("kimi", 79.0, "15/19"),
              ("mimo (prose)", 63.0, "5/8"), ("minimax m3", 38.0, "6/16"),
              ("minimax 2.7", 38.0, "9/24"), ("glm 5.3 flash", 10.0, "2/20")],
        note="Denominators are the claims each model actually made, so a model that claimed less is "
             "not rewarded for it. <code>glm 5.3 flash</code> resubmitted the same Alpha&nbsp;21264 "
             "text for eight different prompts, which is why 16 of its 20 entries sit outside the "
             "paper.",
    ),
    "day5": dict(
        title="Reg Z recomputation, exact of 9",
        subtitle="Reg&nbsp;Z figures recomputed in scratch Python and matched exactly. Twelve of the "
                 "fifteen graded models closed all nine.",
        scale_max=100,
        rows=[("chatgpt", 100.0, "9/9"), ("gemini", 100.0, "9/9"), ("glm 5.3 flash", 100.0, "9/9"),
              ("grok", 100.0, "9/9"), ("kimi", 100.0, "9/9"), ("longcat", 100.0, "9/9"),
              ("meta", 100.0, "9/9"), ("mimo", 100.0, "9/9"), ("minara", 100.0, "9/9"),
              ("qwen", 100.0, "9/9"), ("sonnet", 100.0, "9/9"), ("yuanbao", 100.0, "9/9"),
              ("deepseek", 88.9, "8/9"), ("minimax 2.7", 55.6, "5/9"), ("mistral", 22.2, "2/9")],
        note="Measured from <code>digest/_verify/d5run/d5permodel.json</code>. <code>solar</code> is "
             "absent: its Reg&nbsp;Z answer was prose, so there was nothing to recompute.",
    ),
    "day6": dict(
        title="Browser anchors correct, of 3",
        subtitle="The three anchor questions whose answers were already known from the estate&rsquo;s "
                 "own browser ground truth. A model scores by agreeing where the record agrees and "
                 "disagreeing where the record disagrees.",
        scale_max=100,
        rows=[("deepseek", 100.0, "3/3"), ("kimi", 100.0, "3/3"), ("minara", 100.0, "3/3"),
              ("sonnet", 100.0, "3/3"), ("yuanbao", 100.0, "3/3"),
              ("chatgpt", 66.7, "2/3"), ("gemini", 66.7, "2/3"), ("grok", 66.7, "2/3"),
              ("mimo", 66.7, "2/3"),
              ("glm 5.3 flash", 33.3, "1/3"), ("longcat", 33.3, "1/3"), ("minimax", 33.3, "1/3"),
              ("mistral", 33.3, "1/3"), ("qwen", 33.3, "1/3")],
        note="The correct pattern is agree / agree / disagree. Only five models matched all three. "
             "The separate C-v5 citation anchors are not in this chart: twelve models returned "
             "<code>PASS</code> there, and <code>qwen</code> and <code>solar</code> returned "
             "<code>WRONG-CORRECTION</code>. <code>meta</code> and <code>solar</code> are absent "
             "here because their browser files did not parse.",
    ),
    "day7": dict(
        title="How far each model got, of 3 steps",
        subtitle="Nobody finished the task. Step 1 is a file that parses as JSON, step 2 is a usable "
                 "verdict key inside it, step 3 is the full seven-key schema. Eight models reached "
                 "step 2, three parsed but named no verdict, and four never produced parseable JSON.",
        scale_max=3,
        rows=[("deepseek", 2, "2 / 3"), ("gemini", 2, "2 / 3"), ("glm flash", 2, "2 / 3"),
              ("grok", 2, "2 / 3"), ("kimi", 2, "2 / 3"), ("longcat", 2, "2 / 3"),
              ("sonnet", 2, "2 / 3"), ("yuanbao", 2, "2 / 3"),
              ("mimo", 1, "1 / 3"), ("minimax", 1, "1 / 3"), ("qwen", 1, "1 / 3"),
              ("chatgpt", 0, "0 / 3"), ("meta", 0, "0 / 3"), ("mistral", 0, "0 / 3"),
              ("solar", 0, "0 / 3")],
        note="No model reached step 3: the best result on any single key was 1 of 7, and the verdict "
             "vocabulary was invented afresh by each one. <code>chatgpt</code> (12.1&nbsp;KB), "
             "<code>meta</code> (6.0&nbsp;KB), <code>mistral</code> (two files) and <code>solar</code> "
             "(5.4&nbsp;KB) returned files that do not parse at all, which is the hollow marker. "
             "<code>mimo</code>, <code>minimax</code> and <code>qwen</code> parsed cleanly but "
             "carried no verdict key.",
    ),
    "day8": dict(
        title="Blocks called SUSPECT, of 10",
        subtitle="Higher means stricter. All three models passed the seven-key schema on all thirty "
                 "responses, so this chart is not an accuracy ranking: it shows how often each called "
                 "a draft SUSPECT rather than SOUND-WITH-RESERVATIONS.",
        scale_max=100, neutral=True,
        rows=[("deepseek", 90.0, "9/10"), ("sonnet", 40.0, "4/10"), ("kimi", 20.0, "2/10")],
        note="<code>chatgpt</code> is absent: it ran a single pilot block. On this day the three "
             "models tied on the graded metric (30/30 schema), which is why the index chart ranks "
             "them level and this chart shows strictness instead.",
    ),
}


# ============================================================================
# CONTENT
# ============================================================================

INDEX = (
    hero("Free web AI red-team benchmark &middot; eight collection days",
         "Benchmarking free web AI on tasks with checkable answers",
         "Between 31 August and 17 September 2026, a structured prompt was pasted by hand into the free "
         "web chat interface of each service and the reply saved verbatim. Nothing was automated and "
         "nothing was paid for. Every response was then graded, most of it by mechanical recomputation "
         "and the paper-recall slices against the papers themselves.",
         [("663", "raw responses"), ("16", "models in the pool"), ("5", "instruments"),
          ("0", "fatal objections")])
    + section("What this is", "A per-day record",
              '<div class="prose"><p>Each day is a separate page carrying three things: <strong>the prompt</strong> '
              'that was pasted, <strong>what graded it</strong>, and <strong>a table of how every model '
              'performed</strong>. Where a number could be measured from the response files rather than '
              'read out of a summary, it was measured.</p>'
              '<p>The corpus is not expert data and does not pretend to be. No episode invented a chip, '
              'company or person. Each verdict is a flag for a human reviewer.</p></div>'
              + scene_html("index"))
    + section("The eight days", "Choose a day",
              '<div class="tbl-wrap"><table class="compare"><caption>Collection days</caption><thead><tr>'
              '<th>Day</th><th>Date</th><th>Theme</th><th class="num">Files</th><th class="num">Models</th>'
              '<th>Prompt slices</th><th>Graded by</th></tr></thead><tbody>'
              '<tr><td><a href="day1.html" class="teal">Day 1</a></td><td>2026-08-31</td><td>Exploration</td>'
              '<td class="num">236</td><td class="num">24</td><td>19 lettered prompts</td><td>Fable 5</td></tr>'
              '<tr><td><a href="day2.html" class="teal">Day 2</a></td><td>2026-09-01</td><td>Compliance batch</td>'
              '<td class="num">141</td><td class="num">15</td><td>10 regulatory families</td><td>Opus 5</td></tr>'
              '<tr><td><a href="day3.html" class="teal">Day 3</a></td><td>2026-09-03</td><td>Five families</td>'
              '<td class="num">70</td><td class="num">15</td><td>boundary &middot; APRC &middot; POWER4 &middot; diagnosis &middot; SDC</td><td>Opus 5</td></tr>'
              '<tr><td><a href="day4.html" class="teal">Day 4</a></td><td>2026-09-04 &amp; 09-08</td><td>Paper recall</td>'
              '<td class="num">73</td><td class="num">16</td><td>Alpha &middot; Pentium 4 &middot; POWER4 phys &middot; Niagara &middot; LVS</td><td>Opus 5</td></tr>'
              '<tr><td><a href="day5.html" class="teal">Day 5</a></td><td>2026-09-08 &amp; 09-09</td><td>Five instruments</td>'
              '<td class="num">80</td><td class="num">16</td><td>Reg Z &middot; JCS &middot; E &middot; red1 &middot; red3</td><td>Opus 5 + GLM 5.3 Flash</td></tr>'
              '<tr><td><a href="day6.html" class="teal">Day 6</a></td><td>2026-09-11</td><td>Citation + deployment</td>'
              '<td class="num">32</td><td class="num">16</td><td>B-v8 &middot; C-v5</td><td>GLM 5.3 Flash</td></tr>'
              '<tr><td><a href="day7.html" class="teal">Day 7</a></td><td>2026-09-14</td><td>Format drift</td>'
              '<td class="num">31</td><td class="num">15</td><td>JI-v1.1 block 01</td><td>GLM 5.3 Flash</td></tr>'
              '<tr><td><a href="day8.html" class="teal">Day 8</a></td><td>2026-09-17</td><td>The sweep</td>'
              '<td class="num">30</td><td class="num">3</td><td>JI-v1.2, ten blocks</td><td>GLM 5.3 Flash</td></tr>'
              '</tbody></table></div>'
              '<div class="legend">Model counts are names as collected. One model was collected under two '
              'spellings (<code>minara</code> / <code>minaria</code>) and is counted once.</div>')
    + section("Three lessons beyond this corpus", "What the eight days established",
              verdict_pair(
                  "<code>sonnet</code>",
                  "Top tier on six graded days, including 100% on the Day-4 recall slices and 30 of 30 on Day "
                  "8.",
                  "<code>mistral</code>",
                  "Bottom on three separate days: the Day-2 compliance batch, both Day-5 exact tracks, and two "
                  "unparseable Day-7 files.")
              + findings([
                  ("", "Agreement between models did not track correctness",
                   "Three separate cases. <code>deepseek</code> and <code>minimax m3</code> both called the POWER4 "
                   "coherence protocol directory-based, in a paper where &ldquo;snoop&rdquo; appears 39 times and "
                   "the L3 directory is a cache tag directory. <code>gemini</code>, <code>grok</code> and "
                   "<code>kimi</code> each placed a single shared FPU across the eight cores of a paper that never "
                   "uses the word FPU. Ten models agreed the ASIL&nbsp;B SPFM target is 90%, against two public "
                   "sources that disagree at 90 and 97."),
                  ("", "Mechanical recomputation caught one of three failure shapes",
                   "It catches a step that does not reproduce its own output. It does not catch right arithmetic on "
                   "the wrong rule: <code>yuanbao</code>, <code>solar</code>, <code>minimax 2.7</code> and "
                   "<code>mistral</code> all multiply where the IRB grouping requires division, and every one of "
                   "them closes arithmetically on its own inputs. Nor does it catch a different convention, which is "
                   "how <code>mistral</code>&rsquo;s inverted SPFM survived both the S and T slices unchanged."),
                  ("bad", "Delivery failures were misread as reasoning failures",
                   "<code>solar pro</code> returned five blocks where the prompt asked for three episodes. "
                   "<code>yuanbao</code> wrapped its answer in a <code>{\"prompt_a\": ...}</code> object. "
                   "<code>minimax m3</code> lost the <code>\"le_amount\":</code> key mid-object. <code>solar</code> "
                   "answered the Reg&nbsp;Z prompt in prose. Each was recorded as an absence or a format note rather "
                   "than as a wrong answer."),
              ]))
)


DAY1 = (
    hero("Day 1 &middot; Exploration &middot; collected 2026-08-31",
         "The day that mapped the territory",
         "Nineteen prompt slices and twenty-four model names, including <code>nemotron</code>, "
         "<code>opus 5</code> and two spellings of the same GLM build. This was the day that mapped the "
         "territory rather than measuring it.",
         [("236", "files collected"), ("24", "model names"), ("19", "prompt slices"),
          ("39", "A-episodes returned")])
    + section("The prompt", "Nineteen slices sharing one output discipline",
              '<div class="prose"><p>Day&nbsp;1 ran the whole lettered family. Every prompt shared one '
              'discipline: <em>a single bare JSON object or array and nothing else</em>, an explicit honesty '
              'field, and a hard rule that inventing a source or a chip name is the worst possible output.</p></div>'
              + scene_html("day1")
              + prompt_card(
                  "PROMPT-A-EPISODES &middot; A-v5",
                  "31 prompts in the family; this is the exemplar",
                  '<span class="q">You are helping build a research dataset about how senior ASIC physical-design '
                  'engineers actually reason during design closure. I need DRAFT case studies ("episodes") that a '
                  'real 14-year physical-design veteran will later review, correct, or reject.</span>\n\n'
                  '**Output format: a SINGLE bare JSON array and NOTHING else.**\n\n'
                  'Produce exactly 3 episodes, one per scenario:/n'
                  '  1. A routing-congestion crisis on a 28nm block\n'
                  '  2. A timing-closure failure where the violation report\'s SHAPE drove the diagnosis\n'
                  '  3. A timing-budget / SDC-derivation decision at a block boundary\n\n'
                  '...`candidates_considered` (array of \u22653 `{action, rejected_because}` \u2014 rejections matter '
                  'most and must cite a concrete cost) ... `weakest_point` (the single detail most likely wrong).\n\n'
                  '**Hard rules:** No invented chip, company, or person names. No sources you cannot name. '
                  'Boring-and-consistent beats dramatic-and-wrong. An honest skip scores higher than a '
                  'fabricated episode.',
                  "The other eighteen slices: B-v1/v2 browser cells &middot; C-v1 sources &middot; D1-v3 genre map &middot; "
                  "D2 POWER4 extraction &middot; E-v2 calculations &middot; F-v1 diagnosis library &middot; G-v1 SDC patterns &middot; "
                  "H-v1 proving pitfalls &middot; I-v1 review checklists &middot; J episode red-team &middot; K-v1 node deltas &middot; "
                  "L/M/N/O paper recall &middot; P-v1 POWER4 rerun &middot; Q-v1 interview guide &middot; S-v1 calc depth &middot; T-v1 test vectors")
              + '<div class="prose" style="margin-top:1.4rem"><p>The slices present on this day:</p></div>'
              + roster([("A-v1/v2 episodes", "t"), ("B-v1/v2 browser", "t"), ("C-v1 sources", "t"),
                        ("D1-v3 genre map", ""), ("D2 POWER4 extract", ""), ("E-v2 calculations", ""),
                        ("F-v1 diagnosis", ""), ("G-v1 SDC patterns", ""), ("H-v1 pitfalls", ""),
                        ("I-v1 checklists", ""), ("J red-team", "p"), ("K-v1 node deltas", ""),
                        ("L Alpha recall", "g"), ("M Pentium 4 recall", "g"), ("N POWER4 phys recall", "g"),
                        ("O Niagara recall", "g"), ("P-v1 rerun", "g"), ("Q-v1 interview", ""),
                        ("S-v1 calc depth", "p"), ("T-v1 vectors", "p")]))
    + section("What graded it", "Three run logs followed by a corpus-wide digest",
              grader_cards([
                  ("Station", "Fable 5",
                   "Wrote and graded the three collection run logs. Run 1 (A-v1/B-v1, 15 models) and run 2 "
                   "(A-v2/B-v2/C-v1, 15 outputs) and run 3 (D-v1 Task 1, 14 outputs) each carry a per-model tier "
                   "table and a &ldquo;v-next changes&rdquo; section.",
                   "Web Model Tasks/Day 1/LOG-RUN1,2,3-2026-08-31.md"),
                  ("Station", "Opus 5",
                   "Later re-graded the merged corpus: 233 files, 2.34&nbsp;MB, 1,550 JSON items across 18 slices, "
                   "with nineteen no-JSON files salvaged rather than discarded.",
                   "digest/DIGEST-REPORT.md"),
                  ("Method", "Mechanical, where ground truth exists",
                   "Arithmetic was recomputed; the S and T slices were recomputed vector by vector. Prose was "
                   "not scored.",
                   "digest/recall-scorecard.md &sect;2b"),
              ]))
    + section("How each model performed", "Run 1 covered A-v1 and B-v1 across 15 models",
              table("LOG-RUN1 tier table, 2026-08-31",
                    ["Model", "A episodes", "B cells", "Tier", "Note"],
                    [["opus 5", "3", "6", ("T1", "ok"), "Best of run. Realistic macro-channel/NDR detail; weakest_point correctly flags its own implausible 214k&rarr;340 DRC drop"],
                     ["sonnet", "3", "12", ("T1", "ok"), "Self-flags the optimistic spread-improves-timing claim; largest B block"],
                     ["kimi", "3", "5", ("T1", "ok"), "Only model whose congestion fix COSTS timing (WNS &minus;0.05&rarr;&minus;0.06), the realistic direction"],
                     ["glm 5.3", "3", "8", ("T2", "mid"), "Complete, generic"],
                     ["meta", "3", "10", ("T2", "mid"), "Complete, generic"],
                     ["chatgpt", "3", "&mdash;", ("T2", "mid"), "Honest constructed-example tag on ep3"],
                     ["mimo / minimax m3", "3 each", "&mdash;", ("T2", "mid"), "Over-delivered candidate count (fine)"],
                     ["deepseek / gemini / mistral / qwen", "3 each", "&mdash;", ("T2&ndash;T3", "mid"), "Bland composites, thin rejections"],
                     ["solar pro", "5 blocks", "&mdash;", ("T3", "bad"), "Ignored the output format"],
                     ["tencent yunbao", "3", "partial", ("T2", "mid"), "Content fine, format deviation: wrapped in a <code>{\"prompt_a\": ...}</code> object"],
                     ["minimax (free)", "&mdash;", "&mdash;", ("n/a", "dim"), "Quota error, not an output. Retry after reset"]],
                    highlight_col=None)
              + '<div class="legend">Totals: 39 A-episodes, all tagged <code>composite-of-common-practice</code> or '
                '<code>constructed-example</code> and zero <code>recalled-public-case</code>. Honest, but no jackpot. '
                '~41 B-cells with URLs, unverified at the time of the log.</div>'
              + table("LOG-RUN2 (A-v2 / B-v2 / C-v1) and LOG-RUN3 (D-v1) tier lists",
                      ["Run", "T1", "T2", "T3", "n/a"],
                      [["Run 2 &mdash; A/B/C, 15 outputs",
                        "opus (A+B+C, the tracker lead); chatgpt (two IBM papers); sonnet (A+B+C); kimi (A+B); glm 5.3 (A+B)",
                        "mimo, minimax-3 (content fine, wrong shape), yuanbao, qwen, solar pro, gemini, meta",
                        "deepseek, mistral (bland again; two bland runs = deprioritize)",
                        "minimax 2.7 (quota error, 2nd time)"],
                       ["Run 3 &mdash; D-v1 Task 1, 14 outputs",
                        "13 models produced genre maps: 129 entries, 96 unique titles, 82 singletons",
                        "mimo: empty genre_map (format followed, nothing delivered)",
                        "deep-research-report: never received the attachment, produced a 12&nbsp;KB meta-report",
                        "&mdash;"]],
                      highlight_col=None))
    + section("What it found", "What the widest net returned",
              verdict_pair(
                  "<code>opus 5</code>",
                  "Took T1 in both runs, and its <code>weakest_point</code> field predicted the "
                  "reviewer&rsquo;s own attack on the implausible 214k&rarr;340 DRC drop.",
                  "<code>solar pro</code>",
                  "Returned five blocks instead of three episodes and ignored the bare-array rule, the "
                  "day&rsquo;s only outright T3.")
              + findings([
                  ("", "The honesty machinery worked as designed",
                   "<code>opus 5</code>, <code>sonnet</code> and <code>kimi</code> all took T1 and each named its "
                   "own weakest number. <code>opus 5</code> flagged its implausible 214k&rarr;340 DRC drop, the "
                   "first thing a reviewer attacks, and <code>sonnet</code> flagged its optimistic "
                   "spread-improves-timing claim. The pattern held across six graded slices."),
                  ("", "Prompt C worked on its first run",
                   "Three models attempted it. <code>chatgpt</code> named two IBM Journal of R&amp;D papers, POWER4 "
                   "closure at 2002 with confidence 0.94 and z10 at 2008. <code>opus</code> named the OpenROAD, "
                   "OpenLane and LibreLane GitHub issue trackers as public failure-and-recovery archives. "
                   "<code>sonnet</code> named the Bhasker and Chadha STA book at confidence 0.6. The trackers became "
                   "the ten Day-8 red-team blocks."),
                  ("warn", "Format rules broke whenever more than one prompt went into one chat",
                   "The rule held for single-prompt chats. With several prompts in one chat, <code>chatgpt</code> "
                   "folded its source answers into the episode array as a fifth entry, <code>minimax-3</code> "
                   "emitted dictionary blocks instead of arrays, and <code>kimi</code> appended an empty block. Run "
                   "3 fixed it by process, sending one prompt per fresh chat. Harder prompt language had not helped."),
                  ("warn", "minimax 2.7 hit a quota error twice and was graded n/a",
                   "It failed on run 1 and again on run 2, so it was recorded <code>n/a</code> both times and never "
                   "zero. The same distinction between a model that did not answer and one that answered badly "
                   "recurs on Day 5 (<code>solar</code>, PROSE-NOT-JSON), Day 6 (<code>meta</code> and "
                   "<code>solar</code>, unparseable) and Day 7 (0 of 15 schema)."),
              ]))
    + section("Source files", "Where the evidence lives",
              srcs(["Web Model Tasks/Day 1/ (236 entries)", "LOG-RUN1-2026-08-31.md",
                    "LOG-RUN2-2026-08-31.md", "LOG-RUN3-2026-08-31.md",
                    "prompts/PROMPT-A-EPISODES.md", "prompts/PROMPT-C-SOURCES.md",
                    "digest/DIGEST-REPORT.md", "digest/recall-scorecard.md",
                    "Web Model Tasks/RUN-MANIFEST.tsv"]))
)


DAY2 = (
    hero("Day 2 &middot; Compliance batch &middot; collected 2026-09-01",
         "Ten regulatory families graded by mechanical recomputation",
         "The first day with real ground truth. Every shown computation was re-executed independently in "
         "scratch Python, so a verdict here is a recomputation.",
         [("141", "files collected"), ("15", "models"), ("10", "prompt families"),
          ("~720", "computations recomputed")])
    + section("The prompt", "Eight C1 families and two C2 slices",
              '<div class="prose"><p>Each prompt pinned one regulatory instrument by its exact citation, '
              'supplied the load-bearing rule, and asked for worked cases with a <code>weakest_point</code>. '
              'Several prompts were built specifically to expose the place implementations err.</p></div>'
              + scene_html("day2")
              + prompt_card(
                  "PROMPT-C1-TRID-CASES &middot; C1-TRID-v1",
                  "one of ten Day-2 prompts",
                  '<span class="q">This task is about the <b>TRID fee-tolerance rules \u2014 12 CFR \u00a71026.19(e)(3)</b> '
                  '\u2014 the zero-tolerance, 10%-aggregate-tolerance, and no-tolerance-limit buckets for comparing '
                  'Loan Estimate to Closing Disclosure charges.</span>\n\n'
                  'Produce up to 5 worked tolerance-test cases, each with a fee table (LE amount vs CD amount per '
                  'fee, bucket assignment per the rule) \u2014 and <b>at least 2 cases MUST have mixed directions inside '
                  'the 10% bucket</b> (some fees increased, some decreased), because the 10% test compares AGGREGATE '
                  'to AGGREGATE and mixed-direction cases are where implementations get it wrong.\n\n'
                  '...`computation`: step by step \u2014 per-bucket sums, the 10% threshold (\u03a3le \u00d7 0.10), the '
                  'aggregate comparison (\u03a3cd vs \u03a3le, NOT the sum of increases) ... `weakest_point`\n\n'
                  '<b>Hard rules:</b> the load-bearing rule is aggregate-vs-aggregate for the 10% bucket \u2014 a case '
                  'that computes the sum-of-increases instead is itself the defect this suite exists to catch.',
                  "The full Day-2 set: C1-APPJ-EXAMPLES &middot; C1-CCD2-APRC &middot; C1-FRTB-ES &middot; "
                  "C1-GLOBE-EXAMPLES &middot; C1-IRB-EXAMPLES &middot; C1-MICA-RESERVE &middot; C1-OFAC-GRAPHS &middot; "
                  "C1-TRID-CASES &middot; C2-JCS-EDGES &middot; C2-RECEIPT-ANATOMY")
              + '<div class="prose" style="margin-top:1.4rem"><p>Families and the rule each one turns on:</p></div>'
              + roster([("TRID &mdash; aggregate vs sum-of-increases", "t"), ("OFAC &mdash; attribution vs multiplication", "t"),
                        ("GLOBE &mdash; rate-year pairing", "t"), ("APPJ &mdash; actuarial equation", "t"),
                        ("IRB &mdash; CRE31 grouping", "g"), ("FRTB &mdash; ES multipliers", "g"),
                        ("MiCA &mdash; reserve composition", "g"), ("CCD2 &mdash; APRC", "g"),
                        ("JCS &mdash; RFC 8785", "p"), ("Receipt &mdash; risc0 anatomy", "p")]))
    + section("What graded it", "Two mechanical adjudication passes",
              grader_cards([
                  ("Station", "Opus 5",
                   "First batch: 55 JSONs, 14 models &times; 4 prompts (GLOBE, APPJ, TRID, OFAC). Every shown "
                   "computation re-executed independently in scratch Python. Verdicts are mechanical, not judgment.",
                   "digest/day2-c1-adjudication.md"),
                  ("Station", "Opus 5",
                   "Second batch: 86 files, 15 models &times; 6 prompts (IRB, FRTB, MiCA, CCD2, RECEIPT, JCS), plus "
                   "two Solar cross-adds. CRE31 closed form with <code>statistics.NormalDist</code>; a bisection "
                   "APRC solver; a scratch RFC 8785 canonicalizer self-tested against the RFC's own number vectors.",
                   "digest/day2-c1b-c2-adjudication.md"),
                  ("Vocabulary", "Five verdicts, two of them added",
                   "VERIFIED / WRONG-INPUT / SELF-INCONSISTENT were given. Two more were unavoidable and are "
                   "labelled as such: WRONG-RULE (arithmetic exact, rule misapplied) and INDETERMINATE.",
                   "&sect;2 of both adjudications"),
              ]))
    + section("How each model performed", "The first class-1 arithmetic batch across four families",
              table("Per-model Class-1 verdict, first batch",
                    ["Model", "Verified", "Self-inconsistent", "Wrong-input", "Wrong-rule", "Anti-reversal", "Class-1 verdict"],
                    [["chatgpt", "15/15", "0", "0", "0", "0", ("EXEMPLARY", "ok"), "APPJ rates match independent bisection to 1e-10 across four code paths; 5/5 GLOBE examples close. One wrong-content file (OFAC = its TRID), not assessable"],
                     ["kimi", "20/20", "0", "0", "0", "0", ("EXEMPLARY", "ok"), "Clean on all four prompts; reproduces both published APPJ anchors"],
                     ["grok", "20/20", "0", "0", "0", "0", ("EXEMPLARY", "ok"), "Both APPJ anchors, full-attribution OFAC"],
                     ["meta", "18/18", "0", "0", "0", "0", ("EXCELLENT", "ok"), "Honestly labels all APPJ cases as constructed"],
                     ["qwen", "19/19", "0", "0", "0", "0", ("EXCELLENT", "ok"), "Contributes the sharpest TRID discriminator (+400/&minus;400, aggregate zero)"],
                     ["sonnet", "18/18", "0", "0", "0", "0", ("EXCELLENT", "ok"), "The only 47% near-miss OFAC vector"],
                     ["minimax 2.7", "19/19", "0", "0", "0", "0", ("EXCELLENT", "ok"), "See the reinstatement below"],
                     ["yuanbao", "19/20", "0", "0", "0", ("1", "bad"), ("STRONG", "ok"), "Form 1 and Form 3 closed forms verify exactly; one TRID case titled &ldquo;aggregate passes&rdquo; while its own verdict is a violation"],
                     ["glm 5.3 flash", "14/14", "0", ("1 (GLOBE rate year)", "bad"), "0", "0", ("STRONG", "ok"), "Best OFAC gate case in the batch; its <code>trid</code> file is absent"],
                     ["mimo", "19/20", ("1 (OFAC)", "bad"), "0", "0", "0", ("GOOD", "ok"), "Produced parseable JSON for the first time in the collection"],
                     ["gemini", "15/16", "0", "0", ("1 (OFAC multiplicative)", "bad"), "0", ("GOOD &mdash; with a rule defect", "mid"), "Arithmetic exact, legal treatment wrong on the one case the prompt was built to expose"],
                     ["deepseek", "18/20", ("1 (TRID)", "bad"), ("1 (GLOBE rate pair)", "bad"), "0", "0", ("MIXED", "mid"), "Substituted its own inputs mid-computation to manufacture a violation"],
                     ["mistral", "17/20", ("3 (OFAC)", "bad"), "0", "0", "0", ("MIXED", "mid"), "Correct attribution arithmetic; blocked-entity verdicts omit the intermediaries"],
                     ["minimax m3", "3/3 recovered", "0", "0", "0", "0", ("NOT ASSESSABLE", "dim"), "Token dropout in 3 of 4 files"]],
                    highlight_col=None)
              + table("Class-1 arithmetic, second batch: IRB, FRTB, MICA, CCD2, RECEIPT, JCS",
                      ["Model", "IRB", "FRTB", "MICA", "CCD2", "JCS", "Batch-2 verdict"],
                      [["chatgpt", "4/4", "&#10003;", "&#10003;", "4/4", "10/11", ("EXEMPLARY", "ok"), "IRB to 15 s.f.; JCS recovered only by salvage &mdash; its inner quotes were unescaped"],
                       ["kimi", "4/4", "&#10003;", "&#10003;", "absent", "12/12", ("EXEMPLARY", "ok"), "The only model that <em>derives</em> its Basel benchmark (CRE99.2 at LGD 40%, scaled) rather than asserting one; flawless canonicalizer"],
                       ["sonnet", "4/4", "&#10003;", "&#10003;", "4/4 + 1 honest UNKNOWN", "12/12", ("EXEMPLARY", "ok"), "Declines to assert an APRC it cannot close; joint-best JCS"],
                       ["meta", "4/4", "&#10003;", "&#10003;", "&#10003;", "10/10", ("EXEMPLARY", "ok"), "The only receipt file with source-level detail &mdash; domain-separator tags, 4-byte selector, 128-bit claim-digest split"],
                       ["grok", "4/4", "&#10003;", "&#10003;", "5/5", "10/11", ("EXCELLENT", "ok"), "One escaping-form miss only"],
                       ["qwen", "4/4", "&#10003;", "&#10003; (4 UNKNOWN flags)", "5/5", "9/10", ("EXCELLENT", "ok"), "Its MiCA flags sit on the one figure now marked NEEDS-RETRIEVAL"],
                       ["mimo", "absent", "&#10003;", "&#10003;", "5/5", "9/11", ("STRONG", "ok"), "Second consecutive batch of parseable, correct output"],
                       ["glm 5.3 flash", "&ndash;", "&ndash;", "&ndash;", "&ndash;", "9/11", ("INSUFFICIENT DATA", "dim"), "2 of 6 files. One anti-reversal instance"],
                       ["yuanbao", ("WRONG-RULE 4/4", "bad"), "&#10003;", "&#10003;", "5/5", "9/11", ("SPLIT", "mid"), "Exact on APRC, wrong grouping on CRE31"],
                       ["deepseek", "4/4", "&#10003;", "&#10003;", ("SELF-INCONSISTENT 3", "bad"), ("13/15, 1 WRONG-RULE", "mid"), ("MIXED", "mid"), "The batch&rsquo;s only UTF-16 key-order failure; APRCs disconnected from its own schedules"],
                       ["gemini", ("3/4, 1 SELF-INCONSISTENT", "bad"), "&#10003;", "&#10003;", ("SELF-INCONSISTENT 3", "bad"), "6/8", ("MIXED", "mid"), "Nominal rate reported as APRC; fabricated a benchmark that confirms its own error"],
                       ["solar", ("WRONG-RULE 4/4", "bad"), "&#10003;", "&#10003;", "1/1", "17/19", ("SPLIT", "mid"), "Best JCS volume in the batch, worst IRB formula"],
                       ["minimax 2.7", ("WRONG-RULE 4/4 + WRONG-INPUT", "bad"), "&#10003;", "&#10003;", ("WRONG-RULE 2", "bad"), "5/10", ("WEAK &mdash; but self-flagged", "mid"), "Four independent IRB defects, each correctly reported as not matching benchmark"],
                       ["minimax m3", ("SELF-INCONSISTENT", "bad"), "&#10003;", "&#10003;", ("SELF-INCONSISTENT 3", "bad"), "6/9", ("WEAK", "bad"), "Fabricated a BCBS table citation to explain away its own arithmetic"],
                       ["mistral", ("WRONG-RULE 4/4", "bad"), "&#10003;", "&#10003;", ("WRONG-RULE + SELF-INCONSISTENT 3", "bad"), ("3/11", "bad"), ("BOTTOM", "bad"), "Weakest on arithmetic, rules and output integrity simultaneously"]],
                      highlight_col=None)
              + table("JCS &mdash; RFC 8785 canonicalization, exact scores",
                      ["Model", "OK", "Form", "Wrong", "Score", "Note"],
                      [["solar", "17", "2", "0", ("17/19", "ok"), "Largest set (21 vectors); both misses are escaping form"],
                       ["deepseek", "13", "0", ("2", "bad"), ("13/15", "ok"), "The only key-order failure in the batch"],
                       ["kimi", "12", "0", "0", ("12/12", "ok"), "Flawless"],
                       ["sonnet", "12", "0", "0", ("12/12", "ok"), "Flawless"],
                       ["chatgpt", "10", "1", "0", ("10/11", "ok"), "Recovered only by salvage"],
                       ["grok", "10", "1", "0", ("10/11", "ok"), ""],
                       ["meta", "10", "0", "0", ("10/10", "ok"), "One vector has an empty <code>input_json</code>; its stated output for it is correct"],
                       ["mimo", "9", "2", "0", ("9/11", "ok"), ""],
                       ["yuanbao", "9", "2", "0", ("9/11", "ok"), ""],
                       ["qwen", "9", "0", ("1", "bad"), ("9/10", "ok"), "<code>-0</code> preserved"],
                       ["glm 5.3 flash", "9", "0", ("2", "bad"), ("9/11", "ok"), ""],
                       ["gemini", "6", "2", "0", ("6/8", "mid"), ""],
                       ["minimax m3", "6", "0", ("3", "bad"), ("6/9", "mid"), "2 vectors have malformed <code>input_json</code>"],
                       ["minimax 2.7", "5", "2", ("3", "bad"), ("5/10", "mid"), ""],
                       ["mistral", "3", "2", ("6", "bad"), ("3/11", "bad"), "Six substantive failures spanning every rule family"]],
                      highlight_col=4))
    + section("What it found", "Three defect classes the vocabulary could not name",
              verdict_pair(
                  "<code>kimi</code>",
                  "Verified 20 of 20 first-batch claims, scored 12 of 12 on JCS, and was the only model to "
                  "derive the canonicalization rule.",
                  "<code>mistral</code>",
                  "Came bottom: six substantive JCS failures, WRONG-RULE on every IRB entry, and the "
                  "batch&rsquo;s weakest arithmetic.")
              + findings([
                  ("", "Arithmetic correctness and rule correctness are independent failure modes",
                   "<code>gemini</code> gets the OFAC arithmetic exactly right and applies the US multiplicative "
                   "treatment where the EU attribution test applies, on the one case the prompt was built to expose. "
                   "<code>grok</code> is 20/20 on Class-1 and invents an EAR band elsewhere. Both close "
                   "arithmetically, so a recomputation gate passes both."),
                  ("warn", "The IRB grouping error appeared in four models under four different spellings",
                   "<code>yuanbao</code> multiplies where the grouping requires division. <code>solar</code> omits "
                   "the /&radic;(1&minus;R) term entirely. <code>minimax 2.7</code> multiplies and carries three "
                   "further defects. <code>mistral</code> drops the /(1&minus;1.5b) divisor from the formula itself. "
                   "Four spellings of one structural error, and all four close on their own inputs."),
                  ("warn", "Most honesty labels were real and 15% were boilerplate",
                   "<code>weakest_point</code> was populated on 55 of 55 files and on every item. About 40% name the "
                   "true fault line: <code>gemini</code>&rsquo;s OFAC entry names the exact axis on which it is "
                   "wrong, and <code>deepseek</code> flags the rate year that is the wrong constant. About 45% are "
                   "real but secondary and 15% are boilerplate. It still missed the one defect that mattered, "
                   "<code>deepseek</code>&rsquo;s TRID case 2, which does not mention its own input substitution."),
                  ("bad", "minimax m3 dropped a JSON key mid-structure",
                   "In 3 of its 4 files <code>minimax m3</code> loses a key mid-object: <code>trid: {\"name\": "
                   "&hellip;, \"bucket\": \"ten_pct_aggregate\", 500.00, \"cd_amount\": 350.00}</code>, where the "
                   "<code>\"le_amount\":</code> key has vanished. Recorded as damaged delivery rather than as a wrong "
                   "answer, and the three recoverable entries were graded."),
              ]))
    + section("Source files", "Where the evidence lives",
              srcs(["Web Model Tasks/Day 2/ (141 entries)", "digest/day2-c1-adjudication.md",
                    "digest/day2-c1b-c2-adjudication.md", "digest/recall-scorecard.md &sect;2c&ndash;2d",
                    "prompts/PROMPT-C1-*.md (8)", "prompts/PROMPT-C2-*.md (2)",
                    "Web Model Tasks/RUN-MANIFEST.tsv"]))
)


DAY3 = (
    hero("Day 3 &middot; Five families &middot; collected 2026-09-03",
         "Boundary inclusivity and the paper that reverses it",
         "Five unrelated prompts in one batch: a boundary-inclusivity verdict table graded against operative "
         "regulatory text, an APRC re-run, the POWER4 recall slice, a differential-diagnosis library and an "
         "SDC-derivation catalogue.",
         [("70", "files collected"), ("15", "models"), ("5", "prompt families"),
          ("13", "models on the boundary table")])
    + section("The prompt", "Closed-form verdicts graded mechanically",
              '<div class="prose"><p>The boundary prompt is the sharpest instrument in the corpus: every answer '
              'is a closed-form verdict against text the estate already holds, so the grader is a string match '
              'against a retrieval-level ground truth rather than a judgment.</p></div>'
              + scene_html("day3")
              + prompt_card(
                  "C1-BOUNDARY-VERDICTS &middot; C1-BOUNDARY-v2",
                  "rule 6 transition-rate premise corrected per CS-68",
                  '<span class="q"># Task: boundary-inclusivity verdict tables for regulatory comparators</span>\n\n'
                  'Every answer is a closed-form verdict graded mechanically against operative regulatory text we '
                  'hold. Show reasoning per cell; honesty labels taken at face value.\n\n'
                  'For each rule below, produce a verdict table for the inputs listed: does the trigger/test FIRE '
                  '(or PASS) at exactly the boundary value, just below, and just above? State the operative '
                  "phrase's inclusivity (strict vs inclusive) that drives each verdict.\n\n"
                  '  1. HOEPA prepayment-penalty trigger \u2014 "can exceed, in total, more than 2 percent"  \u2192 1.99 / 2.00 / 2.01\n'
                  '  2. HOEPA duration trigger \u2014 "more than 36 months"                              \u2192 35 / 36 / 37\n'
                  '  3. Higher-priced covered transaction \u2014 "by 1.5 or more percentage points"       \u2192 1.49 / 1.50 / 1.51\n'
                  '  4. General QM price limit \u2014 "does not exceed \u2026 by 2.25 or more"              \u2192 2.24 / 2.25 / 2.26\n'
                  '  5. GloBE de-minimis \u2014 "less than EUR 10 million" AND "less than EUR 1 million"\n'
                  '  6. Transitional CbCR safe harbour simplified ETR \u2014 "equal to or greater than" the transition rate\n'
                  '  7. Solvency II Tier 1 floor \u2014 "at least equal to" 50% of SCR\n'
                  '  8. NIS2 significant incident (users leg)\n\n'
                  '**Output:** bare JSON only: one object per rule plus `{"weakest_point": "..."}`.',
                  "The other four: C1-CCD2-APRC &middot; D2-POWER4-RECALL &middot; F-DIAGNOSIS-LIBRARY (6 failure "
                  "classes) &middot; G-SDC-PATTERNS (up to 10 derivation patterns)")
              + roster([("boundary inclusivity", "t"), ("CCD2 APRC", ""), ("POWER4 recall (D2)", "g"),
                        ("F &mdash; diagnosis library", "p"), ("G &mdash; SDC patterns", "p")]))
    + section("What graded it", "Ground truth retrieved from the operative text",
              grader_cards([
                  ("Station", "Opus 5",
                   "Built a ground-truth table for all eight rules from primary sources: law.cornell for "
                   "Reg Z, the CFPB and Federal Register for the QM limit, OECD/EU for GloBE, EIOPA for Solvency II. "
                   "All retrieval-level, 2026-09-04, zero memory-level.",
                   "BOUNDARY-GRADING-1-REPORT.md &sect;1"),
                  ("Method", "Three verdicts per cell",
                   "V = VERIFIED, W = WRONG-RULE, S = SELF-INCONSISTENT. Rule 8 was indeterminate for every model: "
                   "no users-leg phrase exists, the thresholds are sector-specific, and Art 23(3) is qualitative.",
                   "BOUNDARY-GRADING-1-REPORT.md &sect;2"),
                  ("Note", "A prompt premise was wrong, and the grading says so",
                   "Rule 6's premise flagged 16%-for-2026 as wrong: the actual transition rate is 17%, "
                   "confirmed across three sources. The ground-truth table records the flag rather than silently "
                   "grading against the prompt.",
                   "BOUNDARY-GRADING-1-REPORT.md &sect;1 row 6"),
              ]))
    + section("How each model performed", "Boundary verdict matrix for rules 1&ndash;7",
              table("V = VERIFIED &middot; W = WRONG-RULE (at the boundary) &middot; S = SELF-INCONSISTENT (label or vocabulary) &middot; Rule 8 INDETERMINATE for all 13",
                    ["Model", "R1", "R2", "R3", "R4", "R5", "R6", "R7", "Score"],
                    [["deepseek", "V", "V", "V", "V", "V", "V", "V", ("7", "ok")],
                     ["glm 5.3 flash", "V", "V", "V", "V", "V", "V", "V", ("7", "ok")],
                     ["grok", "V", "V", "V", "V", "V", "V", "V", ("7", "ok")],
                     ["meta", "V", "V", "V", "V", "V", "V", "V", ("7", "ok")],
                     ["mimo", "V", "V", "V", "V", "V", "V", "V", ("7", "ok")],
                     ["qwen", "V", "V", "V", "V", "V", "V", "V", ("7", "ok")],
                     ["minimax 2.7", "V", "V", "V", ("V+S", "mid"), "V", "V", "V", ("6+S", "mid")],
                     ["kimi", "V", "V", "V", ("V+S", "mid"), "V", "V", "V", ("6+S", "mid")],
                     ["yuanbao", "V", "V", "V", ("V+S", "mid"), "V", "V", "V", ("6+S", "mid")],
                     ["chatgpt", "V", "V", "V", ("W", "bad"), "V", ("V&#9733;", "mid"), "V", ("6", "mid")],
                     ["gemini", "V", "V", "V", ("W", "bad"), "V", "V", "V", ("6", "mid")],
                     ["mistral", "V", "V", "V", ("W", "bad"), ("S", "bad"), "V", "V", ("5+S", "mid")],
                     ["minimax m3", "V", "V", ("INDET", "dim"), ("W", "bad"), "V", "V", "V", ("5+I", "mid")]],
                    highlight_col=None)
              + '<div class="legend">Rule 4, the general QM price limit, is the discriminator: four '
                'models apply the wrong boundary semantics. <code>chatgpt</code>&rsquo;s &#9733; on R6 marks the one '
                'model that caught the prompt&rsquo;s own wrong premise. Six models are perfect on all seven '
                'gradable rules.</div>'
              + table("The POWER4 recall slice (D2): the paper that reverses",
                      ["Slice", "Entries", "Confirmed", "Partial", "Not-in-paper", "Contradicted", "Inversions"],
                      [["D2 POWER4 microarchitecture", "37", "62%", "14%", "5%", ("19%", "bad"), ("3", "bad")],
                       ["All six recall slices", "309", "74%", "10%", "12%", ("4%", "mid"), ("3", "mid")]],
                      highlight_col=None)
              + '<div class="legend">Every central-decision inversion in the whole collection landed on this one '
                'paper. The three models that reversed a decision: <code>chatgpt</code> '
                '(&ldquo;balanced design rather than maximizing clock speed&rdquo;), <code>minimax 2.7</code> '
                '(&ldquo;moderate frequency rather than maximum&rdquo;) and <code>minimax m3</code> '
                '(&ldquo;modest clock-frequency target&rdquo;). The confound (did the warning or the paper '
                'cause it?) was settled by a controlled rerun on Day&nbsp;1&rsquo;s P slice.</div>')
    + section("What it found", "Six failure classes and thirteen patterns",
              verdict_pair(
                  "<code>deepseek</code>",
                  "One of six models at a clean 7/7 on the boundary rules, and the only one to name the source "
                  "of its SDC number.",
                  "<code>minimax m3</code>",
                  "The only model to leave a rule indeterminate and get rule 4 wrong, and it inverted a POWER4 "
                  "central decision.")
              + findings([
                  ("", "The diagnosis library holds 6 classes and 64 candidate causes",
                   "Congestion, setup, hold and IR-drop carry 10 causes each; CTS and DRC carry 12. Every entry "
                   "states the report or experiment that rules the cause out, its check cost and the fix. The "
                   "consensus first prior for congestion is macro placement creating narrow channels, offered by all "
                   "nine models, and for hold failures it is adverse clock skew."),
                  ("warn", "The first demonstration that agreement is not evidence",
                   "<code>deepseek</code> and <code>minimax m3</code> both asserted directory-based coherence, "
                   "dismissing snoopy protocols as unscalable, for a design whose paper uses snoop-based coherence "
                   "and where &ldquo;snoop&rdquo; appears 39 times. Ten models agreed the ASIL&nbsp;B SPFM target is "
                   "90% while two public sources disagree at 90 and 97 and the normative value is paywalled."),
                  ("", "The SDC catalogue turned up the one honest provenance",
                   "Of the seven over-constraint patterns, <code>deepseek</code> was the only model to name where "
                   "its number came from: &ldquo;typical 15% degradation synthesis&rarr;post-route on this node, "
                   "from previous tapeouts&rdquo;. <code>yuanbao</code> was the only model to refuse relaxing "
                   "guardband to zero."),
                  ("warn", "One model&rsquo;s boundary failure was a vocabulary failure",
                   "<code>mistral</code>&rsquo;s S on rule 5 is a self-inconsistency in its own stated label, not a "
                   "wrong verdict, which is why the codebook needed a fourth code. Rule 4 is the real discriminator: "
                   "<code>chatgpt</code>, <code>gemini</code>, <code>mistral</code> and <code>minimax m3</code> all "
                   "apply the wrong boundary semantics, while <code>chatgpt</code> alone caught the prompt&rsquo;s "
                   "own wrong 16% premise on rule 6."),
              ]))
    + section("Source files", "Where the evidence lives",
              srcs(["Web Model Tasks/Day 3/ (70 entries)", "BOUNDARY-GRADING-1-REPORT.md",
                    "digest/diagnosis-library.md", "digest/sdc-patterns.md",
                    "digest/recall-scorecard.md &sect;1", "digest/anti-reversal-experiment.md",
                    "prompts/C1-BOUNDARY-VERDICTS.md", "prompts/PROMPT-F-DIAGNOSIS-LIBRARY.md",
                    "prompts/PROMPT-G-SDC-PATTERNS.md"]))
)


DAY4 = (
    hero("Day 4 &middot; Paper recall &middot; collected 2026-09-04 and 2026-09-08",
         "The only place output is scored against ground truth",
         "Four papers reconstructed from memory, each graded against a locator-cited extraction set and the "
         "full PDF text. This is the only slice in the collection where a model is scored against the source "
         "rather than against another model.",
         [("73", "files collected"), ("16", "models"), ("216", "graded claims"),
          ("5", "prompts")])
    + section("The prompt", "One paper named by its exact citation",
              '<div class="prose"><p>Each prompt named one paper by its full citation, forbade general knowledge '
              'from standing in for paper content, and made a <em>direction</em> error the single worst possible '
              'output. Every entry had to carry its own <code>weakest_point</code>.</p></div>'
              + scene_html("day4")
              + prompt_card(
                  "D2-ALPHA21264-RECALL &middot; L-v2",
                  "v1 plus the D2-v5 field set",
                  '<span class="q">This task is about one specific published paper: <b>"The Alpha 21264 '
                  'Microprocessor" \u2014 R. E. Kessler \u2014 IEEE Micro, Vol. 19, No. 2, March\u2013April 1999, '
                  'pp. 24\u201336.</b></span>\n\n'
                  'From your knowledge of THIS SPECIFIC PAPER (not your general knowledge of the Alpha 21264 or DEC), '
                  'reconstruct up to 5 engineering-decision episodes that the paper itself describes \u2014 design '
                  'choices weighed, alternatives considered or rejected, trade-offs made and their stated reasoning.\n\n'
                  '...`quote_as_recalled`: the single most load-bearing sentence AS YOU RECALL IT WORD-FOR-WORD '
                  '(max 25 words; if you cannot reproduce it verbatim, write "cannot-reproduce-verbatim" instead of '
                  'approximating) ... `not_in_paper`: true ONLY if you believe the entry\'s claim is NOT actually in '
                  'this paper ... `paper_vs_general` ... `weakest_point`\n\n'
                  '<b>Hard rules:</b> say-not-know beats guess \u2014 "not-stated-in-paper", '
                  '"cannot-reproduce-verbatim", `not_in_paper`: true, and `[]` are all HONEST outputs that score '
                  'better than any confident fabrication. <b>REVERSING a decision the paper actually made \u2014 '
                  'claiming it chose X when it chose the opposite \u2014 is the single worst possible output.</b>',
                  "The five papers: Alpha 21264 (IEEE Micro 1999) &middot; Pentium 4 (Intel Technology Journal 2001) &middot; "
                  "POWER4 circuit &amp; physical design (IBM JRD 46(1)) &middot; Niagara (IEEE Micro 2005) &middot; "
                  "plus F-LVS-MISMATCH-CLASSES")
              + roster([("L &mdash; Alpha 21264", "g"), ("M &mdash; Pentium 4", "g"),
                        ("N &mdash; POWER4 physical", "g"), ("O &mdash; Niagara", "g"),
                        ("F &mdash; LVS mismatch classes", "p")]))
    + section("What graded it", "Extractions before the PDFs",
              grader_cards([
                  ("Station", "Opus 5",
                   "Graded against five locator-cited extraction sets and the full text of the five PDFs. M and N "
                   "were graded by keyword-anchored spot-check rather than full read; that caveat is stated in the "
                   "scorecard itself.",
                   "digest/recall-scorecard.md"),
                  ("Ground truth", "36 extracted episodes",
                   "Locator-cited extractions from all five papers: POWER4-circuit-physical 8, POWER4-microarch 8, "
                   "Alpha 21264 7, Pentium 4 7, Niagara 6, every entry carrying a section-or-page locator, a "
                   "direct quote and non-empty gaps.",
                   "extractions/*.episodes.json"),
                  ("Note", "Five papers were acquired and verified",
                   "All five consensus sources on disk with verified citations and public URLs, including the "
                   "openly-archived Intel Technology Journal and a bitsavers IBM JRD mirror.",
                   "VERIFIED-SOURCES.md"),
              ]))
    + section("How each model performed", "Per-slice results for the four Day-4 papers",
              table("Recall adjudication by slice",
                    ["Slice", "Paper", "Entries", "Confirmed", "Partial", "Not-in-paper", "Contradicted", "Inversions"],
                    [["L", "Kessler, <em>The Alpha 21264 Microprocessor</em> &middot; IEEE Micro 1999", "57", "72%", "16%", "7%", "5%", ("0", "ok")],
                     ["M", "Hinton et al., <em>The Microarchitecture of the Pentium 4 Processor</em> &middot; ITJ 2001", "52", "81%", "10%", "10%", ("0", "ok")],
                     ["N", "Warnock et al., <em>The circuit and physical design of the POWER4 microprocessor</em>", "48", "75%", "8%", "17%", ("0", "ok")],
                     ["O", "Kongetira et al., <em>Niagara: A 32-Way Multithreaded SPARC Processor</em>", "59", "80%", "3%", "17%", ("0", "ok")]],
                    highlight_col=3)
              + '<div class="legend">All four carry an explicit anti-reversal warning in the prompt. Zero inversions '
                'across all 216 claims, against three inversions on the warning-less POWER4 slice. '
                'Contradiction is near-zero on every slice; the losses are NOT-IN-PAPER, i.e. general knowledge '
                'dressed as paper content.</div>'
              + table("Per-model recall across all six slices; the L/M/N/O models are the Day-4 set",
                      ["Model", "Entries", "Confirmed", "Conf. rate", "Part", "NIP", "Contra", "Inv.", "Slices"],
                      [["meta", "25", "25", ("100%", "ok"), "0", "0", "0", "0", "all 5"],
                       ["qwen", "14", "14", ("100%", "ok"), "0", "0", "0", "0", "L M N O"],
                       ["sonnet", "12", "12", ("100%", "ok"), "0", "0", "0", "0", "L M N O"],
                       ["grok", "25", "23", ("92%", "ok"), "1", "1", "0", "0", "all 5"],
                       ["chatgpt", "25", "23", ("92%", "ok"), "0", "1", ("1", "bad"), ("1", "bad"), "all 5"],
                       ["yuanbao", "24", "22", ("92%", "ok"), "1", "0", ("1", "bad"), ("1", "bad"), "all 5"],
                       ["gemini", "16", "14", ("88%", "mid"), "1", "1", "0", "0", "L M N O"],
                       ["kimi", "19", "15", ("79%", "mid"), "2", "1", ("1", "bad"), ("1", "bad"), "L M N O"],
                       ["deepseek", "25", "20", ("80%", "mid"), "2", "2", ("1", "bad"), ("1", "bad"), "all 5"],
                       ["mimo (prose)", "8", "5", ("63%", "mid"), "1", "1", ("1", "bad"), ("1", "bad"), "D2 L only"],
                       ["minimax m3", "16", "6", ("38%", "bad"), "6", "1", ("3", "bad"), ("3", "bad"), "D2 L M O"],
                       ["minimax 2.7", "24", "9", ("38%", "bad"), "8", "5", ("2", "bad"), ("2", "bad"), "all 5"],
                       ["glm 5.3 flash", "20", "2", ("10%", "bad"), "2", ("16", "bad"), "0", "0", "L M N O"]],
                      highlight_col=3))
    + section("What it found", "Where recall separates models and where it misleads",
              verdict_pair(
                  "<code>meta</code>",
                  "Confirmed 25 of 25 claims across all five slices, a 100% rate with no partials, no "
                  "contradictions and no inversions.",
                  "<code>glm 5.3 flash</code>",
                  "Confirmed only 2 of 20 entries, with 16 claims not in the paper at all, the weakest recall "
                  "of the day.")
              + findings([
                  ("", "A model can be 100% on recall and fabricate a formula",
                   "<code>qwen</code> confirmed 14 of 14 recall entries and then scored 2 of 3 SPFM vectors on a "
                   "fabricated formula. <code>meta</code> is the only model strong at both: 25 of 25 on recall and 4 "
                   "of 4 on the canonicalizer. The two competencies rank the field differently."),
                  ("bad", "glm 5.3 flash submitted the same Alpha 21264 text for eight different prompts",
                   "Slices M, N, O, P, Q, S and T, plus its own L: eight prompts, one answer. The JSON is well "
                   "formed, the schema valid and the honesty fields populated, and the content belongs to a "
                   "different paper. No schema check in the pipeline can see this. Only reading the answer against "
                   "the target finds it."),
                  ("", "grok recalled POWER4&rsquo;s circuit constraints at circuit-designer resolution",
                   "The one-third-cycle global slew limit and the late-binding low-V<sub>t</sub> swap, both "
                   "reproduced verbatim. <code>grok</code> scored 23 of 25 confirmed across all five slices, the "
                   "best recall in the collection on the paper closest to the domain."),
                  ("warn", "The losses are NOT-IN-PAPER claims and none is a contradiction",
                   "About 12% of the 216 graded claims sit outside the paper by the model&rsquo;s own label, and "
                   "only three contradictions appear across all four slices, all of them on the Alpha&nbsp;21264. "
                   "The honesty field <code>paper_vs_general</code> is informative but weak: entries the model "
                   "marked <code>from-general-knowledge</code> are still 70% confirmed."),
              ]))
    + section("Source files", "Where the evidence lives",
              srcs(["Web Model Tasks/Day 4/ (73 entries)", "digest/recall-scorecard.md",
                    "digest/source-candidates.md", "digest/node-era-deltas.md",
                    "extractions/*.episodes.json (36 episodes)", "VERIFIED-SOURCES.md",
                    "sources/ (5 PDFs)", "prompts/D2-*-RECALL.md", "prompts/F-LVS-MISMATCH-CLASSES.md"]))
)


DAY5 = (
    hero("Day 5 &middot; Five instruments &middot; collected 2026-09-08 and 2026-09-09",
         "Sixteen models on five mechanically gradable instruments",
         "The richest onboarding wave in the collection, and the first with two grading stations. Every "
         "instrument on this day is gradable without reading prose, which is what makes the per-model "
         "feed below possible.",
         [("80", "files collected"), ("16", "models"), ("5", "instruments"),
          ("2", "grading stations")])
    + section("The prompt", "Exact recomputation and specification conformance",
              '<div class="prose"><p>The Reg&nbsp;Z prompt is the one track in the corpus where a wrong answer '
              'cannot be argued into a right one: a value is present at six decimal places, or the answer '
              'is wrong. The JCS '
              'prompt asks for exact canonical byte strings, diffed against a reference canonicalizer.</p></div>'
              + scene_html("day5")
              + prompt_card(
                  "C1-REGZ-FACTOR &middot; inflation-indexed threshold derivation",
                  "one of five Day-5 prompts",
                  '<span class="q"># Task: derive and verify inflation-indexed regulatory threshold tables</span>\n\n'
                  'You are given verified official values. Every computation must be shown step by step; all '
                  'arithmetic will be recomputed mechanically, and every honesty label is taken at face value.\n\n'
                  '<b>Given (official, verified):</b> US Regulation Z qualified-mortgage points-and-fees tiers.\n'
                  '  2023: tier A $124,331 \u00b7 tier B fixed $3,730 \u00b7 tier C floor $24,866 \u00b7 tier D fixed $1,243\n'
                  '  2024: tier A $130,461 \u00b7 tier B fixed $3,914 \u00b7 tier C floor $26,092 \u00b7 tier D fixed $1,305\n'
                  '  The 2025 adjustment reflects a 3.4 percent CPI-U increase; the 2024 adjustment reflected 4.9 percent.\n\n'
                  '<b>Tasks:</b>\n'
                  '  1. Compute the implied 2023\u21922024 adjustment factor per tier (4 factors, each to 6 decimal places).\n'
                  '  2. Project the 2025 values per tier by applying 3.4 percent, with the rounding rule you infer.\n'
                  '  3. The actual official 2025 tier A value is $134,841. Compare your projection; compute the exact '
                  'factor that WOULD produce it and state the discrepancy in basis points.\n'
                  '  4. `weakest_point`: a concrete mechanism, not a hedge.',
                  "The other four: C2-JCS-STRINGS (exact RFC 8785 byte strings) &middot; PROMPT-E-CALCULATIONS "
                  "&middot; J-ISSUE-REDTEAM-V1 (red1) &middot; J-EPISODE-REDTEAM-V3 (red3)")
              + roster([("Reg Z &mdash; exact recomputation", "t"), ("JCS &mdash; RFC 8785 byte strings", "t"),
                        ("E &mdash; hardware-assurance calcs", "g"), ("red1 &mdash; BoomTile, known-imperfect", "p"),
                        ("red3 &mdash; Niagara, known-sound", "p")]))
    + section("What graded it", "Why two stations were used",
              grader_cards([
                  ("Station 1", "Opus 5",
                   "Graded all five tracks mechanically: a closed-form Reg Z recomputation, a scratch RFC 8785 "
                   "canonicalizer self-tested against the RFC's own number vectors, and a token-based shape check "
                   "for the E slice. Wrote the per-model feed.",
                   "Web Model Tasks/Day 5/_digest/ &middot; digest/_verify/d5run/d5permodel.json"),
                  ("Station 2", "GLM 5.3 Flash",
                   "Independently vetted the tally codebook from Opus&nbsp;5 before any verdict row was staged. "
                   "The vet found four defects in the named-list branch; the run stayed gated until they were fixed.",
                   "digest/TALLYCODES-VET-1.md &middot; TALLYCODES-VET-1-VERDICT-FLASH.md"),
                  ("Why two", "A rule cannot be tested by the thing it produced",
                   "GLM&nbsp;5.3 Flash reproduced Opus&nbsp;5&rsquo;s count of 13 exact Reg&nbsp;Z scores and signed "
                   "it off, and the count was still wrong. A substring matcher had credited "
                   "<code>1.033573</code> inside <code>1.0335735</code>. <em>Reproducing a number does not test the "
                   "rule that produced it.</em>",
                   "Web Model Tasks/Day 5/_digest/01-regz.md"),
              ]))
    + section("How each model performed", "The per-model feed for 16 models across 5 instruments",
              table("Measured from digest/_verify/d5run/d5permodel.json rather than transcribed from prose",
                    ["Model", "Reg Z /9", "JCS /4", "E shape-ok", "red1 verdict (objections)", "red3 verdict (objections)", "Calibration"],
                    [["chatgpt", ("9", "ok"), "n/g", "6 / 10", "S-W-RES (4)", "S-W-RES (7)", ("consistent", "ok")],
                     ["deepseek", ("8", "mid"), ("3", "ok"), "4 / 8", "S-W-RES (3)", "S-W-RES (3)", ("consistent", "ok")],
                     ["gemini", ("9", "ok"), ("2", "mid"), "6 / 12", "S-W-RES (1)", ("SOUND (0)", "bad"), ("r1 ok &middot; r3 MISCALIBRATED", "bad")],
                     ["glm 5.3 flash", ("9", "ok"), ("3", "ok"), "8 / 12", "S-W-RES (3)", "S-W-RES (3)", ("consistent", "ok")],
                     ["grok", ("9", "ok"), ("4", "ok"), "7 / 12", "S-W-RES (2)", ("SOUND (0)", "bad"), ("r1 ok &middot; r3 MISCALIBRATED", "bad")],
                     ["kimi", ("9", "ok"), ("4", "ok"), "4 / 6", "S-W-RES (3)", "S-W-RES (4)", ("consistent", "ok")],
                     ["longcat", ("9", "ok"), ("3", "ok"), "7 / 12", ("SUSPECT (2)", "mid"), ("SOUND (2)", "bad"), ("r1 ok &middot; r3 SCHEMA-ANOMALY", "mid")],
                     ["meta", ("9", "ok"), ("4", "ok"), "6 / 10", "S-W-RES (1)", ("SOUND (0)", "bad"), ("r1 ok &middot; r3 MISCALIBRATED", "bad")],
                     ["mimo", ("9", "ok"), ("2", "mid"), "4 / 11", "S-W-RES (4)", "S-W-RES (4)", ("consistent", "ok")],
                     ["minara", ("9", "ok"), ("4", "ok"), "6 / 10", "S-W-RES (1)", "S-W-RES (1)", ("consistent", "ok")],
                     ["minimax 2.7", ("5", "bad"), ("2", "mid"), "4 / 7", ("S-W-RES (0)", "bad"), ("SOUND (0)", "bad"), ("r1 SCHEMA-ANOMALY &middot; r3 MISCALIBRATED", "bad")],
                     ["mistral", ("2", "bad"), ("1", "bad"), "3 / 12", "S-W-RES (2)", "S-W-RES (3)", ("consistent", "ok")],
                     ["qwen", ("9", "ok"), ("2", "mid"), "6 / 10", "S-W-RES (1)", ("SOUND (0)", "bad"), ("r1 ok &middot; r3 MISCALIBRATED", "bad")],
                     ["solar", ("n/g", "dim"), ("3", "ok"), "6 / 12", "S-W-RES (3)", ("n/g", "dim"), ("r1 ok &middot; r3 not gradable", "mid")],
                     ["sonnet", ("9", "ok"), ("4", "ok"), "8 / 12", "S-W-RES (3)", "S-W-RES (3)", ("consistent", "ok")],
                     ["yuanbao", ("9", "ok"), ("3", "ok"), ("9 / 12", "ok"), "S-W-RES (6)", "S-W-RES (4)", ("consistent", "ok")]],
                    highlight_col=None)
              + '<div class="legend">S-W-RES = SOUND-WITH-RESERVATIONS. n/g = not gradable. '
                '&ldquo;E shape-ok&rdquo; is a token check, not a correctness check: an inverted formula that '
                'keeps the right tokens passes it silently. Reg&nbsp;Z /9 counts reference values present in the '
                'model&rsquo;s text; 12 of 15 gradable models are exact on all nine.</div>'
              + table("The tally codebook before any verdict row was staged",
                      ["Probe (verbatim from the verdict)", "Returned", "Should be", "Defect class"],
                      [["<code>code_verdict(\"not sound\", \"34\")</code>", ("SOUND", "bad"), "UNCODED (or negation-aliased)", "A negated alias still codes positive"],
                       ["<code>code_field(\"evid\", \"not measured\")</code>", ("MEAS", "bad"), "ASSERT", "Synonyms of one concept assigned to opposite codes"],
                       ["<code>code_field(\"dir\", \"does not match the paper\")</code>", ("MATCHES", "bad"), "UNCODED or REVERSAL-aliased", "Same semantics code two ways"],
                       ["<code>calibration(\"SOUND\", 0, \"Known-Sound\")</code>", ("consistent", "bad"), "MISCALIBRATED-bare-SOUND or a loud error", "Silent <code>consistent</code> masks the calibration finding entirely"]],
                      highlight_col=None))
    + section("What it found", "Three instruments that disagreed",
              verdict_pair(
                  "<code>sonnet</code>",
                  "Exact on all nine Reg Z values and all four JCS cases, with calibration consistent on both "
                  "red-team blocks.",
                  "<code>mistral</code>",
                  "Bottom on both exact tracks: 2 of 9 Reg Z values and 1 of 4 JCS cases.")
              + findings([
                  ("", "Reg Z separated almost nobody",
                   "12 of the 15 gradable models are exact on all nine values, so the track works as a floor test "
                   "and not as a ranking. <code>mistral</code> managed 2 of 9 and <code>minimax 2.7</code> 5 of 9. "
                   "<code>solar</code> answered in prose, was recorded <code>PROSE-NOT-JSON</code>, and was excluded "
                   "from the denominator rather than scored zero."),
                  ("", "The JCS instrument was the discriminator",
                   "Scores run 1 to 4 of 4, driven almost entirely by case 3, ES6 number serialization at "
                   "<code>1e21</code>, <code>1e-7</code>, <code>-0</code> and the 2<sup>53</sup> boundary. Five "
                   "models scored 4 of 4: <code>grok</code>, <code>kimi</code>, <code>meta</code>, "
                   "<code>minara</code> and <code>sonnet</code>. Four scored 2, <code>mistral</code> scored 1, and "
                   "<code>longcat</code> reached 3 with one case right for the wrong rule."),
                  ("warn", "Exact arithmetic does not predict specification conformance",
                   "<code>gemini</code> and <code>qwen</code> are 9 of 9 on Reg&nbsp;Z arithmetic and 2 of 4 on "
                   "canonicalization. <code>grok</code> and <code>meta</code> are 9 of 9 and 4 of 4. "
                   "<code>mistral</code> is weak on both at 2 of 9 and 1 of 4. The two tracks rank the field "
                   "differently."),
                  ("bad", "Reviewing well was a third and orthogonal capability",
                   "Five models returned bare <code>SOUND</code> on the known-sound block, whose own prompt names "
                   "its gaps: <code>gemini</code>, <code>grok</code>, <code>meta</code>, <code>minimax 2.7</code> "
                   "and <code>qwen</code>. Two of them, <code>grok</code> and <code>meta</code>, are 9 of 9 and 4 of "
                   "4 on the arithmetic tracks. <code>longcat</code> reached the same verdict with two objections "
                   "attached and was recorded as a schema anomaly."),
                  ("warn", "One prompt case never reached a single model",
                   "The JCS case-5 input embedded a raw <code>U+0007</code> control character, which is illegal in "
                   "JSON. Every chat surface stripped it, so no model ever saw the case. Grading it against the "
                   "reference would have logged a transmission loss as 15 model failures, and it is scored "
                   "<code>UNGRADABLE</code> instead."),
              ]))
    + section("Source files", "Where the evidence lives",
              srcs(["Web Model Tasks/Day 5/ (80 entries)", "Web Model Tasks/Day 5/_digest/ (8 files)",
                    "digest/_verify/d5run/d5permodel.json", "digest/_verify/d5tally.py",
                    "digest/_verify/tallycodes.py", "digest/TALLYCODES-VET-1.md",
                    "digest/TALLYCODES-VET-1-VERDICT-FLASH.md", "prompts/C1-REGZ-FACTOR.md",
                    "prompts/C2-JCS-STRINGS.md", "prompts/PROMPT-E-CALCULATIONS.md",
                    "prompts/J-ISSUE-REDTEAM-V1.md", "prompts/J-EPISODE-REDTEAM-V3.md"]))
)


DAY6 = (
    hero("Day 6 &middot; Citation + deployment &middot; collected 2026-09-11",
         "Twenty-seven browser cells and three citation anchors",
         "Two prompts with a calibration trick built in: each carries three anchor questions whose answers are "
         "already known, so a model can be scored on calibration separately from its research. The browser "
         "matrix was then checked against real measurements.",
         [("32", "files collected"), ("16", "models"), ("2", "prompts"),
          ("28", "files parsed / 32")])
    + section("The prompt", "Anchors before the grid",
              '<div class="prose"><p>Both prompts open with an <em>anchor check</em> whose ground truth the '
              'estate already holds. Two of the three C-v5 anchors are genuine; the third is a mutated-venue '
              'decoy whose underlying paper is real. Answering the decoy <code>exists-exactly</code> is '
              'fabrication-liable.</p></div>'
              + scene_html("day6")
              + prompt_card(
                  "PROMPT-B-BROWSER &middot; B-v8",
                  "the deployment matrix; 27 rows, no more and no fewer",
                  '<span class="q">I am filling a deployment-constraint matrix for running cryptographic proving '
                  'workloads (WebAssembly + WebGPU) inside web browsers. Answer the cells below for the CURRENT state '
                  'of Chrome/Edge, Firefox, and Safari. Two access tiers \u2014 pick honestly:</span>\n\n'
                  '- <b>Live web access:</b> cite a URL and retrieval date for every claim \u2014 no URL, no claim.\n'
                  '- <b>No live web access:</b> do NOT stop and do NOT skip rows. Answer from training knowledge; set '
                  'knowledge_basis to "training-recall". A labeled training-recall answer is useful data; an invented '
                  'URL is not; an empty file is neither.\n\n'
                  '<b>ANCHOR CHECK (calibration; answer all three):</b>\n'
                  '  b1: "SharedArrayBuffer is available to a page only under cross-origin isolation (COOP/COEP)."\n'
                  '  b2: "WebGPU timestamp-query is exposed to ordinary web content by default in current Chrome."\n'
                  '  b3: "WebAssembly threads module validation fails without cross-origin isolation in current Chrome."\n\n'
                  '<b>THE ROW GRID \u2014 27 rows, no more and no fewer.</b> Every row is uniquely keyed by '
                  '(cell, browser). Emit one row per key even when your answer is identical across browsers.',
                  "The paired prompt: PROMPT-C-SOURCES &middot; C-v5 &mdash; three citation anchors (a1/a2 genuine, "
                  "a3 a mutated-venue decoy) plus up to 8 novel public sources, with per-source knowledge_basis, "
                  "verification_hint and access_guess")
              + roster([("b1 &mdash; SharedArrayBuffer + COI", "t"), ("b2 &mdash; timestamp-query by default", "t"),
                        ("b3 &mdash; threads validation without COI", "t"),
                        ("a1/a2 &mdash; genuine citations", "g"), ("a3 &mdash; mutated-venue decoy", "g")]))
    + section("What graded it", "The Flash station and its tool access",
              grader_cards([
                  ("Station", "GLM 5.3 Flash",
                   "Harvested both slices with tooling rather than by hand: 32 files, C-v5 and B-v8. Anchor answers "
                   "were matched with the pinned longest-alias-first rules from the tally codebook.",
                   "SESSION-MEMORIAL-2026-09-09-FLASH-DAY5-VET-1.md &sect;M2"),
                  ("Method", "A pinned anchor key, written before dispatch",
                   "a1 and a2 = <code>exists-exactly</code>. a3 = <code>exists-but-citation-wrong</code>, and a "
                   "correction counts only if it names <b>both</b> the venue and the year 2001. Naming a different "
                   "wrong venue is a WRONG-CORRECTION, worse than <code>unknown</code>, and previously "
                   "unrepresented.",
                   "prompts/PROMPT-C-SOURCES.md (build note)"),
                  ("Ground truth", "Real browser measurements",
                   "Part of the B matrix no longer needs a model&rsquo;s opinion: the zkprof project has measured "
                   "ground truth for several cells, and where a measurement exists it wins.",
                   "digest/browser-cells.md"),
              ]))
    + section("How each model performed", "The B-v8 anchors and what the measurement says",
              table("Anchor verdicts measured from the response files against the estate's own browser ground truth",
                    ["Model", "b1 SAB + COI", "b2 timestamp-query default", "b3 threads without COI"],
                    [["chatgpt", ("agree", "ok"), ("disagree", "bad"), ("disagree", "ok")],
                     ["deepseek", ("agree", "ok"), ("agree", "ok"), ("disagree", "ok")],
                     ["gemini", ("agree", "ok"), ("disagree", "bad"), ("disagree", "ok")],
                     ["glm 5.3 flash", ("agree", "ok"), ("disagree", "bad"), ("agree", "bad")],
                     ["grok", ("agree", "ok"), ("agree", "ok"), ("agree", "bad")],
                     ["kimi", ("agree", "ok"), ("agree", "ok"), ("disagree", "ok")],
                     ["longcat", ("agree", "ok"), ("disagree", "bad"), ("agree", "bad")],
                     ["meta", ("not parsed", "dim"), ("not parsed", "dim"), ("not parsed", "dim")],
                     ["mimo", ("agree", "ok"), ("disagree", "bad"), ("disagree", "ok")],
                     ["minara", ("agree", "ok"), ("agree", "ok"), ("disagree", "ok")],
                     ["minimax", ("agree", "ok"), ("disagree", "bad"), ("agree", "bad")],
                     ["mistral", ("agree", "ok"), ("disagree", "bad"), ("agree", "bad")],
                     ["qwen", ("agree", "ok"), ("disagree", "bad"), ("agree", "bad")],
                     ["solar", ("not parsed", "dim"), ("not parsed", "dim"), ("not parsed", "dim")],
                     ["sonnet", ("agree", "ok"), ("agree", "ok"), ("disagree", "ok")],
                     ["yuanbao", ("agree", "ok"), ("agree", "ok"), ("disagree", "ok")]],
                    highlight_col=None)
              + '<div class="legend">14 of 16 files parsed. <b>b1</b>: 14 of 14 agree, unanimous and '
                'correct. <b>b2</b>: 8 of 14 disagree, asserting the falsified claim that timestamp-query is not '
                'exposed by default; the measurement says it is. <b>b3</b>: 6 of 14 agree, asserting a threads '
                'failure the measurement contradicts: the module was accepted in both modes. '
                'Two models (<code>meta</code>, <code>solar</code>) could not be graded: their files do not parse.</div>'
              + table("C-v5 citation anchors: the mutated-venue decoy",
                      ["Model", "a1", "a2", "a3 verdict", "a3 correction test", "Anchor result"],
                      [["deepseek", "exists-exactly", "exists-exactly", "citation-wrong", ("venue + 2001", "ok"), ("PASS", "ok")],
                       ["glm 5.3 flash", "exists-exactly", "exists-exactly", "citation-wrong", ("venue + 2001", "ok"), ("PASS", "ok")],
                       ["grok", "exists-exactly", "exists-exactly", "citation-wrong", ("venue + 2001", "ok"), ("PASS", "ok")],
                       ["kimi", "exists-exactly", "exists-exactly", "citation-wrong", ("venue + 2001", "ok"), ("PASS", "ok")],
                       ["longcat", "exists-exactly", "exists-exactly", "citation-wrong", ("venue + 2001", "ok"), ("PASS", "ok")],
                       ["meta", "exists-exactly", "exists-exactly", "citation-wrong", ("venue + 2001", "ok"), ("PASS", "ok")],
                       ["mimo", "exists-exactly", "exists-exactly", "citation-wrong", ("venue + 2001", "ok"), ("PASS", "ok")],
                       ["minara", "exists-exactly", "exists-exactly", "citation-wrong", ("venue + 2001", "ok"), ("PASS", "ok")],
                       ["minimax", "exists-exactly", "exists-exactly", "citation-wrong", ("venue + 2001", "ok"), ("PASS", "ok")],
                       ["mistral", "exists-exactly", "exists-exactly", "citation-wrong", ("venue + 2001", "ok"), ("PASS", "ok")],
                       ["sonnet", "exists-exactly", "exists-exactly", "citation-wrong", ("venue + 2001", "ok"), ("PASS", "ok")],
                       ["yuanbao", "exists-exactly", "exists-exactly", "citation-wrong", ("venue + 2001", "ok"), ("PASS", "ok")],
                       ["qwen", "exists-exactly", "exists-exactly", "citation-wrong", ("venue only &mdash; named IEEE Micro", "bad"), ("WRONG-CORRECTION", "bad")],
                       ["solar", "exists-exactly", "exists-exactly", "citation-wrong", ("venue only &mdash; named IEEE Micro", "bad"), ("WRONG-CORRECTION", "bad")],
                       ["chatgpt", ("not parsed", "dim"), ("not parsed", "dim"), ("not parsed", "dim"), ("&mdash;", "dim"), ("not gradable", "dim")],
                       ["gemini", ("not parsed", "dim"), ("not parsed", "dim"), ("not parsed", "dim"), ("&mdash;", "dim"), ("not gradable", "dim")]],
                      highlight_col=5)
              + '<div class="legend">14 of 16 files parsed. Every graded model identified the decoy as '
                '<code>exists-but-citation-wrong</code>; nobody was fabrication-liable. Under the stricter '
                'correction rule, 12 of 14 name both the venue and the year. The two that fail name '
                '<b>a different wrong venue</b> (<code>qwen</code>: &ldquo;IEEE Micro, vol. 21, no. 1&rdquo;; '
                '<code>solar</code>: &ldquo;IEEE Micro vol. 21, no. 6&rdquo;), the WRONG-CORRECTION class the '
                'build note calls worse than <code>unknown</code>.</div>')
    + section("What it found", "Where the models were right and where measurement overruled them",
              verdict_pair(
                  "<code>deepseek</code>",
                  "One of five models to agree with measured ground truth on all three anchors and pass the "
                  "citation decoy.",
                  "<code>qwen</code>",
                  "Got two of three browser anchors wrong and failed the citation decoy as a wrong-correction, "
                  "naming a different wrong venue.")
              + findings([
                  ("", "Twelve of fourteen passed the citation anchors",
                   "Every graded model refused the decoy. Both failures took the worse form, a wrong-correction: "
                   "<code>qwen</code> offered &ldquo;IEEE Micro, vol. 21, no. 1&rdquo; and "
                   "<code>solar</code> &ldquo;IEEE Micro vol. 21, no. 6&rdquo;, each naming a different wrong venue "
                   "instead of the correct venue and the year 2001. The build note classes this as worse than "
                   "answering <code>unknown</code>."),
                  ("bad", "Eight models asserted a falsified browser claim",
                   "<code>timestamp-query</code> is available by default in current Chrome, measured. Eight of the "
                   "fourteen graded models said the opposite: <code>chatgpt</code>, <code>gemini</code>, <code>glm "
                   "5.3 flash</code>, <code>longcat</code>, <code>mimo</code>, <code>minimax</code>, "
                   "<code>mistral</code> and <code>qwen</code>. The other six, <code>deepseek</code>, "
                   "<code>grok</code>, <code>kimi</code>, <code>minara</code>, <code>sonnet</code> and "
                   "<code>yuanbao</code>, agreed with the measurement."),
                  ("warn", "A confident model claim was falsified on availability",
                   "<code>sonnet</code> tagged its claim that <code>timestamp-query</code> is NOT exposed by default "
                   "as <code>verified from current authoritative page</code>, and the measurement falsifies it. That "
                   "record is from the Day-1 wave in the merged browser-cell file. On the Day-6 anchors the same "
                   "model agreed with the ground truth, so the two records disagree with each other."),
                  ("warn", "Two cells measured unavailable against confident claims of broad support",
                   "<code>relaxed-SIMD</code> and <code>memory64</code> were both rejected by the engine. "
                   "<code>kimi</code> claimed Chrome 114+, Firefox 120+ and Safari 18.4+ for relaxed-SIMD and Chrome "
                   "133+, Edge 133+ and Firefox 134+ for memory64. <code>glm</code> and <code>sonnet</code> called "
                   "relaxed-SIMD part of standardized Wasm 3.0. A real Chrome 151 refused both, so the cells are "
                   "recorded CONTESTED pending a check of the probe&rsquo;s own test modules."),
                  ("", "Two files did not parse and are recorded as absences",
                   "<code>meta</code> and <code>solar</code> on B-v8, and <code>chatgpt</code> and "
                   "<code>gemini</code> on C-v5, produced files that do not parse, so 28 of the 32 files were "
                   "gradable. Not gradable is a value here, never a zero."),
              ]))
    + section("Source files", "Where the evidence lives",
              srcs(["Web Model Tasks/Day 6/ (32 entries)", "digest/browser-cells.md",
                    "digest/source-candidates.md", "prompts/PROMPT-B-BROWSER.md",
                    "prompts/PROMPT-C-SOURCES.md", "SESSION-MEMORIAL-2026-09-09-FLASH-DAY5-VET-1.md &sect;M2"]))
)


DAY7 = (
    hero("Day 7 &middot; Format drift &middot; collected 2026-09-14",
         "Fifteen models flipped from JSON to prose in seventy-two hours",
         "Fifteen models ran the same red-team block under an unchanged prompt. Not one returned the required "
         "schema. Every model invented its own verdict vocabulary, and most of them answered in prose.",
         [("31", "entries"), ("15", "models"), ("0 / 15", "schema compliance"),
          ("14", "prose responses")])
    + section("The prompt", "A literal copy-exact template and a first-character contract",
              '<div class="prose"><p>JI-v1.1 was already the hardened version: it added a binding output-format '
              'contract, because an earlier block-01 wave had returned prose reviews from most models despite a '
              '&ldquo;nothing else&rdquo; rule. The schema was still described abstractly. That turned out to be '
              'the problem.</p></div>'
              + scene_html("day7")
              + prompt_card(
                  "J-ISSUE-REDTEAM-V1 &middot; JI-v1.1 (block 01)",
                  "superseded on 2026-09-10 by JI-v1.2, which replaced the abstract schema with a literal template",
                  '<span class="q">**OUTPUT FORMAT (binding, read first):** your entire response must be exactly one '
                  'JSON object matching the schema at the end of this brief. The first character of your reply must '
                  'be `{` and the last must be `}`. No markdown, no headings, no commentary before or after, no code '
                  'fences, no explanations \u2014 the JSON object only.</span>\n\n'
                  'You are a skeptical principal engineer reviewing a DRAFT incident episode before it enters a '
                  'curated dataset. The episode was mined from a public bug-tracker thread. Your job is to attack '
                  'it: find every technical claim that is wrong, implausible, or internally inconsistent \u2014 and '
                  'say what a correct version would look like.\n\n'
                  '**The draft under review:** RECORD: OpenROAD issue #6066 \u2014 BoomTile/Megaboom: 20k routing '
                  'congestion DRCs at only 0.24 placement density.\n\n'
                  '**Your review, as a single bare JSON object:** {"verdict": one of SOUND | '
                  'SOUND-WITH-RESERVATIONS | SUSPECT | IMPLAUSIBLE-FOR-THIS-RECORD, "objections": [...], '
                  '"mechanism_check", "evidence_check", "attribution_check", "missing_from_story", '
                  '"most_defensible_part"}\n\n'
                  '**Hard rules:** attack the NUMBERS, the causal chain, and whether the intervention explains the '
                  'outcome \u2014 not the writing. Do not browse the web or fetch any page. Fewer sharp objections '
                  'beat a padded list.',
                  "The drift is the finding: 0 of 15 files carried the required seven-key schema, and every model "
                  "invented its own verdict vocabulary: <code>reject</code>, <code>reject_and_revise</code>, "
                  "<code>REVISE_BEFORE_INGEST</code>, <code>overstated</code>, <code>not_ready</code>, "
                  "<code>reject-as-is</code>."))
    + section("What graded it", "The Flash station and a prompt fix",
              grader_cards([
                  ("Station", "GLM 5.3 Flash",
                   "Collected and harvested the block-01 wave. The result was a prompt-format problem rather than a "
                   "prompt-format problem, and it was recorded as one.",
                   "SESSION-MEMORIAL-2026-09-09-FLASH-DAY5-VET-1.md"),
                  ("The fix", "JI-v1.2 &mdash; a literal copy-exact template",
                   "The abstract one-line schema was replaced by a literal template with field-leading enums "
                   "(HOLDS/BREAKS/N-D, MEAS/ASSERT/N-D, SUPPORTS/WEAK/ABSENT/N-D), after this pilot returned "
                   "0/15 schema compliance and every model invented its own verdict vocabulary.",
                   "prompts/J-ISSUE-REDTEAM-V1.md (version note)"),
                  ("Note", "A 72-hour flip on an unchanged prompt",
                   "The same family of prompts had returned compliant JSON earlier in the week. The drift is a "
                   "property of the chat surface, not of the schema.",
                   "digest/DIGEST-REPORT.md"),
              ]))
    + section("How each model performed", "Response form and schema compliance measured from the files",
              table("Measured from Web Model Tasks/Day 7/: every file inspected and parsed",
                    ["Model", "JSON file", "Prose file", "7-key schema", "Verdict token the model actually emitted"],
                    [["chatgpt", "yes (12.1 KB, unparseable)", "yes", ("0 / 7", "bad"), "&mdash;"],
                     ["deepseek", "yes (4.9 KB, parses)", "yes", ("1 / 7", "bad"), "reject"],
                     ["gemini", "yes (5.1 KB, parses)", "yes", ("1 / 7", "bad"), "reject_and_revise"],
                     ["glm flash", "yes (15.1 KB, parses)", "yes", ("1 / 7", "bad"), "reject-as-is"],
                     ["grok", "yes (3.7 KB, parses)", "yes", ("1 / 7", "bad"), "overstated"],
                     ["kimi", "yes (6.6 KB, parses)", "yes", ("1 / 7", "bad"), "REVISE_BEFORE_INGEST"],
                     ["longcat", "yes (7.2 KB, parses)", "yes", ("1 / 7", "bad"), "REJECT for curated dataset. The record contains fundamental stage-confusion errors&hellip;"],
                     ["meta", "yes (6.0 KB, unparseable)", "yes", ("0 / 7", "bad"), "&mdash;"],
                     ["mimo", "yes (9.3 KB, parses)", "yes", ("0 / 7", "bad"), "&mdash; (fenced, no verdict key)"],
                     ["minimax", "yes (6.7 KB, parses)", "yes", ("0 / 7", "bad"), "&mdash; (no verdict key)"],
                     ["mistral", "yes (2 of them, neither parses)", "yes", ("0 / 7", "bad"), "&mdash;"],
                     ["qwen", "yes (2.4 KB, parses)", "yes", ("0 / 7", "bad"), "&mdash; (no verdict key)"],
                     ["solar", "yes (5.4 KB, unparseable)", "yes", ("0 / 7", "bad"), "&mdash;"],
                     ["sonnet", "yes (4.3 KB, parses)", "yes", ("1 / 7", "bad"), "not_ready"],
                     ["yuanbao", "yes (13.9 KB, parses)", "yes", ("1 / 7", "bad"), "reject-as-recovery-episode"]],
                    highlight_col=3)
              + '<div class="legend">Every file was opened and measured: 16 JSON files and 14 prose files. <b>No file '
                'carried the required seven-key schema</b>. The best any model managed was one key out of '
                'seven. Four files do not parse at all. The verdict column shows what the models emitted instead: '
                'fifteen different vocabularies for a four-value enum.</div>')
    + section("What it found", "The finding is the drift itself",
              verdict_pair(
                  "<code>longcat</code>",
                  "One of eight models at the day&rsquo;s ceiling of one schema key, and its verdict named the "
                  "record&rsquo;s stage-confusion errors.",
                  "<code>mistral</code>",
                  "Returned two JSON files and neither parsed, the only model to fail twice, with zero of seven "
                  "schema keys.")
              + findings([
                  ("bad", "Zero of fifteen returned the required schema",
                   "The prompt offered four verdict values. The fifteen models emitted <code>reject</code>, "
                   "<code>reject_and_revise</code>, <code>REVISE_BEFORE_INGEST</code>, <code>overstated</code>, "
                   "<code>not_ready</code>, <code>reject-as-is</code>, <code>reject-as-recovery-episode</code> and "
                   "more: fifteen vocabularies for one enum. A grader keyed on the enum would have failed all "
                   "fifteen for the wrong reason, and shortest-enum-first matching would have collapsed reserved "
                   "verdicts into <code>SOUND</code>, the defect found in the Day-5 codebook."),
                  ("warn", "The contract broke on the prose files",
                   "The rule asked for one bare JSON object, no fences and no commentary. Fourteen of the fifteen "
                   "models also returned a prose file, and <code>mistral</code> returned two JSON files with no "
                   "prose at all. Two of the sixteen JSON files open with a <code>```json</code> fence the prompt "
                   "forbids by name, <code>mimo</code>&rsquo;s and <code>mistral</code>&rsquo;s second. The other "
                   "fourteen open with <code>{</code>."),
                  ("", "The fix was structural and it worked",
                   "JI-v1.2 replaced the one-line schema with a literal object to copy and put the enum values "
                   "directly against the field names. The same three models scored 0 of 15 on the one-line schema "
                   "and 30 of 30 on the template, all seven keys present, none renamed or extra."),
                  ("", "The drift was a delivery problem",
                   "<code>kimi</code>&rsquo;s prose response names a confounded intervention, two knobs changed at "
                   "once, which is a real objection the schema had no field for. <code>deepseek</code> wrote "
                   "&ldquo;reject&rdquo; where the enum held four reserved values and none of them was "
                   "&ldquo;reject&rdquo;. Both models reasoned correctly and encoded incorrectly."),
              ]))
    + section("Source files", "Where the evidence lives",
              srcs(["Web Model Tasks/Day 7/ (31 entries)", "prompts/J-ISSUE-REDTEAM-V1.md (JI-v1.1 &rarr; JI-v1.2)",
                    "prompts/J-EPISODE-REDTEAM-V3.md", "digest/TALLYCODES-VET-1.md",
                    "SESSION-MEMORIAL-2026-09-09-FLASH-DAY5-VET-1.md", "Web Model Tasks/Day 7/v12-pilot/"]))
)

DAY8 = (
    hero("Day 8 &middot; The sweep &middot; collected 2026-09-17",
         "Thirty schema-compliant reviews of ten incident drafts",
         "The JI-v1.2 fix was tested against the same three models that had just produced 0 / 15 schema "
         "compliance. This time every one of the thirty responses parsed on the first try, with the full "
         "seven-key schema and no renamed keys.",
         [("30", "files"), ("3", "models"), ("10", "drafts"), ("30 / 30", "schema compliance"),
          ("15 / 15", "SUSPECT / S-W-RES")])
    + section("The prompt", "The literal template that replaced the abstract schema",
              '<div class="prose"><p>JI-v1.2 is the whole intervention. The Day-7 pilot had shown that an '
              'abstract one-line schema was not a contract: fifteen models each invented their own verdict '
              'vocabulary. JI-v1.2 replaced the schema with a literal object to copy, and put the enum values '
              'directly against the field names.</p><p>Each model saw each of the ten drafts exactly once. The '
              'drafts were stratified by failure type rather than taken as the first ten: unmeasured post-state, '
              'resolution claimed with no fix described, a tooling policy that hides errors, a crash on degenerate '
              'input, measurement validity, nondeterminism, silent netlist corruption, a repair that took 40000 '
              'seconds on one endpoint, a misattributed root cause, and a bug closed without reproduction.</p></div>'
              + scene_html("day8")
              + prompt_card(
                  "J-ISSUE-REDTEAM-V1 &middot; JI-v1.2",
                  "the fix that closed the Day-7 drift: a literal template instead of a described schema",
                  '<span class="q">**OUTPUT FORMAT (binding, read first):** your entire response must be exactly one '
                  'JSON object matching the schema at the end of this brief. The first character of your reply must '
                  'be `{` and the last must be `}`. No markdown, no headings, no commentary before or after, no code '
                  'fences, no explanations &mdash; the JSON object only.</span>\n\n'
                  '**Your review, as a single bare JSON object:** {"verdict": one of SOUND | '
                  'SOUND-WITH-RESERVATIONS | SUSPECT | IMPLAUSIBLE-FOR-THIS-RECORD, "objections": [{"claim_attacked", '
                  '"objection", "severity", "confidence"}], "mechanism_check", "evidence_check", "attribution_check", '
                  '"missing_from_story", "most_defensible_part"}\n\n'
                  '**Hard rules:** attack the NUMBERS, the causal chain, and whether the intervention explains the '
                  'outcome &mdash; not the writing. The pasted record is the WHOLE evidence base: do not browse the '
                  'web or fetch any page. Do not invent thread content, commits, PRs, participants, or tool '
                  'behaviour that is not in it. If the record does not settle a question, write '
                  '&ldquo;not-determinable-from-this-record&rdquo; rather than guessing &mdash; a field-level escape '
                  'beats a guessed objection. A claimed resolution with no measured post-state is an EVIDENCE defect, '
                  'not a mechanism defect; classify it under `evidence_check`. If a claim is sound, say so &mdash; '
                  'inventing objections is as bad as missing real ones. Fewer sharp objections beat a padded list. '
                  'This review is a PRE-SCREEN for expert review, not a verdict on the underlying bug &mdash; flag, '
                  'don&rsquo;t convict.',
                  "Same three models as the Day-7 pilot: <b>kimi</b>, <b>sonnet</b>, <b>deepseek</b>. Chosen for "
                  "clean records on the earlier truth-anchored instruments: arithmetic exact on 9 / 9 values, "
                  "format conformance 4 / 4 on the reference canonicalizer, correct on the citation-anchor and "
                  "measured browser-behaviour probes. <code>chatgpt</code> ran block 01 as a format pilot and was "
                  "schema-compliant, but was not extended to the other nine blocks."))
    + section("What graded it", "How the sweep was harvested and what debt it left",
              grader_cards([
                  ("Station", "GLM 5.3 Flash",
                   "Collected and harvested the sweep. The harvest is reproducible from the script, not from a "
                   "human reading thirty files: <code>digest/_verify/flash_d6_harvest.py</code> &rarr; "
                   "<code>d6run/d6harvest.json</code>, staged tally in <code>redteam/TALLY-34.md</code>.",
                   "digest/wave1-report.md"),
                  ("The instrument", "Format conformance, then verdict calibration",
                   "Two separate checks. First the mechanical one: does the file parse, does it carry all "
                   "seven keys, are any keys renamed or extra. Then the calibration check: the prompt defines a "
                   "four-value enum with two reserved values, so a bare <code>SOUND</code> on a draft known to be "
                   "imperfect would be the same miscalibration defect the tally codebook had produced earlier.",
                   "redteam/TALLY-34.md"),
                  ("Recorded debt", "Expert review: not performed",
                   "None of the thirty verdicts has been reviewed by a human expert. The dataset card, when it "
                   "ships, will say exactly that. The verdicts and the full response JSON are on disk and "
                   "hash-verified, so anyone can re-run the same prompt on the same block and compare.",
                   "digest/wave1-report.md, &ldquo;What the review debt looks like&rdquo;"),
              ]))
    + section("How each model performed", "Schema compliance and verdict calibration measured from the files",
              table("Measured from Web Model Tasks/Day 8/: all 30 files parsed without repair",
                    ["Model", "Files", "7-key schema", "Objections", "Major / minor", "SUSPECT", "S-W-RES",
                     "Bare SOUND"],
                    [["deepseek", "10 / 10", ("30 / 30", "ok"), "26", "20 / 6", ("9", "bad"), "1", ("0", "ok")],
                     ["kimi", "10 / 10", ("30 / 30", "ok"), "23", "16 / 7", "2", ("8", "ok"), ("0", "ok")],
                     ["sonnet", "10 / 10", ("30 / 30", "ok"), "22", "8 / 14", "4", ("6", "ok"), ("0", "ok")],
                     ["chatgpt", ("1 (pilot)", "dim"), ("block 01 only", "dim"), "&mdash;", "&mdash;",
                      "&mdash;", "&mdash;", ("0", "ok")]],
                    highlight_col=2)
              + table("Per-block verdict matrix; S-W-RES = SOUND-WITH-RESERVATIONS",
                      ["Block", "Draft under review", "deepseek", "kimi", "sonnet", "Reading"],
                      [["red1-01", "BoomTile/Megaboom: 20k congestion DRCs at 0.24 density",
                        ("SUSPECT", "bad"), ("S-W-RES", "ok"), ("S-W-RES", "ok"), "deepseek strictest"],
                       ["red1-02", "GPL-0314: getFillerGCell index out of bounds",
                        ("SUSPECT", "bad"), ("SUSPECT", "bad"), ("SUSPECT", "bad"), "unanimous"],
                       ["red1-03", "RUDY and global-route congestion maps disagree (ICCAD04 risc2)",
                        ("SUSPECT", "bad"), ("SUSPECT", "bad"), ("S-W-RES", "ok"), "strong concern"],
                       ["red1-04", "GRT DRC cap (10000) hides hotspots and macro overlaps",
                        ("SUSPECT", "bad"), ("S-W-RES", "ok"), ("SUSPECT", "bad"), "split"],
                       ["red1-05", "repair_timing ODB-1200 with Liberty Q&rarr;QN arcs",
                        ("SUSPECT", "bad"), ("S-W-RES", "ok"), ("S-W-RES", "ok"), ""],
                       ["red1-06", "TritonCTS segfault when Liberty has no max_capacitance",
                        ("SUSPECT", "bad"), ("S-W-RES", "ok"), ("SUSPECT", "bad"), "split"],
                       ["red1-07", "CTS NDRs on heavily gated clocks (level definition)",
                        ("SUSPECT", "bad"), ("S-W-RES", "ok"), ("SUSPECT", "bad"), "split"],
                       ["red1-08", "asap7 cva6 hier-synth GRT report references a nonexistent net",
                        ("SUSPECT", "bad"), ("S-W-RES", "ok"), ("S-W-RES", "ok"), ""],
                       ["red1-09", "STA false hold/setup: ideal top clock mixed with propagated macro clock",
                        ("S-W-RES", "ok"), ("S-W-RES", "ok"), ("S-W-RES", "ok"), "unanimous; strongest record"],
                       ["red1-10", "GPL regression: too-early non-virtual TD iteration makes design unroutable",
                        ("SUSPECT", "bad"), ("S-W-RES", "ok"), ("S-W-RES", "ok"), "deepseek strictest"]],
                      highlight_col=2)
              + '<div class="legend">Thirty files, thirty first-try parses, thirty complete seven-key objects, '
                'zero renamed or extra keys. Verdict distribution: <b>15 SUSPECT</b>, <b>15 '
                'SOUND-WITH-RESERVATIONS</b>. No <code>SOUND</code>, no <code>IMPLAUSIBLE</code>. '
                '<b>Zero fatal objections</b> across all thirty reviews. deepseek flagged SUSPECT on nine of ten '
                'blocks; kimi and sonnet leaned SOUND-WITH-RESERVATIONS. The models agree on which records are '
                'strong and which are thin.</div>')
    + section("What it found", "The contract held and the disagreement was the finding",
              verdict_pair(
                  "<code>deepseek</code>",
                  "Produced the most objections, 26 with 20 major, and was the strictest model on two of the "
                  "ten blocks.",
                  "<code>sonnet</code>",
                  "The least strict model: 8 major objections out of 22, and 4 blocks flagged suspect where "
                  "deepseek flagged 9.")
              + findings([
                  ("", "The literal template fixed the drift",
                   "Day 7 produced 0 of 15 schema compliance from a schema described in one line of prose. Day 8 "
                   "produced 30 of 30 from the same three models against a literal object to copy, with no renamed "
                   "or extra keys. The prompt family, the models and the chat surface were unchanged."),
                  ("", "No model invented content and none refused",
                   "Across thirty reviews there are no fabricated quotes, no invented tool or chip names, no "
                   "invented commits and no invented participants. No model browsed the web and none refused. The "
                   "field-level escape <code>not-determinable-from-this-record</code> was available, and every model "
                   "treated the pasted record as its whole evidence base."),
                  ("warn", "Zero fatal objections reflects the models&rsquo; caution",
                   "The enum offers two reserved values, <code>SUSPECT</code> and "
                   "<code>IMPLAUSIBLE-FOR-THIS-RECORD</code>. The second was never used by any of the three models "
                   "on any of the ten blocks. Every draft carries a known defect by construction, since the set was "
                   "stratified by failure type, and no model escalated past <code>SUSPECT</code>. The enum is wider "
                   "than the models&rsquo; willingness to convict."),
                  ("", "Unanimity tracked the record",
                   "Block 02 resolves the incident with the sentence &ldquo;solved on the latest version&rdquo;, no "
                   "commit and no PR, and drew <code>SUSPECT</code> from all three models. Block 09, the STA false "
                   "hold and setup record, is the best evidenced in the set and drew "
                   "<code>SOUND-WITH-RESERVATIONS</code> from all three. Where the three agree on which records are "
                   "thin, a human reviewer can start there."),
                  ("", "No model emitted a bare SOUND on block 01",
                   "This is the check the Day-5 codebook failed. Shortest-alias-first matching collapses "
                   "<code>SOUND-WITH-RESERVATIONS</code> into <code>SOUND</code> and manufactures a clean verdict. "
                   "Across all thirty files no model emitted a bare <code>SOUND</code>, so no grader had to collapse "
                   "a reserved verdict to reach one. <code>deepseek</code> reached <code>SUSPECT</code> on 9 of the "
                   "10 blocks."),
                  ("warn", "Three models from one generation is a narrow basis",
                   "<code>deepseek</code>, <code>kimi</code> and <code>sonnet</code> share training biases we cannot "
                   "see. Thirty reviews of ten drafts describe how those three read incident drafts. Three models "
                   "from one generation cannot stand for the web field. The drafts are first-generation mining "
                   "with no expert review yet, and if "
                   "that review changes them these verdicts describe the old versions."),
              ]))
    + section("Source files", "Where the evidence lives",
              srcs(["Web Model Tasks/Day 8/ (30 files, deepseek &middot; kimi &middot; sonnet &times; red1-01..10)",
                    "digest/wave1-report.md &mdash; the Day-8 report",
                    "prompts/J-ISSUE-REDTEAM-V1.md (JI-v1.2)",
                    "prompts/_paste/redteam/red1-01.paste.md &hellip; red1-10.paste.md",
                    "prompts/_paste/redteam/MANIFEST-PASTE-RT.sha256",
                    "digest/_verify/flash_d6_harvest.py &rarr; d6run/d6harvest.json",
                    "redteam/TALLY-34.md &mdash; staged tally", "RUNSHEET-34.md &mdash; the 34-draft sheet"]))
)


# ============================================================================
# CLOSING PURPOSE PANEL
# ============================================================================

# The panel appears on the index ("All Days") only — one instance, not one per day.
# Target length is ~370 words: long enough for the whole rationale, short enough to read
# in one sitting. The financial-regulation control paragraph is the answer to "why is a
# semiconductor benchmark running mortgage-disclosure arithmetic?" — keep it.
PURPOSE = purpose(
    "Why this exists",
    "A ground-truth check on the AI most people actually use",
    ["Free web chat models are what most people use, and almost nothing published about them "
     "measures the product a person gets in a browser tab. Published evaluations run a model through an "
     "API, inside a harness, temperature pinned. Every number below comes from a browser tab.",
     "So we chose tasks whose answers can be checked without trusting the model. "
     "Financial-regulation calculations were recomputed from the primary text. Recall slices were "
     "scored against the papers themselves. Incident reviews were judged against a record that was "
     "its own evidence base.",
     "The financial family is the control. It is the same kind of task as the semiconductor "
     "calculations in this corpus, a deterministic rule behind a citable clause. Its figures are "
     "published and its answers already checked, so a wrong response can be demonstrated by pointing "
     "at the number.",
     "We ask about semiconductors because we hold the primary sources. An EDA incident arrives with its "
     "bug-tracker thread; an architecture claim sits in a public paper. A reply can be checked against "
     "that record rather than our judgement, and the terminology is narrow enough that a bluff is obvious.",
     "We re-ran the work where the answer allowed it: about 720 calculations on Day 2, and the RFC "
     "8785 vectors diffed against a reference canonicalizer. A wrong number stays wrong however the "
     "response is worded, which is not true of a score awarded by another model.",
     "We also wanted to keep apart two failures usually blended into one score. A response that "
     "ignores a format contract has failed at <b>delivery</b>, and its reasoning may have been sound. "
     "A delivery failure is repaired with a template. A reasoning failure needs a different model. "
     "Day 7 and Day 8 are the same models on the same prompt "
     "family with opposite results, which is only visible if you keep them apart.",
     "Nothing here needed a budget. Every prompt is on disk and every reply was saved verbatim, so anyone "
     "with a browser can re-run a block and compare. The method does not ask the reader to trust us.",
     "The thirty red-team verdicts have not been reviewed by a physical-design expert yet. The sweep "
     "also ran on three models from one generation, so it describes those three models on ten drafts. "
     "Nothing wider follows."],
    "This is a pre-screen. A physical-design expert has not reviewed the thirty verdicts yet. No episode in "
    "this corpus invented a chip, a company or a person. Where a number could be measured from the response "
    "files rather than read out of a summary, it was measured."
)


# ============================================================================
# WRITE
# ============================================================================

TITLES = {
    "index": "Free web AI red-team benchmark",
    "day1": "Day 1 &middot; Exploration",
    "day2": "Day 2 &middot; Compliance batch",
    "day3": "Day 3 &middot; Five families",
    "day4": "Day 4 &middot; Paper recall",
    "day5": "Day 5 &middot; Five instruments",
    "day6": "Day 6 &middot; Citation and deployment",
    "day7": "Day 7 &middot; Format drift",
    "day8": "Day 8 &middot; The sweep",
}

BODIES = {"index": INDEX, "day1": DAY1, "day2": DAY2, "day3": DAY3, "day4": DAY4,
          "day5": DAY5, "day6": DAY6, "day7": DAY7, "day8": DAY8}

os.makedirs(OUT, exist_ok=True)
total = 0
for fid, _label in DAYS:
    body = BODIES[fid]

    # Splice the chart section in directly after the hero, so the ranking is the
    # first thing a reader meets and the detail sections follow it.
    if fid == "index":
        charts = index_charts()
    else:
        cfg = dict(CHARTS[fid])
        if cfg.get("neutral"):
            cfg["legend"] = [(C_TEAL, "strictness, not an accuracy rank")]
        else:
            cfg["legend"] = [(C_GREEN, "top value group"), (C_RED, "bottom value group"),
                             (C_TEAL, "between")]
        charts = [bar_chart(**cfg)]
    sec = chart_section(fid, charts)
    anchor = '<section class="panel"'
    i = body.find(anchor)
    if i < 0:
        raise SystemExit("no section anchor on %s — chart not inserted" % fid)
    body = body[:i] + sec + body[i:]

    tail = PURPOSE if fid == "index" else ""
    html = page(fid, TITLES[fid], body + tail)
    path = os.path.join(OUT, fid + ".html")
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(html)
    n = len(html.encode("utf-8"))
    total += n
    print("%-8s %8d bytes  %s" % (fid, n, path))

print("-" * 62)
print("%d pages, %d bytes total (%.1f KB)" % (len(DAYS), total, total / 1024.0))
