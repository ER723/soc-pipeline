# Live Verification Log

Periodic re-verification that the pipeline still genuinely works, not just a historical record from initial testing. Each entry is a real, dated run against the live system — not a repeat of old evidence.

---

## 2026-09-13 — Outage found, diagnosed, fixed, and re-verified

**What happened:** Requested a live re-test of the pipeline (unchanged since initial testing). Discovered the pipeline had silently stopped processing *any* events roughly ten days earlier (last entry in `alerts.json` was 2026-09-03) — not a single-rule issue, a full stall.

**Diagnosis:**
```
docker exec wazuh-manager /var/ossec/bin/agent_control -l
```
showed the agent status as `Unknown` with repeated `Cannot find 'queue/db/wdb'` errors — the same wedged internal-service state diagnosed once before during initial development. Root cause not fully determined (same as the earlier occurrence), but the fix is known and repeatable.

**Fix applied:**
```
docker compose down && docker compose up -d
```
Full container recreation (not just a restart) cleared the wedged state. Agent status returned to `Active` immediately after.

**Verification, part 1 — base detection, unmodified config:**
Triggered a real `sudo` failure (3 incorrect passwords). Rule `5404` ("Three failed attempts to run sudo") fired correctly at its default severity (level 10), confirming the underlying detection pipeline — agent → manager → decision log — was genuinely healthy again. Decision: `logged` (not escalated), which is *correct* behavior — the custom escalation rule had been intentionally reverted to empty after initial testing, specifically so routine events wouldn't stay permanently over-escalated. See `known-limitations.md` for why this matters.

**Verification, part 2 — full escalation path, rule temporarily restored:**
Re-added custom rule `100100` (same content used in original testing), restarted the manager, and re-triggered the identical sudo failure test.

```json
{"decided_at": "2026-09-13T13:25:32.361812+00:00", "decision": "escalated", "rule_id": "100100",
 "rule_level": 12, "rule_description": "SOC Pipeline: Repeated sudo authentication failures — escalated (possible brute force)"}
```

Confirmed landing in both Discord and the Google Sheet, same as the original test months earlier. `local_rules.xml` was then reverted back to empty immediately after, restoring the intended default (tuned, non-escalating) state.

**Why this matters for the portfolio:** this wasn't a clean re-run — it surfaced a real infrastructure failure mode (silent, ten-day event-processing stall) that the original testing never encountered. Finding it, diagnosing it methodically rather than guessing, and confirming the fix with two separate levels of evidence (base detection, then full escalation) is a more realistic demonstration of SOC-relevant troubleshooting than a test that simply worked on the first try.
