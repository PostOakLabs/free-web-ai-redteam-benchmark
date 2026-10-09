#!/usr/bin/env python3
"""DAY3-FOLD-NORMALIZE-1 deterministic loader.

Reads Web Model Tasks/Day 3/_digest/quarantine.json (the authority) and
applies, in order:
  1. fence-strip (unconditional)
  2. per-file transforms in repair_structural_only
  3. field-alias (quote_as_recall_verbatim -> quote_as_recalled)
  4. contamination strip per field_contamination
  5. exclude drop

Emits Day 3/_digest/normalized/<family>.json. Each file-level record carries
a _provenance block {file, model, family, parse_status, transforms_applied[],
excluded_fields[], truncated_bool, recovered_items, prompt_expects}.

STRUCTURAL ONLY: never edits content, never completes a truncated string,
never reconciles a fused object, never fills an ABSENT cell. The genuinely
missing cell (minimax m3 boundary rule 3 verdicts.at) is emitted as null
with "_absent": true.

Stdlib only. No network. Read-only on model outputs.
"""

import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DAY3 = os.path.dirname(HERE)  # Web Model Tasks/Day 3
OUTDIR = os.path.join(HERE, "normalized")

FAMILIES = ["aprc", "boundary", "power4", "library", "patterns"]
PROMPT_EXPECTS = {"aprc": 4, "boundary": 8, "power4": 5, "library": 10,
                  "patterns": 10}

CHATGPT_ESCAPE_KEYS = ["no_era_difference_recalled",
                       "no-era-difference_recalled",
                       "no-era-difference-recalled"]
MIMO_STRIP = ["not_in_paper", "paper_vs_general", "weakest_point"]
GLM_STRIP = ["not_in_paper"]


def read_text(path):
    with open(path, encoding="utf-8-sig") as f:
        return f.read()


def fence_strip(text):
    """Remove ```json fences (unconditional). Returns (stripped, applied)."""
    s = text.strip()
    applied = False
    if s.startswith("```"):
        applied = True
        # drop opening fence line
        nl = s.find("\n")
        s = s[nl + 1:] if nl != -1 else ""
        # content may hold a SECOND fenced block after the value (mimo aprc);
        # that is handled by read_trailing_fence, not here.
        end = s.rfind("```")
        if end != -1:
            s = s[:end]
        s = s.strip()
    # lone trailing fence marker with no opening fence (deepseek library.json
    # ends "]\\n```"): strip it structurally, record the transform.
    if s.endswith("```"):
        s = s[:s.rfind("```")].strip()
        applied = True
    return s, applied


def strip_trailing_nonjson(text):
    """chatgpt boundary.json: trailing reference-link footer after the value.
    Cuts from the first line starting with '[' outside the JSON value."""
    lines = text.split("\n")
    # find last line that is part of JSON: walk back past footer lines like [1]: http...
    cut = len(lines)
    for i, ln in enumerate(lines):
        if re.match(r"^\[\d+\]:\s*http", ln.strip()):
            cut = i
            break
    return "\n".join(lines[:cut]).strip()


def split_top_level_objects(text):
    """Greedy balanced-brace/bracket scan returning complete top-level {...}
    substrings of a JSON array body. Used for element-wise recovery of
    truncated files: only structurally complete objects are returned."""
    objs = []
    depth = 0
    in_str = False
    esc = False
    start = None
    for i, ch in enumerate(text):
        if in_str:
            if esc:
                esc = False
            elif ch == "\\":
                esc = True
            elif ch == '"':
                in_str = False
            continue
        if ch == '"':
            in_str = True
        elif ch == "{":
            if depth == 0:
                start = i
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0 and start is not None:
                objs.append(text[start:i + 1])
                start = None
    return objs


def recover_elements(text):
    """Element-wise recovery: return list of parsed complete top-level
    objects from an array that will not parse whole."""
    body = text.strip()
    if body.startswith("["):
        body = body[1:]
    # drop any partial tail: keep scanning complete objects only
    recovered = []
    for cand in split_top_level_objects(body):
        try:
            recovered.append(json.loads(cand))
        except json.JSONDecodeError:
            continue
    return recovered


def main():
    with open(os.path.join(HERE, "quarantine.json"), encoding="utf-8") as f:
        gate = json.load(f)

    exclude_files = {e["file"] for e in gate["exclude"]}
    truncated_info = {t["file"]: t for t in gate["truncated"]}

    # ---- enumerate Day 3 model files ----
    files = sorted(f for f in os.listdir(DAY3) if f.endswith(".json"))
    # family from "<model> <family>.json": family is last token before .json
    fam_of = {}
    for fn in files:
        stem = fn[:-len(".json")]
        fam = stem.rsplit(" ", 1)[-1]
        if fam in FAMILIES:
            fam_of[fn] = fam

    out = {fam: [] for fam in FAMILIES}
    fence_count = 0
    log = []

    for fn in sorted(fam_of):
        fam = fam_of[fn]
        model = fn[:-len(".json")].rsplit(" ", 1)[0] if " " in fn[:-len(".json")] else fn[:-len(".json")]
        # model = stem minus trailing family token
        stem = fn[:-len(".json")]
        model = stem[:-(len(fam) + 1)]
        path = os.path.join(DAY3, fn)
        raw = read_text(path)

        if fn in exclude_files:
            log.append(f"EXCLUDE drop: {fn}")
            continue

        transforms = []
        excluded_fields = []
        parse_status = "clean"
        truncated_bool = fn in truncated_info
        prompt_expects = PROMPT_EXPECTS[fam]

        text = raw
        s, fenced = fence_strip(text)
        if fenced:
            fence_count += 1
            transforms.append("fence-strip")
            parse_status = "fence-stripped"
            text = s

        record_extra = {}
        items = None
        weakest_point = None

        # ---------- family / file specific structural transforms ----------
        if fn == "minimax 2.7 power4.json":
            # unwrap-double-array [[{...}x5]]
            v = json.loads(text)
            if isinstance(v, list) and len(v) == 1 and isinstance(v[0], list):
                v = v[0]
                transforms.append("unwrap-double-array")
            # field alias quote_as_recall_verbatim -> quote_as_recalled
            for it in v:
                if isinstance(it, dict) and "quote_as_recall_verbatim" in it:
                    it["quote_as_recalled"] = it.pop("quote_as_recall_verbatim")
            transforms.append("field-alias:quote_as_recall_verbatim->quote_as_recalled")
            items = v
            parse_status = "recovered" if parse_status == "clean" else parse_status + "+recovered"

        elif fam == "boundary" and fn in ("deepseek boundary.json",
                                          "minimax m3 boundary.json"):
            if fn == "deepseek boundary.json":
                v = json.loads(text)
                weakest_point = v.get("weakest_point")
                items = v["rules"]
                transforms.append("unnest:rules")
            else:
                # minimax m3 boundary.json: unnest + pair-in-array salvage.
                # Rule 3 verdicts carries the malformed fragment
                #   "below": "at": "FIRE"
                # Structural salvage: the below VALUE was destroyed by the
                # seam; the surviving "FIRE" cannot be attributed to at vs
                # below. Per gate, verdicts.at is ABSENT -> null + _absent.
                # below is emitted as the literal surviving raw where
                # present; here the value slot is destroyed so below is
                # null WITHOUT _absent ruling (documented seam loss), at is
                # null WITH _absent:true per gate, above is "FIRE" as in bytes.
                v = json.loads(text.replace(
                    '"verdicts": {"below": "at": "FIRE", "above": "FIRE"}',
                    '"verdicts": {"below": null, "at": null, "above": "FIRE"}'))
                weakest_point = v.get("weakest_point")
                items = v["rules"]
                transforms.append("unnest:rules")
                transforms.append("salvage:rule3-seam below-value-destroyed; "
                                  "at->null+_absent per gate")
                parse_status = "recovered"
                for it in items:
                    if isinstance(it, dict) and it.get("rule") == 3:
                        it["_absent"] = {"verdicts.at": True}

        elif fam == "boundary":
            # list-shaped files; separate trailing non-rule objects
            # (weakest_point folded into the rules list)
            v = json.loads(strip_trailing_nonjson(text) if fn == "chatgpt boundary.json" else text)
            if fn == "chatgpt boundary.json":
                transforms.append("strip-trailing-nonjson")
            rules = []
            for el in v:
                if isinstance(el, dict) and "rule" not in el:
                    if weakest_point is None:
                        weakest_point = el.get("weakest_point")
                        record_extra["weakest_point_reason"] = el.get("reasoning", el.get("reason"))
                        transforms.append("separate-weakest_point-from-rules-list")
                    continue
                rules.append(el)
            if fn == "mistral boundary.json":
                for el in rules:
                    if isinstance(el.get("rule"), str):
                        el["rule"] = int(el["rule"])
                transforms.append("coerce-rule-key:str->int")
            items = rules

        elif fn == "mimo aprc.json":
            # leading prose + array fenced block + SECOND fenced block with
            # weakest_point. Work from raw: generic fence-strip would damage
            # the two-block structure.
            if "fence-strip" in transforms:
                transforms.remove("fence-strip")
            fence_blocks = re.findall(r"```(?:json)?\s*\n(.*?)```", raw, re.S)
            weakest_point = None
            array_text = None
            for blk in fence_blocks:
                blk = blk.strip()
                if blk.startswith("["):
                    array_text = blk
                else:
                    try:
                        tail = json.loads(blk)
                    except json.JSONDecodeError:
                        continue
                    if isinstance(tail, dict) and "weakest_point" in tail:
                        weakest_point = tail["weakest_point"]
            if weakest_point is not None:
                transforms.append("read-trailing-fence:weakest_point")
            v = json.loads(array_text)
            items = v
            transforms.append("strip-leading-prose")
            parse_status = "recovered"

        elif fn in ("minimax m3 aprc.json", "longcat library.json",
                    "minimax m3 library.json"):
            rec = recover_elements(text)
            transforms.append("element-wise-recovery")
            parse_status = "truncated-recovered"
            if fam == "aprc":
                # split recovered case objects from trailing non-case objects
                # (e.g. weakest_point); cases 2+3 sit inside the fused blob
                # and do not parse. Cases 1 and 4 are structurally complete.
                cases = [el for el in rec
                         if isinstance(el, dict) and "case" in el]
                rest = [el for el in rec
                        if not (isinstance(el, dict) and "case" in el)]
                for el in rest:
                    if isinstance(el, dict) and "weakest_point" in el \
                            and weakest_point is None:
                        weakest_point = el["weakest_point"]
                if rest:
                    record_extra["trailing_objects"] = rest
                    transforms.append(
                        f"separate-trailing-objects:{len(rest)}")
                record_extra["unparseable_fused"] = (
                    "cases 2+3 fused with no '},{' (char 4699); "
                    "case-2 aprc 30.5 present-but-unparseable per gate")
                items = cases
            else:
                items = rec
            log.append(f"TRUNCATED {fn}: recovered {len(items) if isinstance(items, list) else 0} of "
                       f"{truncated_info[fn]['prompt_expects']}")

        else:
            v = json.loads(text)
            if isinstance(v, dict) and "rules" in v:
                weakest_point = v.get("weakest_point")
                items = v["rules"]
                transforms.append("unnest:rules")
            elif isinstance(v, list):
                # generic: separate trailing non-case objects (sonnet aprc
                # 6-element list: 4 cases + financed note + weakest_point;
                # most other aprc files: 4 cases + weakest_point)
                if fam == "aprc" and isinstance(v, list) and all(
                        isinstance(el, dict) for el in v):
                    cases = [el for el in v if "case" in el]
                    rest = [el for el in v if "case" not in el]
                    for el in rest:
                        if "weakest_point" in el and weakest_point is None:
                            weakest_point = el["weakest_point"]
                    if rest:
                        transforms.append(
                            f"separate-trailing-objects:{len(rest)}")
                        record_extra["trailing_objects"] = rest
                    items = cases
                elif isinstance(v, list):
                    items = v
            else:
                items = v

        # ---------- contamination strip ----------
        if fn == "mimo library.json":
            for it in items:
                for fld in MIMO_STRIP:
                    if isinstance(it, dict) and fld in it:
                        del it[fld]
                        if fld not in excluded_fields:
                            excluded_fields.append(fld)
            transforms.append(f"contamination-strip:{MIMO_STRIP}")
        elif fn == "glm 5.3 flash library.json":
            for it in items:
                for fld in GLM_STRIP:
                    if isinstance(it, dict) and fld in it:
                        del it[fld]
                        if fld not in excluded_fields:
                            excluded_fields.append(fld)
            transforms.append(f"contamination-strip:{GLM_STRIP}")
        elif fn == "chatgpt library.json":
            # gate rule: IGNORE — escape keys sit beside populated prose.
            # Structural handling: drop the escape-token keys (they are not
            # schema fields), keep node_era_note prose untouched. Recorded.
            for it in items:
                if not isinstance(it, dict):
                    continue
                for fld in CHATGPT_ESCAPE_KEYS:
                    if fld in it:
                        del it[fld]
                        if fld not in excluded_fields:
                            excluded_fields.append(fld)
            transforms.append(f"contamination-ignore-removed:{CHATGPT_ESCAPE_KEYS}")

        # power4 generic alias (only minimax 2.7 carries the variant, but
        # alias is applied wherever the variant key appears)
        if fam == "power4" and isinstance(items, list):
            for it in items:
                if isinstance(it, dict) and "quote_as_recall_verbatim" in it \
                        and "quote_as_recalled" not in it:
                    it["quote_as_recalled"] = it.pop("quote_as_recall_verbatim")
                    if "field-alias:quote_as_recall_verbatim->quote_as_recalled" not in transforms:
                        transforms.append("field-alias:quote_as_recall_verbatim->quote_as_recalled")

        recovered_items = len(items) if isinstance(items, list) else 1
        rec = {
            "model": model,
            "file": fn,
            "items": items,
        }
        if weakest_point is not None:
            rec["weakest_point"] = weakest_point
        rec.update(record_extra)
        rec["_provenance"] = {
            "file": fn,
            "model": model,
            "family": fam,
            "parse_status": parse_status,
            "transforms_applied": transforms,
            "excluded_fields": excluded_fields,
            "truncated_bool": truncated_bool,
            "recovered_items": recovered_items,
            "prompt_expects": prompt_expects,
        }
        out[fam].append(rec)

    os.makedirs(OUTDIR, exist_ok=True)
    for fam in FAMILIES:
        out[fam].sort(key=lambda r: r["model"])
        with open(os.path.join(OUTDIR, f"{fam}.json"), "w",
                  encoding="utf-8") as f:
            json.dump(out[fam], f, indent=1, ensure_ascii=False)
            f.write("\n")

    counts = {fam: (len(out[fam]),
                    sum(r["_provenance"]["recovered_items"] for r in out[fam]))
              for fam in FAMILIES}
    print(json.dumps({"records_per_family": {k: v[0] for k, v in counts.items()},
                       "items_per_family": {k: v[1] for k, v in counts.items()},
                       "fence_wrapped_files": fence_count}, indent=1))
    for line in log:
        print(line)


if __name__ == "__main__":
    sys.exit(main())
