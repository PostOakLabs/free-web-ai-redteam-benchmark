# Browser-dispatch mechanism notes (2026-09-03, first supervised run)

Findings from the pilot attempt. These are properties of the Claude-in-Chrome MCP, not of any model.

## 1. The extension only addresses its own tab group
`tabs_context_mcp` sees ONLY tabs inside the session's Chrome tab group. Tabs the user already has open
elsewhere are invisible and untargetable. The user must drag them into the group (or the session opens
its own). Cookies are profile-wide, so a tab opened by the session in the same Chrome profile inherits
the user's logins — no login wall, no SKIPPED-AUTH.

## 2. Closing the group's last original tab DESTROYS the group
Closing the blank anchor tab dissolved group 1549947802 and ejected all 13 dragged-in tabs.
NEVER close the blank anchor tab. Leave it open for the whole run.

## 3. ctrl+v does not work
The extension's key action cannot reach the system clipboard. `computer-use write_clipboard` + extension
`ctrl+v` leaves the composer empty. Clipboard route is unusable for payload delivery.

## 4. `type` silently no-ops on background tabs
Every `type` and `key` action against a non-foregrounded tab returned success while the composer stayed
empty (verified by screenshot). This MCP has no tab-select/activate tool, so during a fan-out at least
N-1 tabs are always backgrounded. Keystroke input therefore cannot be used for fan-out dispatch.

**This is the failure the doc's pilot gate exists to catch:** 11 manifest lines would have been written
against 11 empty composers. Reported-success is not evidence of delivery.

## 5. Standing rule adopted
Verify the composer's ACTUAL text (read_page / javascript_tool) before every send. A dispatch is only
recorded after the payload is confirmed present in the box. Never trust an action's success return.

## Method adopted
DOM write via `javascript_tool`: set composer content, dispatch the input events the framework listens
for, confirm text, then click Send by element ref. Focus-independent, so fan-out works.
