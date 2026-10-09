import json, os, sys, textwrap
OUT = os.path.dirname(os.path.abspath(__file__))
store = json.load(open(os.path.join(OUT, "store.json"), encoding="utf-8"))
sl = sys.argv[1]
maxlen = int(sys.argv[2]) if len(sys.argv) > 2 else 100000

def render(o, ind=0):
    pad = "  " * ind
    if isinstance(o, dict):
        lines = []
        for k, v in o.items():
            if isinstance(v, (dict, list)):
                lines.append(f"{pad}{k}:")
                lines.append(render(v, ind + 1))
            else:
                lines.append(f"{pad}{k}: {v}")
        return "\n".join(lines)
    if isinstance(o, list):
        return "\n".join(
            (render(v, ind) if isinstance(v, (dict, list)) else f"{pad}- {v}")
            for v in o)
    return f"{pad}{o}"

buf = []
for f in store.get(sl, []):
    buf.append(f"\n@@@@@@ FILE {f['file']}  model={f['model']}  n={len(f['items'])}")
    for i, it in enumerate(f["items"]):
        buf.append(f"--- [{f['model']}#{i}]")
        buf.append(render(it))
t = "\n".join(buf)
sys.stdout.reconfigure(encoding="utf-8",errors="replace")
print(t[:maxlen])
print(f"\n[[dumped {len(t)} chars of slice {sl}]]")
