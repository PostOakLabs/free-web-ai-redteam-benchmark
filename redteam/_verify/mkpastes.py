"""mkpastes.py — generate the 76 dispatch-ready red-team paste files.

For each block: the prompt head (everything above the `---` rule, which is the paste)
with the exemplar region (RECORD/PAPER line + JSON fence) SUBSTITUTED by the block's own
RECORD/PAPER line + fence. Output: prompts/_paste/redteam/ + MANIFEST-PASTE-RT.sha256.

Byte guarantees:
  * redteam r1 block 01 == J-ISSUE-REDTEAM-V1 head verbatim (Block 01 IS its exemplar)
  * redteam r3 block 08 == J-EPISODE-REDTEAM-V3 head verbatim (Block 08 IS its exemplar)
Any generator change that breaks either identity is a defect, checked at build time.
"""
import os, re, hashlib

ASIC = r"C:\dev\Claude\Projects\ASIC"
RS34 = os.path.join(ASIC, "redteam", "RUNSHEET-34.md")
RS42 = os.path.join(ASIC, "redteam", "RUNSHEET-42.md")
J1 = os.path.join(ASIC, "prompts", "J-ISSUE-REDTEAM-V1.md")
J3 = os.path.join(ASIC, "prompts", "J-EPISODE-REDTEAM-V3.md")
OUT = os.path.join(ASIC, "prompts", "_paste", "redteam")
os.makedirs(OUT, exist_ok=True)

def prompt_head(path):
    raw = open(path, encoding="utf-8", newline="").read()
    m = re.search(r"\n---\r?\n", raw)
    return raw[:m.start() + 1]

def blocks(path, pattern):
    raw = open(path, encoding="utf-8", newline="").read()
    return re.findall(pattern, raw, re.S)

j1_head = prompt_head(J1)
j3_head = prompt_head(J3)

# J-v1's exemplar region: RECORD line + following ```json fence
r1_blocks = blocks(RS34, r"(RECORD: [^\n]*\n+```json\n.*?\n```)")
# J-v3's exemplar region: PAPER line + following ```json fence
r3_blocks = blocks(RS42, r"(PAPER: [^\n]*\n+```json\n.*?\n```)")

assert len(r1_blocks) == 34, f"RUNSHEET-34: {len(r1_blocks)} blocks"
assert len(r3_blocks) == 42, f"RUNSHEET-42: {len(r3_blocks)} blocks"

# substitution region in each prompt head (first occurrence)
J1_REGION = re.compile(r"RECORD: [^\n]*\n+```json\n.*?\n```", re.S)
J3_REGION = re.compile(r"PAPER: [^\n]*\n+```json\n.*?\n```", re.S)

j1_head_new = J1_REGION.sub("@@BLOCK@@", j1_head, count=1)
j3_head_new = J3_REGION.sub("@@BLOCK@@", j3_head, count=1)

def make(head_template, block):
    return head_template.replace("@@BLOCK@@", block)

# byte guarantees: block 01 (r1) and block 08 (r3) must reproduce the prompt heads exactly
assert make(j1_head_new, r1_blocks[0]) == j1_head, "r1-01 != J-v1 head (exemplar identity broken)"
assert make(j3_head_new, r3_blocks[7]) == j3_head, "r3-08 != J-v3 head (exemplar identity broken)"

entries = []
for i, block in enumerate(r1_blocks, start=1):
    name = f"red1-{i:02d}.paste.md"
    body = make(j1_head_new, block)
    open(os.path.join(OUT, name), "wb").write(body.encode("utf-8"))
    entries.append((name, body))
for i, block in enumerate(r3_blocks, start=1):
    name = f"red3-{i:02d}.paste.md"
    body = make(j3_head_new, block)
    open(os.path.join(OUT, name), "wb").write(body.encode("utf-8"))
    entries.append((name, body))

man = os.path.join(OUT, "MANIFEST-PASTE-RT.sha256")
with open(man, "w", encoding="utf-8", newline="\n") as fh:
    for name, body in sorted(entries):
        fh.write(hashlib.sha256(body.encode("utf-8")).hexdigest() + " *" + name + "\n")

print(f"generated {len(entries)} paste files in prompts/_paste/redteam/")
print("identity checks: r1-01 == J-v1 head, r3-08 == J-v3 head — both hold")
