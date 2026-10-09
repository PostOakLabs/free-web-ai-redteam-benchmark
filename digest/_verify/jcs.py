"""Minimal RFC 8785 (JCS) canonicalizer used to adjudicate the C2-JCS slice."""
import json, math, re, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

ESC = {'"': '\\"', '\\': '\\\\', '\b': '\\b', '\f': '\\f',
       '\n': '\\n', '\r': '\\r', '\t': '\\t'}

def jstr(s):
    out = ['"']
    for ch in s:
        if ch in ESC:
            out.append(ESC[ch])
        elif ord(ch) < 0x20:
            out.append('\\u%04x' % ord(ch))
        else:
            out.append(ch)
    out.append('"')
    return "".join(out)

def es_number(x):
    """ECMAScript Number::toString for a double (RFC 8785 §3.2.2.3)."""
    if isinstance(x, int) and not isinstance(x, bool):
        x = float(x)
    if x != x or x in (float("inf"), float("-inf")):
        raise ValueError("non-finite")
    if x == 0:
        return "0"                       # JCS: -0 serializes as 0
    neg = x < 0
    a = abs(x)
    r = repr(a)                          # shortest round-trip, like ES
    if "e" in r or "E" in r:
        m, e = r.split("e")
        exp = int(e)
    else:
        if a == int(a) and a < 1e21:
            m, exp = str(int(a)), 0
        else:
            m, exp = r, 0
    # normalise to digits + decimal exponent
    d = repr(a)
    if "e" in d:
        mant, ex = d.split("e")
        ex = int(ex)
    else:
        mant, ex = d, 0
    mant = mant.rstrip(".")
    if "." in mant:
        ip, fp = mant.split(".")
    else:
        ip, fp = mant, ""
    digits = (ip + fp).lstrip("0") or "0"
    point = len(ip.lstrip("0")) + ex if ip.strip("0") else ex - (len(fp) - len(fp.lstrip("0")))
    digits = digits.rstrip("0") or "0"
    k = len(digits)
    n = point
    if k <= n <= 21:
        s = digits + "0" * (n - k)
    elif 0 < n <= 21:
        s = digits[:n] + "." + digits[n:]
    elif -6 < n <= 0:
        s = "0." + "0" * (-n) + digits
    else:
        e = n - 1
        sign = "+" if e >= 0 else "-"
        head = digits[0] + ("." + digits[1:] if k > 1 else "")
        s = f"{head}e{sign}{abs(e)}"
    return ("-" if neg else "") + s

def canon(v):
    if v is True:
        return "true"
    if v is False:
        return "false"
    if v is None:
        return "null"
    if isinstance(v, str):
        return jstr(v)
    if isinstance(v, (int, float)):
        return es_number(v)
    if isinstance(v, list):
        return "[" + ",".join(canon(x) for x in v) + "]"
    if isinstance(v, dict):
        items = sorted(v.items(), key=lambda kv: kv[0].encode("utf-16-be"))
        return "{" + ",".join(jstr(k) + ":" + canon(x) for k, x in items) + "}"
    raise TypeError(type(v))

if __name__ == "__main__":
    # self-tests against RFC 8785 known values
    tests = [
        ({"a": 1}, '{"a":1}'),
        ({}, "{}"),
        ([], "[]"),
        (1.0, "1"),
        (-0.0, "0"),
        (1e21, "1e+21"),
        (1e-7, "1e-7"),
        (0.000001, "0.000001"),
        (9007199254740992.0, "9007199254740992"),
        (1e20, "100000000000000000000"),
        (333333333.33333329, "333333333.3333333"),
        ({"€": 1, "$": 2, "ü": 3}, None),
    ]
    for v, exp in tests:
        got = canon(v)
        print(("OK  " if (exp is None or got == exp) else "FAIL"), repr(v), "->", got,
              "" if exp is None else f"(expected {exp})")
