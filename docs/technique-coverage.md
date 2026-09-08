# Technique Coverage — What This Pipeline Can and Can't Detect

Compiled from direct testing, not assumption.

## Reliably detected (proven working)

| Source / Mechanism | Example techniques | Default severity | Notes |
|---|---|---|---|
| Sudo authentication events | T1110 (Brute Force), T1548 | 4-10 | Reliable. Needs custom-rule escalation to cross a typical threshold. |
| Rootcheck | T1014 (Rootkit) | 7 | Most reliable detection source tested. |
| Network port/service changes (netstat-based) | T1571, T1046 | 7 | Fires on both open and close. Expect to allowlist routine noise. |
| Agent lifecycle events | operational | 3 | Pipeline health, not threat detection. |
| SCA / CIS benchmark checks | Compliance/hardening posture | 3-7 | Config drift, not live attack detection. |
| File integrity — existing file enumeration only | Baseline verification | - | Confirmed on /bin, /sbin, /usr/bin, /usr/sbin, LaunchAgents via scheduled scans. Realtime does not work. |
| CVE/threat awareness | General vulnerability awareness | - | Custom weekly script (CISA KEV), not Wazuh-native. |

## Not suitable / does not work on this platform

| Source / Mechanism | Why it fails | Verified how |
|---|---|---|
| Realtime file integrity monitoring | Not implemented by Wazuh for macOS — officially Windows/Linux only. | Wazuh's own documentation. |
| FIM detection of newly created files (even scheduled) | Files register in baseline but additions are not reliably alerted on. | Direct SQLite queries against fim.db, repeated across techniques and reboots. |
| FIM enumeration of /etc specifically | Directory registers but contents never enumerate. | Direct database verification; extensively diagnosed, root cause undetermined. |
| SSH-based brute force detection | Rules exist at level 14 but written for Linux syslog format; macOS sshd logs don't match. | Zero matches across repeated real SSH failed-login tests. |
| TCC / privacy-permission event detection | Log source collected, but zero alerts generated across multiple real trigger attempts. | Not fully diagnosed — flagged unreliable. |
| Wazuh's built-in Vulnerability Detection module | No destination to publish results without an indexer; silently consumed 8.8GB before being disabled. | Direct disk usage measurement. |
| Severity-12+ escalation from any technique's default score | Default level 12+ rules require correlated, multi-source evidence a single benign local tester can't produce. | Verified via direct ruleset inspection; every real technique topped out at level 10 or below by default. |

## Practical implication

Well-suited to host-based, single-machine threat detection with locally-observable indicators. Not suited to network-level attacks not touching the monitored host, anything relying on macOS realtime file monitoring, or out-of-the-box severity scoring for a production threshold — custom rule tuning is required, not optional.
