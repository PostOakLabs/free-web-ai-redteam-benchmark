"""Generate the multi-day report pages. Run from ASIC root."""
import os

OUT = os.path.join("digest", "report")
os.makedirs(OUT, exist_ok=True)

CSS = """<style>
:root{--bg:#080E1A;--bg2:#0D1627;--bg3:#111E35;--bd:#1E2F4A;--mut:#3A5270;--body:#6888A8;--txt:#A8C4DE;--wht:#EEF6FD;--teal:#14B8A6;--gold:#D4A847;--fb:sans-serif;--fh:'DM Serif Display',serif;--fm:monospace}
*{box-sizing:border-box;margin:0;padding:0}
body{background:var(--bg);color:var(--body);font:15px/1.6 var(--fb)}
a{color:var(--teal);text-decoration:none}
.c{max-width:960px;margin:0 auto;padding:0 1.5em}
.hdr{background:var(--bg2);border-bottom:1px solid var(--bd);padding:.8em 0}
.hdr .c{display:flex;align-items:center;gap:1.2em}
.wm{font-family:'DM Serif Display',serif;font-size:1.3em;color:var(--wht)}
.wm span{color:var(--teal)}
nav{display:flex;gap:1.5em;margin-left:auto}
nav a{font-size:.85em;color:var(--body);text-transform:uppercase;letter-spacing:.06em}
nav a:hover,nav a.cur{color:var(--teal)}
h1{font-family:var(--fh);font-size:2em;color:var(--wht);font-weight:400;margin:1.2em 0 .4em}
h2{font-family:var(--fh);font-size:1.3em;color:var(--wht);margin:1.5em 0 .6em;font-weight:400}
h3{font-size:.95em;color:var(--teal);margin:1em 0 .4em;text-transform:uppercase;letter-spacing:.04em}
p{margin:.6em 0}
.card{background:var(--bg2);border:1px solid var(--bd);border-radius:8px;padding:1.2em;margin:.8em 0}
table{border-collapse:collapse;width:100%;margin:.8em 0;font-size:.88em;font-family:var(--fm)}
th{background:var(--bg3);color:var(--txt);padding:.5em .7em;text-align:left;font-size:.85em}
td{border:1px solid var(--bd);padding:.4em .6em;color:var(--body)}
.tr{color:var(--mut);font-size:.82em;font-family:var(--fm);margin:.3em 0}
.tag{display:inline-block;padding:.15em .5em;border-radius:4px;font-size:.82em;font-family:var(--fm);margin-right:.3em}
.t-ok{background:rgba(74,222,128,.12);color:#4ade80}
.t-warn{background:rgba(251,191,36,.12);color:#fbbf24}
.t-fail{background:rgba(255,107,107,.12);color:#ff6b6b}
.t-info{background:rgba(96,165,250,.08);color:#60a5fa}
.ftr{border-top:1px solid var(--bd);margin-top:3em;padding:2em 0;text-align:center;font-size:.82em;color:var(--mut)}
.dt{font-family:var(--fm);font-size:.82em;color:var(--mut);margin:.3em 0}
.nav-cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:.8em;margin:1.5em 0}
.nav-cards a{display:block;background:var(--bg2);border:1px solid var(--bd);border-radius:8px;padding:1em;color:var(--txt)}
.nav-cards a:hover{border-color:var(--teal)}
.nav-cards .n{font-family:var(--fm);font-size:.8em;color:var(--teal)}
.nav-cards .t{font-size:1em;font-weight:600;margin:.3em 0}
.nav-cards .s{font-size:.82em;color:var(--mut)}
.hl{background:rgba(20,184,166,.06);border-left:3px solid var(--teal);padding-left:1em;margin:1em 0}
</style>"""

DAYS = [
    ("day1", "Day 1: Exploration", "Collected 2026-08-31", "231 files, 19 prompts, 17+ models", """<p>The widest net. Nineteen prompt suffixes (A through T plus dispatch rounds), seventeen-plus model names including nemotron and opus 5. This wave mapped the territory.</p>
<h2>What it produced</h2>
<p>The original digest graded 233 files across eighteen slices, totalling 1,550 JSON items. Key findings: meta scored 25/25 across five papers. chatgpt scored 92% recall with excellent arithmetic. glm 5.3 flash submitted the same Alpha 21264 text for eight different prompts (well-formed JSON, entirely wrong content). mistral's inverted SPFM formula reported 95% where the correct value is 3%.</p>
<h2>Per-model reliability (early wave)</h2>
<table><tr><th>model</th><th>recall</th><th>arithmetic</th><th>verdict</th></tr>
<tr><td>meta</td><td>100%</td><td>EXCELLENT</td><td>First call</td></tr>
<tr><td>chatgpt</td><td>92%</td><td>EXCELLENT</td><td>Deterministic math</td></tr>
<tr><td>yuanbao</td><td>92%</td><td>EXCELLENT</td><td>Recall + math</td></tr>
<tr><td>grok</td><td>92%</td><td>MIXED</td><td>Recall yes, math spot-check</td></tr>
<tr><td>sonnet</td><td>100% (low vol)</td><td>GOOD</td><td>Verifier</td></tr>
<tr><td>qwen</td><td>100% (low vol)</td><td>POOR formula, GOOD honesty</td><td>Recall-verifier only</td></tr>
<tr><td>gemini</td><td>88%</td><td>MIXED</td><td>Structure only</td></tr>
<tr><td>kimi</td><td>79%</td><td>GOOD</td><td>Generative, mid-tier</td></tr>
<tr><td>deepseek</td><td>80%</td><td>MIXED</td><td>Generative, spot-check</td></tr>
<tr><td>minimax 2.7</td><td>38%</td><td>GOOD arithmetic</td><td>Drop (4 integrity failures)</td></tr>
<tr><td>minimax m3</td><td>38%</td><td>Convention-divergent</td><td>Drop</td></tr>
<tr><td>mistral</td><td>—</td><td>DISQUALIFYING</td><td>Drop from all math</td></tr>
<tr><td>glm 5.3 flash</td><td>10%</td><td>NOT ASSESSABLE</td><td>Suspend (wrong content x8)</td></tr>
<tr><td>mimo</td><td>63% (prose)</td><td>—</td><td>Undeliverable</td></tr></table>
<div class="hl"><p><strong>Three lessons that outlive the corpus:</strong> Consensus is not evidence. Recomputation catches one failure shape out of three. Delivery failures masquerade as reasoning failures.</p></div>"""),

    ("day2", "Day 2: Compliance batch", "Collected 2026-09-01", "141 files, 15 models, 10 families", """<p>Ten financial-regulation instrument families: APPJ, CCD2, FRTB, Globe, IRB, MICA, OFAC, Receipt, TRID, JCS. This wave produced the compliance-calculation findings and the verdict-severity data.</p>
<h2>What it produced</h2>
<p>The Day-2 digest graded these responses against recomputation and regulatory ground truth. The evidence-assert class of defect appears across multiple families. The TRID tolerance-cure calculations and the GloBE computations produced verified step-sequences.</p>"""),

    ("day3", "Day 3: Five families", "Collected 2026-09-02 to 2026-09-04", "71 files, 15 models, 5 families", """<p>APRC, boundary, library, patterns, power4 across fifteen models. Seventy of seventy-one files were covered by the digest scope correction.</p>
<h2>What it produced</h2>
<p>The pattern library (88 drafts reduced to 13 canonical patterns), the boundary grading results, and the POWER4 paper-recall data.</p>"""),

    ("day4", "Day 4: Paper recall", "Collected 2026-09-04 and 2026-09-08", "73 files, 16 models, 6 families", """<p>Six families: Alpha 21264, Niagara, Pentium 4, POWER4 physical, POWER4 system recall, and LVS mismatch classes. Sixteen models including solar and longcat (first appearance).</p>
<h2>What it produced</h2>
<p>Source-recall data for the five papers and the novel-source candidates. This wave was screened by the d6 digest.</p>"""),

    ("day5", "Day 5: Five instruments", "Collected 2026-09-08 to 2026-09-09", "80 files, 17 model names, 5 instruments", """<p>Reg Z (exact arithmetic), strings (JCS conformance), e (HW-safety calculations), red1 + red3 (calibration blocks). Seventeen model names including minara and minaria (later resolved as one model).</p>
<h2>What it produced</h2>
<p>The fully digested and vetted wave. Twelve models scored 9/9 on Reg Z arithmetic. Five scored 4/4 on JCS. Five were flagged for bare-SOUND miscalibration. Six agreed with a falsified validation claim. The digest survived a two-station adversarial review that found four tool defects and one retracted inference.</p>"""),

    ("day6", "Day 6: Citation + deployment", "Collected 2026-09-11", "32 files, 16 models, 2 instruments", """<p>C-v5 citation anchors + B-v8 deployment matrix. Twelve of fourteen models pass citation anchors. Fourteen emit the full 27-row deployment grid. Eight assert the falsified timestamp-query claim. The sharpened b3 discriminator split the field 6 pass-mech / 6 falsified / 2 PARTIAL.</p>
<h2>What it produced</h2>
<p>The B-v8 deployment matrix, the citation-decoy calibration data, and the format-drift finding. This wave was 100% schema-compliant with zero parse failures.</p>"""),

    ("day7", "Day 7: Format drift", "Collected 2026-09-14", "16 files, 15 models, 1 block", """<p>Fifteen models ran block 01 under J-v1.1. Thirteen returned prose instead of JSON. The fleet flipped from JSON to prose in three days on an unchanged prompt.</p>
<h2>What it produced</h2>
<p>The format-drift finding. The first-character contract and the literal template were designed to survive this class of failure.</p>"""),

    ("day8", "Day 8: The sweep", "Collected 2026-09-14", "30 files, 3 models, 10 blocks", """<p>Ten stratified blocks × three models. All thirty returned schema-compliant JSON with zero parse failures and zero fatal objections. The verdict matrix and the calibration discriminator are in the findings.</p>
<h2>What it produced</h2>
<p>The per-model reliability matrix, the sharpened b3 discriminator results, and the citation-decoy calibration data.</p>"""),

    ("models", "Model reliability across all waves", "Combined from all instruments", "16 models, multiple instruments", """<p>This page combines every truth-anchored measurement. Tables are separated by wave.</p>

<h2>Early wave (Days 1-3)</h2>
<table><tr><th>model</th><th>recall</th><th>arithmetic</th><th>verdict</th></tr>
<tr><td>meta</td><td>100%</td><td>EXCELLENT</td><td>First call</td></tr>
<tr><td>chatgpt</td><td>92%</td><td>EXCELLENT</td><td>Deterministic math</td></tr>
<tr><td>yuanbao</td><td>92%</td><td>EXCELLENT</td><td>Recall + math</td></tr>
<tr><td>grok</td><td>92%</td><td>MIXED</td><td>Recall yes, math spot-check</td></tr>
<tr><td>sonnet</td><td>100% (low vol)</td><td>GOOD</td><td>Verifier</td></tr>
<tr><td>qwen</td><td>100% (low vol)</td><td>POOR formula</td><td>Recall-verifier</td></tr>
<tr><td>gemini</td><td>88%</td><td>MIXED</td><td>Structure only</td></tr>
<tr><td>kimi</td><td>79%</td><td>GOOD</td><td>Generative, mid-tier</td></tr>
<tr><td>deepseek</td><td>80%</td><td>MIXED</td><td>Generative, spot-check</td></tr>
<tr><td>minimax 2.7</td><td>38%</td><td>GOOD arithmetic</td><td>Drop</td></tr>
<tr><td>mistral</td><td>—</td><td>DISQUALIFYING</td><td>Drop from math</td></tr>
<tr><td>glm 5.3 flash</td><td>10%</td><td>NOT ASSESSABLE</td><td>Suspend</td></tr></table>

<h2>B-v8 deployment matrix (Day 6)</h2>
<table><tr><th>model</th><th>b2</th><th>b3</th></tr>
<tr><td>kimi</td><td>correct</td><td>pass-mech</td></tr>
<tr><td>sonnet</td><td>correct</td><td>pass-mech</td></tr>
<tr><td>deepseek</td><td>correct</td><td>pass-mech</td></tr>
<tr><td>yuanbao</td><td>correct</td><td>pass-mech</td></tr>
<tr><td>mimo</td><td>correct</td><td>pass-mech</td></tr>
<tr><td>minara</td><td>correct</td><td>PARTIAL</td></tr>
<tr><td>chatgpt</td><td>WRONG</td><td>PARTIAL</td></tr>
<tr><td>grok</td><td>correct</td><td>falsified</td></tr>
<tr><td>gemini</td><td>WRONG</td><td>pass-mech</td></tr>
<tr><td>meta</td><td>correct</td><td>falsified</td></tr>
<tr><td>longcat</td><td>WRONG</td><td>falsified</td></tr>
<tr><td>qwen</td><td>WRONG</td><td>falsified</td></tr>
<tr><td>solar</td><td>WRONG</td><td>pass-mech</td></tr>
<tr><td>minimax 2.7</td><td>WRONG</td><td>falsified</td></tr>
<tr><td>mistral</td><td>WRONG</td><td>falsified</td></tr></table>

<h2>What the combined data shows</h2>
<p>No model is strong on every instrument. kimi and sonnet are the most consistent. deepseek has the strongest mechanism reasoning but a transcription slip on arithmetic. The falsified-belief cluster is stable across waves and instruments.</p>"""),
]

TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} | AINumbers Research</title>
{css}
</head>
<body>
<header><div class="c">
<span class="wm">AI<span style="color:var(--teal)">Numbers</span> <span style="font-size:.6em;color:var(--mut)">Research</span></span>
<nav>{nav}</nav>
</div></header>
<div class="c">
<h1>{title}</h1>
<div class="dt">{date} · {meta}</div>
{body}
</div>
<footer><div class="c"><p>AINumbers Research · Free Web AI Red-Team Benchmark · 2026-09</p><p>Static snapshot. No scripts, no network calls, no tracking.</p></div></footer>
</body>
</html>"""

for fname, title, date, meta, body in DAYS:
    nav_items = []
    for f, label, _, _, _ in DAYS:
        cls = ' style="color:var(--teal)"' if f == fname else ""
        nav_items.append(f'<a href="{f}.html"{cls}>{label}</a>')
    nav = "\n".join(nav_items)
    html = TEMPLATE.format(title=title, css=CSS, nav=nav, date=date, meta=meta, body=body)
    path = os.path.join(OUT, fname + ".html")
    open(path, "w", encoding="utf-8").write(html)
    print(f"  {fname}.html: {len(html)} bytes")

# also copy the index
import shutil
index_body = """
<p>Eight days of collection. Six instruments. Sixteen models.</p>
<div class="nav-cards">
<a href="day1.html"><div class="n">DAY 1</div><div class="t">Exploration</div><div class="s">231 files</div></a>
<a href="day2.html"><div class="n">DAY 2</div><div class="t">Compliance batch</div><div class="s">141 files</div></a>
<a href="day3.html"><div class="n">DAY 3</div><div class="t">Five families</div><div class="s">71 files</div></a>
<a href="day4.html"><div class="n">DAY 4</div><div class="t">Paper recall</div><div class="s">73 files</div></a>
<a href="day5.html"><div class="n">DAY 5</div><div class="t">Instruments</div><div class="s">80 files</div></a>
<a href="day6.html"><div class="n">DAY 6</div><div class="t">Citation + deployment</div><div class="s">32 files</div></a>
<a href="day7.html"><div class="n">DAY 7</div><div class="t">Format drift</div><div class="s">16 files</div></a>
<a href="day8.html"><div class="n">DAY 8</div><div class="t">The sweep</div><div class="s">30 files</div></a>
<a href="models.html"><div class="n">MODELS</div><div class="t">Reliability</div><div class="s">Cross-day matrix</div></a>
</div>
"""
page("index", "Free Web AI Red-Team Benchmark", "index", index_body)

print("Done. Files in", OUT)
for f in sorted(os.listdir(OUT)):
    print(f"  {f}: {os.path.getsize(os.path.join(OUT, f))} bytes")
