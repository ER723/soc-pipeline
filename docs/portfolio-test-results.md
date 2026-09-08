# Portfolio Test Results

Three MITRE ATT&CK-mapped techniques were tested end-to-end against the live pipeline and confirmed landing in both the Google Sheet escalation queue and Discord, with HMAC-signature-verified delivery. A fourth technique was tested and produced a documented partial result. All tests were run against a real macOS host with a live Wazuh agent — no synthetic/injected alerts were used for the results below.

**Methodology note on severity:** Wazuh's default ruleset scores macOS-native events well below typical SOC escalation thresholds by design (see `known-limitations.md`). Each test below uses one custom rule — a standard Wazuh rule-tuning mechanism — to reclassify an already-real, already-firing detection to a severity appropriate for this deployment's threshold (12). No test used a fabricated event, and no test altered the escalation threshold itself.

---

## Test 1 — T1110: Brute Force (sudo authentication)

**Method:** `sudo -k && sudo -v`, three incorrect passwords entered interactively.
**Default detection:** Wazuh rule `5404` ("Three failed attempts to run sudo"), level 10.
**Custom escalation:** Rule `100100`, reclassifies `5404` to level 12.
**Result:** Escalated correctly. Delivered to Discord and the Google Sheet with matching HMAC signature.

```json
{"decision": "escalated", "rule_id": "100100", "rule_level": 12,
 "rule_description": "SOC Pipeline: Repeated sudo authentication failures - escalated (possible brute force)"}
```

---

## Test 2 — T1014: Rootkit (rootcheck anomaly)

**Method:** No manual trigger required — rootcheck runs on its own schedule and fired repeatedly and reliably throughout testing (rule `510`, "Port hidden. Kernel-level rootkit or trojaned version of netstat," level 7).
**Custom escalation:** Rule `100101`, reclassifies `510` to level 12.
**Result:** Escalated correctly on the next natural rootcheck cycle.

---

## Test 3 — T1571: Non-Standard Port (unauthorized service/backdoor indicator)

**Method:** `python3 -m http.server 8888 &`, followed by an agent restart to force an immediate port-state re-check.
**Default detection:** Wazuh rule `533` ("Listened ports status changed"), level 7 — fired 111 times in one week of normal background activity per the pipeline's own weekly tuning report.
**Custom escalation:** Rule `100102`, reclassifies `533` to level 12.
**Result:** Escalated correctly, twice — once for the port opening and again when the test server was killed, since rule 533 fires on both open and close events.

---

## Test 4 (partial) — T1543.001: Create or Modify System Process (LaunchAgent persistence)

**Method:** The genuine, unmodified test artifact from Red Canary's official Atomic Red Team repository (`atomics/T1543.001/src/atomicredteam_T1543_001.plist`), downloaded directly from GitHub and loaded via the documented official command sequence.
**Result: no alert generated, end to end, despite extensive verification.** Diagnosed as a real Wazuh macOS FIM limitation, not a test error — see `known-limitations.md` for the full diagnostic trail (Full Disk Access grants, full reboots, config restructuring, realtime-vs-scheduled testing, and direct SQLite verification against Wazuh's FIM database all confirmed the file was never enumerated).
**What was proven:** the watcher's decision logic, HMAC signing, and delivery pipeline all function correctly, verified independently via the other three tests. The gap is specifically Wazuh's macOS FIM for newly created files, not this pipeline's escalation logic.
