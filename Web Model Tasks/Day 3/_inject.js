(async () => {
  const B64 = "RXhlY3V0ZSB0aGUgYXR0YWNoZWQgZG9jdW1lbnQgZXhhY3RseSBhcyB3cml0dGVuLCBmb2xsb3dpbmcgaXRzIG91dHB1dCBmb3JtYXQgYW5kIGhvbmVzdHkgcnVsZXMgdG8gdGhlIGxldHRlciwgYW5kIHJlcGx5IHdpdGggdGhlIGJhcmUgSlNPTiBvbmx5LgoKIyBUYXNrOiBib3VuZGFyeS1pbmNsdXNpdml0eSB2ZXJkaWN0IHRhYmxlcyBmb3IgcmVndWxhdG9yeSBjb21wYXJhdG9ycwoKRXZlcnkgYW5zd2VyIGlzIGEgY2xvc2VkLWZvcm0gdmVyZGljdCBncmFkZWQgbWVjaGFuaWNhbGx5IGFnYWluc3Qgb3BlcmF0aXZlIHJlZ3VsYXRvcnkgdGV4dCB3ZSBob2xkLiBTaG93IHJlYXNvbmluZyBwZXIgY2VsbDsgaG9uZXN0eSBsYWJlbHMgdGFrZW4gYXQgZmFjZSB2YWx1ZS4KCkZvciBlYWNoIHJ1bGUgYmVsb3csIHByb2R1Y2UgYSB2ZXJkaWN0IHRhYmxlIGZvciB0aGUgaW5wdXRzIGxpc3RlZDogZG9lcyB0aGUgdHJpZ2dlci90ZXN0IEZJUkUgKG9yIFBBU1MpIGF0IGV4YWN0bHkgdGhlIGJvdW5kYXJ5IHZhbHVlLCBqdXN0IGJlbG93LCBhbmQganVzdCBhYm92ZT8gU3RhdGUgdGhlIG9wZXJhdGl2ZSBwaHJhc2UncyBpbmNsdXNpdml0eSAoc3RyaWN0IHZzIGluY2x1c2l2ZSkgdGhhdCBkcml2ZXMgZWFjaCB2ZXJkaWN0LgoKMS4gKipIT0VQQSBwcmVwYXltZW50LXBlbmFsdHkgdHJpZ2dlcioqIOKAlCByZWd1bGF0aW9uOiBwZW5hbHRpZXMgdGhhdCAiY2FuIGV4Y2VlZCwgaW4gdG90YWwsIG1vcmUgdGhhbiAyIHBlcmNlbnQgb2YgdGhlIGFtb3VudCBwcmVwYWlkLiIgSW5wdXRzOiAxLjk5JSwgMi4wMCUsIDIuMDElLgoyLiAqKkhPRVBBIGR1cmF0aW9uIHRyaWdnZXIqKiDigJQgIm1vcmUgdGhhbiAzNiBtb250aHMgYWZ0ZXIgY29uc3VtbWF0aW9uLiIgSW5wdXRzOiAzNSwgMzYsIDM3IG1vbnRocy4KMy4gKipIaWdoZXItcHJpY2VkIGNvdmVyZWQgdHJhbnNhY3Rpb24qKiDigJQgQVBSICJleGNlZWRzIHRoZSBhdmVyYWdlIHByaW1lIG9mZmVyIHJhdGUg4oCmIGJ5IDEuNSBvciBtb3JlIHBlcmNlbnRhZ2UgcG9pbnRzLiIgU3ByZWFkczogMS40OSwgMS41MCwgMS41MS4KNC4gKipHZW5lcmFsIFFNIHByaWNlIGxpbWl0Kiog4oCUIEFQUiAiZG9lcyBub3QgZXhjZWVkIEFQT1Ig4oCmIGJ5IDIuMjUgb3IgbW9yZSBwZXJjZW50YWdlIHBvaW50cyIgKHBhc3MgY29uZGl0aW9uKS4gU3ByZWFkczogMi4yNCwgMi4yNSwgMi4yNi4KNS4gKipHbG9CRSBkZS1taW5pbWlzIChnZW5lcmFsIHJ1bGUpKiog4oCUIGF2ZXJhZ2UgcmV2ZW51ZSAibGVzcyB0aGFuIEVVUiAxMCBtaWxsaW9uIiBBTkQgYXZlcmFnZSBpbmNvbWUgImxlc3MgdGhhbiBFVVIgMSBtaWxsaW9uLiIgUGFpcnM6ICgxMC4wTSwgMC45TSksICg5LjlNLCAxLjBNKSwgKDkuOU0sIDAuOU0pLgo2LiAqKlRyYW5zaXRpb25hbCBDYkNSIHNhZmUgaGFyYm91ciBzaW1wbGlmaWVkIEVUUioqIOKAlCBzaW1wbGlmaWVkIEVUUiAiZXF1YWwgdG8gb3IgZ3JlYXRlciB0aGFuIiB0aGUgMTYlIHRyYW5zaXRpb24gcmF0ZSAoMjAyNiBmaXNjYWwgeWVhcikuIEVUUnM6IDE1Ljk5JSwgMTYuMDAlLCAxNi4wMSUuCjcuICoqU29sdmVuY3kgSUkgVGllciAxIGZsb29yKiog4oCUIGVsaWdpYmxlIFRpZXIgMSAiYXQgbGVhc3QgZXF1YWwgdG8iIDUwJSBvZiBTQ1IuIFJhdGlvczogNDkuOTklLCA1MC4wMCUsIDUwLjAxJS4KOC4gKipOSVMyIHNpZ25pZmljYW50IGluY2lkZW50ICh1c2VycyBsZWcpKiog4oCUIGFmZmVjdGVkIHVzZXJzIHRocmVzaG9sZCBmcmFtZWQgYXMgImVxdWFsIHRvIG9yIGdyZWF0ZXIgdGhhbiIgdGhlIG1pbmltdW0uIFZhbHVlczogdGhyZXNob2xk4oiSMSwgdGhyZXNob2xkLCB0aHJlc2hvbGQrMS4KCioqT3V0cHV0OioqIGJhcmUgSlNPTiBvbmx5OiBvbmUgb2JqZWN0IHBlciBydWxlIGB7InJ1bGUiOiBOLCAicGhyYXNlX2luY2x1c2l2aXR5IjogInN0cmljdHxpbmNsdXNpdmUiLCAidmVyZGljdHMiOiB7ImJlbG93IjogIi4uLiIsICJhdCI6ICIuLi4iLCAiYWJvdmUiOiAiLi4uIn0sICJyZWFzb25pbmciOiAiPG9uZSBzZW50ZW5jZT4ifWAgcGx1cyBgeyJ3ZWFrZXN0X3BvaW50IjogIi4uLiJ9YCDigJQgdGhlIHJ1bGUgd2hvc2UgcGhyYXNpbmcgeW91IGFyZSBsZWFzdCBjZXJ0YWluIHlvdSBoYXZlIHZlcmJhdGltLXJpZ2h0LCBhbmQgd2h5Lgo=";
  const txt = new TextDecoder().decode(Uint8Array.from(atob(B64), c => c.charCodeAt(0)));
  const pick = () => [...document.querySelectorAll('textarea,[contenteditable="true"],[role="textbox"]')]
      .filter(e => (e.offsetParent !== null || e.getClientRects().length) && !e.closest('[aria-hidden="true"]'))
      .map(e => { const r = e.getBoundingClientRect(); return { e, a: r.width * r.height }; })
      .filter(o => o.a > 500)
      .sort((x, y) => y.a - x.a)
      .map(o => o.e)[0];
  let el = null;
  for (let i = 0; i < 30 && !el; i++) { el = pick(); if (!el) await new Promise(r => setTimeout(r, 500)); }
  if (!el) return { ok: false, err: 'NO-COMPOSER-AFTER-15S' };
  const read = () => (el.value !== undefined ? el.value : el.innerText) || '';
  const pre = read().trim();
  if (pre.length) return { ok: false, err: 'COMPOSER-NOT-EMPTY', pre_len: pre.length };
  el.focus();
  const dt = new DataTransfer();
  dt.setData('text/plain', txt);
  const ev = new ClipboardEvent('paste', { bubbles: false, cancelable: true, clipboardData: dt });
  el.dispatchEvent(ev);
  await new Promise(r => setTimeout(r, 800));
  let rb = read();
  let method = 'paste-nonbubbling';
  if (rb.trim().length < txt.length * 0.9) {
    el.dispatchEvent(new ClipboardEvent('paste', { bubbles: true, cancelable: true, clipboardData: dt }));
    await new Promise(r => setTimeout(r, 800));
    rb = read();
    method = 'paste-bubbling';
  }
  const marker = 'Execute the attached document';
  let i = -1, n = 0;
  while ((i = rb.indexOf(marker, i + 1)) !== -1) n++;
  return {
    ok: n === 1 && rb.trim().length >= txt.length * 0.98 && rb.trim().length <= txt.length * 1.05,
    method, occurrences: n, payload_len: txt.length, readback_len: rb.trim().length,
    head: rb.slice(0, 50), tail: rb.trim().slice(-50)
  };
})()
