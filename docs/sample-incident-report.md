# Sample Incident Report: Repeated sudo Authentication Failures (T1110)

> **Scope note:** This is a Tier-1 write-up of a *controlled test event* from the live pipeline's verification run on 2026-09-13, not a real intrusion. It is written the way I would hand a genuine alert to Tier 2. Anything the test record did not capture is marked as such rather than filled in.

| Field | Value |
|---|---|
| Incident ID | SAMPLE-2026-09-13-01 |
| Decision time | 2026-09-13 13:25:32 UTC |
| Source | Wazuh agent on a monitored macOS host, reporting to the Wazuh manager |
| Detection | Wazuh rule `5404` ("Three failed attempts to run sudo"), level 10, reclassified by custom rule `100100` to level 12 |
| ATT&CK | T1110 Brute Force |
| Pipeline decision | **Escalated** (level 12 meets the escalation threshold of 12) |
| Verdict | True positive for the detection; benign cause (authorised test by the system owner) |
| Analyst | Anggasukmana Adisastra (Tier 1) |

## 1. Summary

Three failed `sudo` password attempts on the monitored host raised rule 5404. The pipeline's custom rule lifted it to level 12, so the watcher escalated it, and it was delivered to Discord and the Google Sheet escalation queue with a valid HMAC signature. The cause was my own test (`sudo -k && sudo -v`, three deliberately wrong passwords), so no response action was needed.

## 2. Evidence

The pipeline's decision record for this event:

```json
{"decided_at": "2026-09-13T13:25:32.361812+00:00", "decision": "escalated", "rule_id": "100100",
 "rule_level": 12, "rule_description": "SOC Pipeline: Repeated sudo authentication failures — escalated (possible brute force)"}
```

## 3. Timeline (UTC)

| Time | Event | Basis |
|---|---|---|
| Just before 13:25:32 | Three wrong passwords entered at the `sudo` prompt | Test procedure; exact second not recorded |
| Just before 13:25:32 | Rule 5404 fires at level 10; rule 100100 reclassifies to level 12 | Rule configuration |
| 13:25:32 | Watcher decision: `escalated` | Decision log (above) |
| Shortly after | HMAC-signed webhook accepted; alert appears in Discord and the Sheet | Verification log |

## 4. Analysis

Repeated `sudo` failures matter because they can mean someone already on the host is guessing a privileged password, or misusing a stolen account. Before closing a real alert like this I would check:

1. **Which account and terminal?** Did the failures come from the account's normal owner?
2. **Is it a pattern?** One slip of the fingers is normal. Several bursts, or failures at odd hours, are not.
3. **Did a success follow?** Failures followed by a successful `sudo` is the worrying sequence.
4. **Was anyone expecting this?** An admin test or change window explains it.

**Not captured in the test record:** account name, terminal, and the full raw alert. In a real case I would pull these from the manager's full alert log before deciding.

## 5. Verdict and reasoning

Benign. The timing and count match a test I ran myself, and I knew the cause before the alert arrived. I would not close an unexplained alert on timing alone.

## 6. Handoff to Tier 2 (if this had been real)

Escalate with: the rule IDs and levels above, the decision time, the account and terminal (to be retrieved), whether a successful `sudo` followed, and whether other hosts showed similar failures.

## 7. Tuning notes

- Rule 5404 is level 10 by default, below this deployment's escalation threshold, so the pipeline never escalates it without a custom rule. The custom rule is deliberately **kept empty in normal operation** so routine mistyped passwords do not flood Tier 2. It was re-enabled only for this verification, then reverted (see `live-verification-log.md`).
- A better production rule would escalate on a **pattern** rather than a single event: repeated failures within a window, or failures followed by success. That is the logic I implemented in my `soc-log-analyser` project.

## 8. Limits of this report

One monitored macOS host, a controlled test, and a decision-log record that holds only a few fields. It demonstrates the triage and write-up method, not experience of a live incident.

*Source evidence: `docs/portfolio-test-results.md` and `docs/live-verification-log.md` in this repository.*
