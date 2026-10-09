"""Animated SVG scenes for the benchmark day pages, one per page.

Each scene shows what that day's prompt asked a model to do. They are built on the
scene kit's classes (sk-fade, sk-pop, sk-slide, sk-draw, sk-strike; copied into
_staircase_kit.py), so motion is opt-in, every scene renders complete and still with
no JavaScript, in print and under prefers-reduced-motion, and all motion stops
within five seconds (WCAG 2.2.2). Importing this module checks that limit and
refuses to build a scene that runs longer.

Every number comes from the prompt it illustrates, with two exceptions that are
labelled on the scene: Day 2's fee table is illustrative, and Day 5's factor chain
was computed exactly from the Day-5 prompt's own figures (Python Decimal):
130461 / 124331 = 1.049304; 130461 x 1.034 = 134896.674, which rounds to 134897;
134841 / 130461 = 1.033573; (1.034 - 1.033573) x 10000 = 4.27 bps; 134897 - 134841 = 56.

Run directly to print each scene's motion length:  python _day_scenes.py
"""
import re

# Durations of the scene kit's one-shot animations, in seconds.
DUR = {"sk-draw": 0.9, "sk-fade": 0.6, "sk-pop": 0.5, "sk-slide": 0.7, "sk-strike": 0.4}
MAX_END = 5.0


def _d(v):
    return ("%.2f" % v).rstrip("0").rstrip(".")


def g(cls, d, inner, style=""):
    """A group that animates with one scene-kit class after a delay of d seconds."""
    return '<g class="%s" style="--d:%ss%s">%s</g>' % (cls, _d(d), (";" + style) if style else "", inner)


def t(x, y, s, cls="s sm", anchor=None, style=""):
    a = ' text-anchor="%s"' % anchor if anchor else ""
    st = ' style="%s"' % style if style else ""
    return '<text x="%s" y="%s" class="%s"%s%s>%s</text>' % (x, y, cls, a, st, s)


def rect(x, y, w, h, stroke="var(--border-2)", fill="var(--bg-3)", rx=8, sw=1.4):
    return ('<rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="%s" stroke="%s" stroke-width="%s"/>'
            % (x, y, w, h, rx, fill, stroke, sw))


def arrow(x1, y, x2, d, color="var(--muted)"):
    """A line that draws in from x1 to x2, then its arrowhead appears."""
    length = x2 - 8 - x1
    return ('<path class="sk-draw" d="M%s %s H%s" stroke="%s" stroke-width="1.6" fill="none" style="--len:%s;--d:%ss"/>'
            % (x1, y, x2 - 8, color, length, _d(d))
            + '<path class="sk-fade" d="M%s %s l-8 -4.5 v9 Z" fill="%s" style="--d:%ss"/>' % (x2, y, color, _d(d + 0.6)))


def doc(x, y, w=86, h=108, stroke="var(--purple)"):
    """A page with a folded corner, top-left at (x, y)."""
    f = 20
    lines = "".join('<path d="M%s %s H%s" stroke="var(--muted)" stroke-width="2" stroke-linecap="round"/>'
                    % (x + 12, y + dy, x + w - 14) for dy in (40, 56, 72, 88) if dy < h - 10)
    return ('<path d="M%s %s H%s L%s %s V%s H%s Z" fill="var(--bg-3)" stroke="%s" stroke-width="1.4"/>'
            % (x, y, x + w - f, x + w, y + f, y + h, x, stroke)
            + '<path d="M%s %s V%s H%s" fill="none" stroke="%s" stroke-width="1.2"/>' % (x + w - f, y, y + f, x + w, stroke)
            + lines)


def check(cx, cy, r=10):
    return ('<circle cx="%s" cy="%s" r="%s" fill="var(--green-dim)" stroke="var(--green)" stroke-width="1.5"/>'
            '<path d="M%s %s L%s %s L%s %s" fill="none" stroke="var(--green)" stroke-width="1.8" '
            'stroke-linecap="round" stroke-linejoin="round"/>'
            % (cx, cy, r, cx - r * 0.45, cy, cx - r * 0.1, cy + r * 0.35, cx + r * 0.48, cy - r * 0.38))


def cross(cx, cy, r=10):
    k = r * 0.38
    return ('<circle cx="%s" cy="%s" r="%s" fill="var(--red-dim)" stroke="var(--red)" stroke-width="1.5"/>'
            '<path d="M%s %s L%s %s M%s %s L%s %s" stroke="var(--red)" stroke-width="1.8" stroke-linecap="round"/>'
            % (cx, cy, r, cx - k, cy - k, cx + k, cy + k, cx + k, cy - k, cx - k, cy + k))


def lock(x, y, stroke="var(--teal)"):
    return ('<rect x="%s" y="%s" width="16" height="11" rx="2" fill="var(--bg-3)" stroke="%s" stroke-width="1.3"/>'
            '<path d="M%s %s V%s a4 4 0 0 1 8 0 V%s" fill="none" stroke="%s" stroke-width="1.3"/>'
            % (x, y + 7, stroke, x + 4, y + 7, y + 4.5, y + 7, stroke))


KIND = {
    "ok": ("var(--green)", "var(--green-dim)", "ok"),
    "bad": ("var(--red)", "var(--red-dim)", "r"),
    "teal": ("var(--teal)", "var(--teal-dim)", "t"),
    "gold": ("var(--gold)", "var(--gold-dim)", "g"),
    "warn": ("var(--warn)", "var(--warn-dim)", "w"),
    "purple": ("var(--purple)", "var(--purple-dim)", "p"),
    "neutral": ("var(--border-2)", "var(--bg-3)", "s"),
}


def chip(x, y, w, label, kind, h=26):
    stroke, fill, cls = KIND[kind]
    return rect(x, y, w, h, stroke, fill, h / 2.0, 1.3) + t(x + w / 2.0, y + h / 2.0 + 4, label, "m xs " + cls, "middle")


# --------------------------------------------------------------------------- scenes
# Each returns (viewBox height, aria-label, caption, SVG body). Width is always 960.

def s_index():
    b = [g("sk-fade", 0.1, doc(40, 112) + t(83, 100, "the prompt", "p sm", "middle")
           + t(83, 244, "fixed for the day", "s xs", "middle"))]
    b.append(arrow(140, 166, 204, 0.4))
    b.append(g("sk-fade", 0.5, t(172, 138, "pasted", "mu xs", "middle") + t(172, 153, "by hand", "mu xs", "middle")))
    win = (rect(214, 96, 224, 168, "var(--border-2)", "var(--bg-2)", 10)
           + '<path d="M214 106 a10 10 0 0 1 10 -10 H428 a10 10 0 0 1 10 10 V122 H214 Z" fill="var(--bg-3)"/>'
           + "".join('<circle cx="%s" cy="109" r="3" fill="var(--muted)"/>' % cx for cx in (228, 240, 252))
           + t(340, 113, "free web chat", "m xs s", "middle"))
    b.append(g("sk-pop", 0.7, win))
    b.append(g("sk-slide", 1.0, rect(296, 134, 128, 26, "var(--purple)", "var(--purple-dim)", 8)
               + t(360, 151, "the prompt", "m xs p", "middle"), "--dx:16px;--dy:0px"))
    reply = rect(228, 170, 160, 70, "var(--teal)", "var(--teal-dim)", 8) + "".join(
        '<path d="M240 %s H%s" stroke="var(--teal-lt)" stroke-width="2" stroke-linecap="round" opacity=".7"/>'
        % (y, xe) for y, xe in ((188, 372), (202, 360), (216, 376), (230, 330)))
    b.append(g("sk-slide", 1.4, reply, "--dx:-16px;--dy:0px"))
    b.append(g("sk-fade", 1.6, t(326, 290, "16 models &middot; zero spend", "m xs s", "middle")))
    b.append(arrow(448, 166, 508, 1.8))
    b.append(g("sk-fade", 1.9, t(478, 138, "saved", "mu xs", "middle") + t(478, 153, "verbatim", "mu xs", "middle")))
    stack = "".join(rect(x, y, 72, 92, "var(--border-2)", "var(--bg-3)", 6) for x, y in ((530, 110), (524, 116), (518, 122)))
    stack += "".join('<path d="M530 %s H576" stroke="var(--muted)" stroke-width="2" stroke-linecap="round"/>' % yy
                     for yy in (146, 160, 174))
    b.append(g("sk-pop", 2.2, stack + t(554, 238, "663 replies", "m sm g", "middle")))
    b.append(arrow(606, 166, 652, 2.6))
    for i, (lab, y) in enumerate((("recompute the arithmetic", 104), ("match the operative text", 156),
                                  ("score against the paper", 208))):
        b.append(g("sk-slide", 2.9 + 0.2 * i, rect(662, y, 262, 40) + t(680, y + 25, lab, "b sm"), "--dx:18px;--dy:0px"))
        b.append(g("sk-pop", 3.5 + 0.1 * i, check(902, y + 20)))
    b.append(g("sk-fade", 3.9, t(480, 330, "Every verdict traces back to a measured row in that day&rsquo;s table.",
                                 "s sm", "middle")))
    label = ("A prompt document is pasted by hand into a free web chat window. The model reply is saved verbatim "
             "into a stack of 663 replies. Three grading lanes follow it: recompute the arithmetic, match the "
             "operative text and score against the paper. Each lane ends in a check mark.")
    cap = ("How every day worked. A person pasted one prompt into each model&rsquo;s free web chat, and every reply was "
           "saved verbatim and graded against something checkable.")
    return 360, label, cap, "".join(b)


def s_day1():
    b = [g("sk-fade", 0.1, doc(36, 120) + t(79, 108, "A-v5 prompt", "p sm", "middle"))]
    b.append(arrow(132, 174, 186, 0.4))
    b.append(g("sk-pop", 0.7, rect(196, 140, 68, 68, "var(--teal)", "var(--teal-dim)", 12)
               + t(230, 179, "model", "m xs t", "middle") + t(230, 228, "free web chat", "s xs", "middle")))
    b.append(arrow(274, 174, 318, 1.0))
    b.append(g("sk-fade", 1.2, t(628, 86, "exactly three episodes in one bare JSON array", "m xs s", "middle")))
    b.append(g("sk-pop", 1.2, t(323, 212, "[", "m g", style="font-size:118px")))
    b.append(g("sk-pop", 1.2, t(869, 212, "]", "m g", style="font-size:118px")))
    eps = (("ep 1", "routing congestion", "on a 28nm block"),
           ("ep 2", "a timing failure read", "from the report&rsquo;s shape"),
           ("ep 3", "an SDC derivation", "at a block boundary"))
    for i, (n, l1, l2) in enumerate(eps):
        x = 382 + i * 170
        card = (rect(x, 108, 152, 112, "var(--teal)", "var(--bg-3)", 8) + t(x + 14, 132, n, "m xs g")
                + t(x + 14, 158, l1, "b sm") + t(x + 14, 178, l2, "s xs")
                + '<path d="M%s 198 H%s" stroke="var(--muted)" stroke-width="2" stroke-linecap="round"/>' % (x + 14, x + 120))
        b.append(g("sk-slide", 1.5 + 0.3 * i, card))
    cand = rect(382, 246, 300, 124, "var(--border-2)", "var(--bg-2)", 8) + t(398, 270, "candidates_considered", "m xs t")
    for y in (294, 320, 346):
        cand += cross(408, y - 4, 7) + t(424, y, "an option rejected with its concrete cost", "s xs")
    b.append(g("sk-slide", 2.5, cand))
    b.append(g("sk-pop", 2.9, rect(698, 246, 192, 58, "var(--gold)", "var(--gold-dim)", 8)
               + t(714, 270, "weakest_point", "m xs g") + t(714, 290, "the detail most likely wrong", "b xs")))
    b.append(g("sk-pop", 3.3, chip(698, 314, 192, "invented name = worst output", "bad")))
    b.append(g("sk-pop", 3.6, chip(698, 346, 192, "honest skip scores higher", "ok")))
    label = ("The A-v5 prompt goes to a free web model, which must return exactly three episodes inside one bare "
             "JSON array: routing congestion on a 28nm block, a timing failure read from the report shape, and an "
             "SDC derivation at a block boundary. Each episode lists rejected candidates with their cost and a "
             "weakest point. An invented name is the worst output; an honest skip scores higher.")
    cap = ("The Day-1 exemplar asked for three draft episodes a veteran engineer would later attack. The rejected "
           "alternatives and the self-named weakest point mattered more than the story.")
    return 400, label, cap, "".join(b)


def s_day2():
    b = [g("sk-fade", 0.1, rect(40, 74, 400, 44) + t(56, 101, "zero tolerance", "b sm")
           + t(424, 101, "no increase allowed", "s xs", "end"))]
    b.append(g("sk-fade", 0.2, rect(40, 128, 400, 196, "var(--teal)", "var(--teal-dim)", 8)
               + t(56, 152, "10% aggregate tolerance", "t sm") + t(424, 152, "where implementations err", "s xs", "end")))
    b.append(g("sk-fade", 0.3, rect(40, 334, 400, 44) + t(56, 361, "no tolerance limit", "b sm")
               + t(424, 361, "any change allowed", "s xs", "end")))
    b.append(g("sk-fade", 0.4, t(56, 182, "fee", "mu xs u") + t(262, 182, "LE", "mu xs u", "end")
               + t(338, 182, "CD", "mu xs u", "end") + t(424, 182, "change", "mu xs u", "end")))
    rows = (("recording", "100", "180", "+80", "w"), ("title services", "600", "570", "&minus;30", "ok"),
            ("survey", "300", "340", "+40", "w"))
    for i, (fee, le, cd, ch, cls) in enumerate(rows):
        y = 208 + i * 26
        b.append(g("sk-slide", 0.5 + 0.2 * i, t(56, y, fee, "b sm") + t(262, y, le, "m sm b", "end")
                   + t(338, y, cd, "m sm b", "end") + t(424, y, ch, "m sm " + cls, "end")))
    b.append(g("sk-fade", 1.2, '<path d="M56 278 H424" stroke="var(--border-2)" stroke-width="1"/>'
               + t(56, 302, "total", "g sm") + t(262, 302, "1,000", "m sm g", "end")
               + t(338, 302, "1,090", "m sm g", "end") + t(424, 302, "+90", "m sm g", "end")))
    good = (rect(470, 74, 450, 150, "var(--green)", "var(--bg-3)", 8) + t(490, 102, "aggregate against aggregate", "ok sm")
            + t(490, 134, "total CD 1,090 against total LE &times; 1.10 = 1,100", "m xs b"))
    b.append(g("sk-slide", 1.6, good))
    b.append(g("sk-pop", 2.2, chip(490, 160, 210, "within tolerance", "ok") + check(724, 173)))
    bad = (rect(470, 240, 450, 150, "var(--red)", "var(--bg-3)", 8) + t(490, 268, "sum of the increases", "r sm")
           + t(490, 300, "80 + 40 = 120 against 10% of 1,000 = 100", "m xs b"))
    b.append(g("sk-slide", 2.5, bad))
    b.append(g("sk-pop", 2.8, chip(490, 326, 210, "flags a false violation", "bad") + cross(724, 339)))
    b.append('<path class="sk-draw" d="M480 250 L910 380" stroke="var(--red)" stroke-width="2" opacity=".7" '
             'fill="none" style="--len:451;--d:3.1s"/>')
    b.append(g("sk-fade", 3.4, t(920, 412, "the defect this prompt exists to catch", "r xs", "end")))
    b.append(g("sk-fade", 3.6, t(40, 412, "Illustrative numbers. Day 2 recomputed about 720 real cases.", "s xs")))
    label = ("A TRID fee table with three buckets: zero tolerance, a ten percent aggregate tolerance and no limit. "
             "In the ten percent bucket the fees move in mixed directions, totalling 1,000 on the Loan Estimate and "
             "1,090 on the Closing Disclosure. The correct test compares the totals, 1,090 against 1,100, and passes. "
             "The wrong method adds only the increases, 120 against 100, and flags a false violation, which is "
             "struck through.")
    cap = ("The rule the prompt pinned: the ten percent bucket compares the totals. A case that sums only the "
           "increases is the defect the prompt was built to expose. Numbers here are illustrative.")
    return 420, label, cap, "".join(b)


def s_day3():
    b = []

    def line(y0, title, phrase, ticks, strict, verdicts, d0):
        out = [g("sk-fade", d0, t(40, y0 - 34, title, "b sm") + t(40, y0 - 14, "&ldquo;%s&rdquo;" % phrase, "m xs g"))]
        out.append('<path class="sk-draw" d="M330 %s H900" stroke="var(--border-2)" stroke-width="2" fill="none" '
                   'style="--len:570;--d:%ss"/>' % (y0, _d(d0 + 0.1)))
        xs = (420, 610, 800)
        x0 = 618 if strict else 610
        out.append(g("sk-fade", d0 + 1.0, '<rect x="%s" y="%s" width="%s" height="14" rx="3" fill="var(--teal-dim)" '
                     'stroke="var(--teal)" stroke-width="1"/>' % (x0, y0 - 7, 900 - x0) + t(896, y0 - 14, "fires", "t xs u", "end")))
        for x, lab in zip(xs, ticks):
            out.append(g("sk-fade", d0 + 0.4, '<path d="M%s %s V%s" stroke="var(--muted)" stroke-width="1.5"/>'
                         % (x, y0 - 6, y0 + 6) + t(x, y0 + 26, lab, "m sm b", "middle")))
        fill = "var(--bg-2)" if strict else "var(--warn)"
        out.append(g("sk-pop", d0 + 0.8, '<circle cx="610" cy="%s" r="8" fill="%s" stroke="var(--warn)" stroke-width="2.4"/>'
                     % (y0, fill)))
        out.append(g("sk-fade", d0 + 0.9, t(610, y0 - 18, "strict boundary" if strict else "inclusive boundary", "w xs", "middle")))
        for k, (x, v) in enumerate(zip(xs, verdicts)):
            out.append(g("sk-pop", d0 + 1.4 + 0.25 * k, chip(x - 34, y0 + 38, 68, v, "ok" if v == "fires" else "neutral")))
        return out

    b += line(118, "HOEPA duration trigger", "more than 36 months", ("35", "36", "37"), True, ("no", "no", "fires"), 0.1)
    b += line(282, "Higher-priced covered transaction", "by 1.5 or more percentage points",
              ("1.49", "1.50", "1.51"), False, ("no", "fires", "fires"), 0.6)
    b.append(g("sk-fade", 3.3, t(480, 372, "Each cell is a closed-form verdict, graded by string match against the operative text.",
                                 "s sm", "middle")))
    label = ("Two number lines probed below, at and above a boundary. HOEPA's duration trigger, more than 36 months, "
             "is strict: an open circle at 36, so 35 and 36 do not fire and 37 does. The higher-priced test, 1.5 or "
             "more percentage points, is inclusive: a filled circle at 1.50, so 1.50 and 1.51 fire and 1.49 does not.")
    cap = ("The boundary prompt asked whether each rule fires exactly at its boundary, just below and just above. "
           "The operative phrase decides it, and the boundary value is where models slip.")
    return 380, label, cap, "".join(b)


def s_day4():
    b = [g("sk-fade", 0.1, rect(40, 96, 270, 150, "var(--gold)", "var(--bg-3)", 8) + t(56, 124, "the one named paper", "m xs g")
           + t(56, 152, "The Alpha 21264 Microprocessor", "b sm") + t(56, 176, "R. E. Kessler", "s xs")
           + t(56, 196, "IEEE Micro 19(2) &middot; 1999", "s xs") + t(56, 216, "pages 24&ndash;36", "s xs"))]
    b.append(arrow(320, 171, 372, 0.5))
    b.append(g("sk-pop", 0.8, rect(382, 136, 92, 70, "var(--teal)", "var(--teal-dim)", 12)
               + t(428, 176, "model", "m xs t", "middle") + t(428, 226, "recall from memory", "s xs", "middle")
               + t(428, 244, "of this paper only", "s xs", "middle")))
    b.append(arrow(484, 171, 530, 1.2))
    lanes = (("claim found in the paper", "matches the extraction set", "ok", 96),
             ("cannot-reproduce-verbatim", "an honest answer that scores well", "teal", 162),
             ("a reversed decision", "the single worst output", "bad", 228))
    for i, (h, sub, kind, y) in enumerate(lanes):
        stroke, _fill, cls = KIND[kind]
        b.append(g("sk-slide", 1.5 + 0.4 * i, rect(540, y, 380, 54, stroke, "var(--bg-3)", 8)
                   + t(586, y + 23, h, "m sm " + cls) + t(586, y + 42, sub, "s xs"), "--dx:18px;--dy:0px"))
        if kind == "ok":
            icon = check(562, y + 27)
        elif kind == "bad":
            icon = cross(562, y + 27)
        else:
            icon = ('<circle cx="562" cy="%s" r="10" fill="var(--teal-dim)" stroke="var(--teal)" stroke-width="1.5"/>' % (y + 27)
                    + t(562, y + 31, "?", "m xs t", "middle"))
        b.append(g("sk-pop", 1.9 + 0.4 * i, icon))
    b.append(g("sk-fade", 3.1, rect(40, 306, 880, 40, "var(--border)", "var(--bg-2)", 8)
               + t(480, 331, "Each claim is checked against a locator-cited extraction set and the full PDF text.", "s sm", "middle")))
    label = ("A citation card for the Alpha 21264 paper by R. E. Kessler, IEEE Micro 1999, feeds a model that must "
             "recall from that paper only. Its claims land in three lanes: found in the paper, an honest "
             "cannot-reproduce-verbatim, or a reversed decision, which is the worst output.")
    cap = ("Each Day-4 prompt named one paper by its full citation. Saying it cannot be reproduced scored well; "
           "reversing a decision the paper made was the single worst answer.")
    return 380, label, cap, "".join(b)


def s_day5():
    b = []

    def val(x, w, lab, amount, stroke, d, cls="sk-pop"):
        return g(cls, d, rect(x, 112, w, 80, stroke, "var(--bg-3)", 8) + t(x + w / 2.0, 140, lab, "s xs u", "middle")
                 + t(x + w / 2.0, 172, amount, "m md b", "middle"))

    b.append(val(36, 150, "2023 tier A", "$124,331", "var(--border-2)", 0.1, "sk-fade"))
    b.append(arrow(192, 152, 270, 0.4))
    b.append(g("sk-fade", 0.6, t(231, 138, "&times; 1.049304", "m xs g", "middle") + t(231, 176, "implied", "mu xs", "middle")))
    b.append(val(276, 150, "2024 tier A", "$130,461", "var(--border-2)", 0.9))
    b.append(arrow(432, 152, 510, 1.3))
    b.append(g("sk-fade", 1.5, t(471, 138, "&times; 1.034", "m xs g", "middle") + t(471, 176, "CPI-U 3.4%", "mu xs", "middle")))
    b.append(val(516, 196, "2025 projected", "$134,896.674", "var(--teal)", 1.7))
    b.append(g("sk-fade", 2.1, t(614, 212, "rounds to $134,897", "t xs", "middle")))
    b.append(val(736, 186, "2025 official", "$134,841", "var(--gold)", 2.4))
    b.append(g("sk-slide", 2.8, rect(276, 246, 646, 72, "var(--border-2)", "var(--bg-2)", 8)
               + t(296, 274, "the exact factor that would produce the official value", "s xs")
               + t(296, 300, "134,841 &divide; 130,461 = 1.033573", "m sm b")))
    b.append(g("sk-pop", 3.3, chip(700, 262, 204, "gap 4.27 bps &middot; $56", "warn", 40)))
    b.append(g("sk-fade", 3.7, t(36, 344, "Six decimal places, recomputed mechanically.", "s xs")))
    label = ("Regulation Z tier A: 124,331 dollars in 2023 times the implied factor 1.049304 gives 130,461 in 2024. "
             "Times 1.034 for the 3.4 percent CPI-U rise projects 134,896.674, which rounds to 134,897. The official "
             "2025 value is 134,841, so the exact factor is 1.033573 and the gap is 4.27 basis points, or 56 dollars.")
    cap = ("The Reg Z prompt asked for the implied factors and a 2025 projection checked against the official value. "
           "Every figure here was recomputed from the prompt&rsquo;s own inputs.")
    return 360, label, cap, "".join(b)


def s_day6():
    b = [g("sk-fade", 0.1, t(40, 76, "anchor check", "m xs g u"))]
    for i, lab in enumerate(("b1", "b2", "b3")):
        y = 92 + i * 58
        b.append(g("sk-slide", 0.2 + 0.2 * i, rect(40, y, 250, 46) + lock(56, y + 13)
                   + t(84, y + 20, lab + " &middot; answer already known", "b xs") + t(84, y + 36, "used for calibration", "s xs")))
    b.append(g("sk-fade", 1.0, t(40, 288, "calibration is scored", "s sm") + t(40, 308, "apart from the research", "s sm")))
    for j, c in enumerate(("Chrome/Edge", "Firefox", "Safari")):
        b.append(g("sk-fade", 1.0, t(392 + j * 92, 80, c, "m xs s", "middle")))
    k = 0
    for r in range(9):
        for j in range(3):
            b.append(g("sk-fade", 1.2 + 0.055 * k, rect(352 + j * 92, 92 + r * 24, 80, 18, "var(--border-2)", "var(--bg-3)", 3, 1)))
            k += 1
    b.append(g("sk-fade", 2.8, t(484, 330, "27 rows, no more and no fewer", "m sm t", "middle")
               + t(484, 350, "each tagged live URL with a date, or training-recall", "s xs", "middle")))
    b.append(g("sk-pop", 2.0, chip(650, 92, 128, "a1 genuine", "ok")))
    b.append(g("sk-pop", 2.2, chip(792, 92, 128, "a2 genuine", "ok")))
    b.append(g("sk-slide", 2.6, rect(650, 134, 270, 122, "var(--red)", "var(--bg-3)", 8) + t(666, 160, "a3 &middot; the decoy", "m xs r")
               + t(666, 186, "the paper is real", "b sm") + t(666, 208, "its venue was swapped", "b sm")
               + t(666, 238, "a citation anchor with a planted error", "s xs")))
    b.append(g("sk-pop", 3.4, chip(650, 270, 270, "exists-exactly = fabrication-liable", "bad")))
    label = ("Three anchor statements, b1, b2 and b3, whose answers are already known, score calibration on their "
             "own. A grid of 27 rows, nine cells across Chrome or Edge, Firefox and Safari, fills in, each row tagged "
             "with a live URL and date or as training recall. Citation anchors a1 and a2 are genuine; a3 is a real "
             "paper with its venue swapped, and calling it exists-exactly is fabrication.")
    cap = ("Both Day-6 prompts opened with anchors the estate could already check, so calibration is measured "
           "apart from the research. The a3 decoy rewards a model that notices the venue is wrong.")
    return 380, label, cap, "".join(b)


# Day-7 table: keys of the required seven that each model's JSON file carried.
DAY7_KEYS = (("chatgpt", 0), ("deepseek", 1), ("gemini", 1), ("glm flash", 1), ("grok", 1), ("kimi", 1),
             ("longcat", 1), ("meta", 0), ("mimo", 0), ("minimax", 0), ("mistral", 0), ("qwen", 0),
             ("solar", 0), ("sonnet", 1), ("yuanbao", 1))
DAY7_TOKENS = ("reject", "reject_and_revise", "reject-as-is", "overstated", "REVISE_BEFORE_INGEST", "not_ready")


def s_day7():
    b = [g("sk-fade", 0.1, rect(36, 80, 300, 210, "var(--purple)", "var(--bg-3)", 8) + t(52, 104, "the binding contract", "m xs p u")
           + "".join(t(52, 136 + i * 28, r, "b sm") for i, r in enumerate(
               ("first character {", "last character }", "seven keys described in one line", "verdict from a four-value enum")))
           + t(52, 262, "SOUND | SOUND-WITH-RESERVATIONS", "m xs g") + t(52, 280, "SUSPECT | IMPLAUSIBLE-FOR-THIS-RECORD", "m xs g"))]
    b.append(arrow(344, 185, 392, 0.9))
    for i, (m, keys) in enumerate(DAY7_KEYS):
        col, row = i // 5, i % 5
        x, y = 402 + col * 176, 80 + row * 42
        tile = rect(x, y, 166, 34, "var(--border-2)", "var(--bg-3)", 6) + t(x + 10, y + 21, m, "m xs b")
        for s in range(7):
            tile += ('<rect x="%s" y="%s" width="8" height="12" rx="2" fill="%s" stroke="var(--border-2)" stroke-width="1"/>'
                     % (x + 90 + s * 10, y + 11, "var(--warn)" if s < keys else "var(--bg-2)"))
        b.append(g("sk-fade", 1.2 + 0.07 * i, tile))
    b.append(g("sk-fade", 2.4, t(402, 306, "required keys present, out of seven", "mu xs")))
    b.append(g("sk-fade", 2.5, t(36, 352, "verdicts the models invented", "s xs")))
    x = 236
    for i, tok in enumerate(DAY7_TOKENS):
        w = 18 + 7 * len(tok)
        b.append(g("sk-slide", 2.6 + 0.1 * i, chip(x, 334, w, tok, "warn")))
        x += w + 10
    b.append(g("sk-pop", 3.6, t(480, 404, "0 / 15 carried the schema", "m lg r", "middle")))
    label = ("The binding contract demands a first character of an opening brace, a last character of a closing "
             "brace, seven keys described in one line and a verdict from a four-value enum. Fifteen model tiles "
             "follow, each with a seven-slot key meter that never fills past one. Invented verdict words such as "
             "reject, overstated, REVISE_BEFORE_INGEST and not_ready float in. None of the fifteen carried the schema.")
    cap = ("Fifteen models answered the same prompt and none returned the seven-key schema. The best carried one key "
           "in seven, and each invented its own word for a four-value verdict.")
    return 420, label, cap, "".join(b)


def s_day8():
    b = [g("sk-fade", 0.1, rect(36, 72, 318, 270, "var(--teal)", "var(--bg-3)", 8) + t(52, 96, "a literal object to copy", "m xs t u"))]
    lines = (("{", 52), ('"verdict": "SOUND | SUSPECT | &hellip;",', 66), ('"objections": [ &hellip; ],', 66),
             ('"mechanism_check": "&hellip;",', 66), ('"evidence_check": "&hellip;",', 66),
             ('"attribution_check": "&hellip;",', 66), ('"missing_from_story": "&hellip;",', 66),
             ('"most_defensible_part": "&hellip;"', 66), ("}", 52))
    for i, (ln, x) in enumerate(lines):
        b.append(g("sk-fade", 0.3 + 0.08 * i, t(x, 124 + i * 24, ln, "m xs b")))
    b.append(arrow(362, 207, 410, 1.2))
    b.append(g("sk-fade", 1.4, t(708, 80, "the ten incident drafts", "s xs", "middle")
               + "".join(t(516 + c * 42, 100, str(c + 1), "m xs mu", "middle") for c in range(10))))
    for r, m in enumerate(("kimi", "sonnet", "deepseek")):
        y = 110 + r * 70
        b.append(g("sk-fade", 1.3, t(486, y + 26, m, "m sm b", "end")))
        for c in range(10):
            x = 498 + c * 42
            tile = (rect(x, y, 36, 40, "var(--green)", "var(--green-dim)", 6)
                    + '<path d="M%s %s L%s %s L%s %s" fill="none" stroke="var(--green)" stroke-width="2" '
                      'stroke-linecap="round" stroke-linejoin="round"/>' % (x + 11, y + 21, x + 16, y + 26, x + 26, y + 14))
            b.append(g("sk-pop", 1.5 + 0.18 * c + 0.04 * r, tile))
    b.append(g("sk-pop", 3.7, t(708, 372, "30 / 30 parsed on the first try", "m lg ok", "middle")))
    b.append(g("sk-fade", 3.9, t(708, 398, "all seven keys present and no key renamed", "s sm", "middle")))
    label = ("A literal JSON object to copy, with the verdict enum written against its field and all seven keys "
             "shown. Three models, kimi, sonnet and deepseek, each review ten incident drafts. All thirty tiles turn "
             "green: thirty of thirty parsed on the first try with all seven keys and no key renamed.")
    cap = ("Day 8 replaced the abstract schema with a literal object to copy. The same three models then returned "
           "thirty of thirty parseable reviews.")
    return 420, label, cap, "".join(b)


SCENES = {"index": s_index, "day1": s_day1, "day2": s_day2, "day3": s_day3, "day4": s_day4,
          "day5": s_day5, "day6": s_day6, "day7": s_day7, "day8": s_day8}


def max_end(svg):
    """Latest moment any animation in the scene finishes, in seconds."""
    end = 0.0
    for tag in re.findall(r"<[a-z][^>]*>", svg):
        m = re.search(r'class="([^"]*)"', tag)
        if not m:
            continue
        anims = [c for c in m.group(1).split() if c in DUR]
        if not anims:
            continue
        dm = re.search(r"--d:([0-9.]+)s", tag)
        end = max(end, (float(dm.group(1)) if dm else 0.0) + max(DUR[c] for c in anims))
    if re.search(r"\bsk-(pulse|travel)\b", svg):
        raise SystemExit("scene uses sk-pulse or sk-travel; this module only budgets one-shot classes")
    return end


def scene_html(fid):
    """The scene for one page, wrapped the way the Staircase explainer wraps its scenes."""
    h, label, cap, body = SCENES[fid]()
    svg = ('<svg class="sk-scene" viewBox="0 0 960 %d" role="img" aria-label="%s" xmlns="http://www.w3.org/2000/svg">%s</svg>'
           % (h, label, body))
    return ('<div class="scene-wrap"><button type="button" class="replay" data-replay>Replay</button>'
            '<div class="scene-scroll">%s</div></div><p class="sk-cap">%s</p>' % (svg, cap))


# Refuse to build a scene whose motion outlasts the five-second limit.
for _fid, _fn in SCENES.items():
    _end = max_end(_fn()[3])
    if _end > MAX_END:
        raise SystemExit("scene %s animates for %.2fs, over the %.1fs limit" % (_fid, _end, MAX_END))

if __name__ == "__main__":
    for _fid, _fn in SCENES.items():
        print("%-6s motion ends at %.2fs" % (_fid, max_end(_fn()[3])))
