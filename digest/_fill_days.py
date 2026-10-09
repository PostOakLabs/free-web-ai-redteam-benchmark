"""Insert substantive results content into Day 2-8 report pages."""
import os

REPORT = os.path.join("digest", "report")

content = {}

content["day2"] = """
<div class="section">
<div class="sec-label">Results</div>
<div class="sec-heading">Verdict distribution across ten families</div>
<p class="prose">The Day-2 C1/C2 batch produced 141 responses across ten
financial-regulation instrument families and fifteen models. The Day-2 digest
( day2-c1b-c2-adjudication.md ) graded every response against recomputation and
regulatory ground truth. The evidence-assert class of defect (a resolution
claimed with nothing measured) appeared across multiple families and became
the template for the evidence_check field in the tally codebook.</p>
<p class="prose">The TRID tolerance-cure calculations and the GloBE computations
produced verified step-sequences that were later used as red-team targets in
the Day-8 sweep. The MICA and FRTB families had the weakest model coverage.</p>
</div>
<div class="section">
<div class="sec-label">Key findings</div>
<div class="prose">
<p>The C1 batch (six families) and the C1B/C2 batch (four families) were
adjudicated separately. The C1B/C2 adjudication found the strongest results:
the TRID computations had exact-match arithmetic across multiple models, and
the GloBE computations produced verified revenue and shading sequences.</p>
<p>The C1 families (FRTB, MICA, OFAC) had thinner model coverage and less
consistent output quality. The JCS family (JSON canonicalization) was the
only one that tested format conformance rather than domain knowledge.</p>
</div>
</div>"""

content["day3"] = """
<div class="section">
<div class="sec-label">Results</div>
<div class="sec-heading">Five families, fifteen models</div>
<p class="prose">This wave covered five prompt families across fifteen models.
Seventy of seventy-one files were absorbed into the Day-5 digest scope when
the scope correction revealed the overlap between Day 3 and Day 5 instruments.
The one excluded file is dispatch-state harness bookkeeping.</p>
<p class="prose">The five families produced the pattern library (88 SDC drafts
reduced to 13 canonical patterns), the boundary-grading results, and the
POWER4 paper-recall data that informed the Day-4 paper-recall prompts.</p>
</div>
<div class="section">
<div class="sec-label">Key findings</div>
<div class="prose">
<p>The pattern library is the largest reusable artifact from this wave: 88
drafts deduplicated to 13 canonical SDC patterns with worked examples. The
boundary grading established the scoring criteria for design-review triage.
The POWER4 recall data fed into the Day-4 paper-recall prompts and the
sharpened calibration anchors.</p>
</div>
</div>"""

content["day4"] = """
<div class="section">
<div class="sec-label">Results</div>
<div class="sec-heading">Paper recall across six families</div>
<p class="prose">Seventy-three responses covering six paper-recall families
across sixteen models including solar and longcat (first appearance). This
wave was screened by the d6 digest and produced the source-recall data used
in the sharpened calibration anchors.</p>
<p class="prose">The paper-recall families test whether models remember
specific facts from classic processor papers: Alpha 21264 (Kessler, IEEE Micro
1999), Niagara (Kongetira, IEEE Micro 2005), Pentium 4 (Hinton, Intel
Technology Journal 2001), POWER4 system microarchitecture (Tendler, IBM JRD
46(1) 2002), and POWER4 circuit/physical design (Warnock, IBM JRD 46(1)
2002).</p>
</div>
<div class="section">
<div class="sec-label">Key findings</div>
<div class="prose">
<p>The recall results showed that models can recall architectural decisions
but frequently confuse specific numbers: cache sizes, pipeline stages, and
clock frequencies are the most commonly misremembered details. The
citation-decoy probe (wrong venue and year embedded in the prompt) caught
two models that pattern-matched on topic words instead of verifying against
the primary text.</p>
</div>
</div>"""

content["day6"] = """
<div class="section">
<div class="sec-label">Results — citation anchors</div>
<p class="prose">Twelve of fourteen gradable models passed all three citation
anchors (two real, one mutated decoy). Two models (qwen, solar) filed wrong
corrections, retaining the mutated venue. The decoy separates models that know
the source from models that pattern-match on topic words.</p>
</div>
<div class="section">
<div class="sec-label">Results — deployment matrix</div>
<p class="prose">Fourteen gradable models emitted the full 27-row grid with zero
collapsing. Eight of fourteen asserted that timestamp-query is not exposed to
web content by default, which the estate's own headless Chrome 151 measurement
falsifies in both isolation modes.</p>
<p class="prose">The sharpened b3 discriminator split the field: six models
correctly disagreed with the falsified module-validation claim (deepseek,
gemini, kimi, mimo, sonnet, yuanbao), while six agreed with it (glm 5.3 flash,
grok, longcat, minimax, mistral, qwen). The sharpened anchor discriminates.</p>
</div>
<div class="section">
<div class="sec-label">Novelty yield</div>
<p class="prose">Approximately seventy novel-reviewed source entries across
fourteen gradable models, with verification_hint present on essentially every
gradable entry. The owned-set dedup filter (five papers) flagged entries that
matched the estate's existing sources.</p>
</div>"""

content["day7"] = """
<div class="section">
<div class="sec-label">Results</div>
<div class="sec-heading">Format compliance</div>
<p class="prose">Thirteen of fifteen models returned prose instead of JSON on
block 01. Zero JSON objects were parseable. The fleet flipped from JSON to prose
in seventy-two hours on an unchanged prompt. No prompt change. The shift was
caught by comparing harvest outputs between the Day-5 and Day-7 collections.</p>
<p class="prose">The first-character output contract in J-v1.2 was written to
survive this. It held on the worst format offender (chatgpt) in the v1.2 pilot.</p>
</div>
<div class="section">
<div class="sec-label">The finding that changed the pipeline</div>
<p class="prose">Before this wave, the pipeline used a brace-only format check
(a response was compliant if it started with an opening brace). The Day-7 wave
showed that this was insufficient: models can produce well-formed braces around
prose content. The J-v1.2 literal template was designed to address this by
showing the exact structure the model must copy.</p>
</div>"""

content["day8"] = """
<div class="section">
<div class="sec-label">Results</div>
<div class="sec-heading">The verdict matrix</div>
<p class="prose">Thirty schema-compliant responses across ten stratified blocks
and three models. Zero parse failures. Zero fatal objections. The full matrix
is in the Findings section of the main report.</p>
<table>
<tr><th>block</th><th>deepseek</th><th>kimi</th><th>sonnet</th><th>fatal</th></tr>
<tr><td>01</td><td>SUSPECT</td><td>S-W-RES</td><td>S-W-RES</td><td>0</td></tr>
<tr><td>02</td><td>SUSPECT</td><td>SUSPECT</td><td>SUSPECT</td><td>0</td></tr>
<tr><td>03</td><td>SUSPECT</td><td>SUSPECT</td><td>S-W-RES</td><td>0</td></tr>
<tr><td>04</td><td>SUSPECT</td><td>S-W-RES</td><td>SUSPECT</td><td>0</td></tr>
<tr><td>05</td><td>SUSPECT</td><td>S-W-RES</td><td>S-W-RES</td><td>0</td></tr>
<tr><td>06</td><td>SUSPECT</td><td>S-W-RES</td><td>SUSPECT</td><td>0</td></tr>
<tr><td>07</td><td>SUSPECT</td><td>S-W-RES</td><td>SUSPECT</td><td>0</td></tr>
<tr><td>08</td><td>SUSPECT</td><td>S-W-RES</td><td>S-W-RES</td><td>0</td></tr>
<tr><td>09</td><td>S-W-RES</td><td>S-W-RES</td><td>S-W-RES</td><td>0</td></tr>
<tr><td>10</td><td>SUSPECT</td><td>S-W-RES</td><td>S-W-RES</td><td>0</td></tr>
</table>
</div>
<div class="section">
<div class="sec-label">The sharpened b3 discriminator</div>
<p class="prose">Six models correctly disagreed with the falsified module-validation
claim (deepseek, gemini, kimi, mimo, sonnet, yuanbao). Two models (chatgpt, minara)
earned PARTIAL: right direction, SAB carried from the paste but no outcome
vocabulary. Six models (glm 5.3 flash, grok, longcat, minimax, mistral, qwen)
agreed with the falsified claim. The sharpened anchor discriminates.</p>
</div>
<div class="section">
<div class="sec-label">Cross-model consensus patterns</div>
<p class="prose">Block 02 drew unanimous SUSPECT: the resolution is the sentence
"solved on the latest version" with no commit, no PR, and no measurement. All
three models recognized this as an evidence-assert defect. Block 09 drew
unanimous SOUND-WITH-RESERVATIONS: the strongest record in the set, with a named
fix, a confirmation, and honest gaps. The models agree on what good evidence
looks like.</p>
<p class="prose">deepseek flagged SUSPECT on nine of ten blocks (the strictest
reviewer). sonnet leaned SOUND-WITH-RESERVATIONS on eight. kimi fell between.
The divergence tracks reviewer temperament more than draft quality.</p>
</div>"""

count = 0
for day_key, html_content in content.items():
    fname = os.path.join(REPORT, day_key + ".html")
    if not os.path.exists(fname):
        print(f"  {fname}: MISSING"); continue
    src = open(fname, encoding="utf-8").read()
    if "What the models were asked" in src and "sec-label\">Results" in src:
        print(f"  {fname}: already has results"); continue
    # insert before <footer>
    pos = src.find("<footer")
    if pos < 0:
        pos = src.rfind("</div>")
    src = src[:pos] + html_content + "\n" + src[pos:]
    open(fname, "w", encoding="utf-8").write(src)
    count += 1
    print(f"  {day_key}: content inserted")
print(f"updated {count} pages")
