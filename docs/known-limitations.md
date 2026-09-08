# Known Limitations & Operational Drawbacks

Documented directly from what was actually encountered building and testing this pipeline.

## Detection-layer limitations

See `technique-coverage.md`. Summary: realtime FIM doesn't exist on macOS by Wazuh's design; scheduled FIM has an unresolved reliability gap for newly-created files; /etc specifically never enumerates; SSH and TCC event sources don't produce usable alerts on this platform; the built-in vulnerability scanner cannot function without an indexer.

## Severity ceiling — the most consequential finding

Wazuh's default ruleset scores essentially every macOS-native, single-host event at or below level 10. Severity-12+ rules in the default ruleset are built for correlated, multi-source attack evidence. In practice: out of the box, this pipeline will never escalate anything to a human, regardless of what happens on the monitored machine, unless custom rules are written to reclassify specific events. This must be addressed deliberately before this pipeline is useful in practice.

## Operational fragility

- Container config resets on volume changes. Custom rules and manual ossec.conf edits live in a Docker-managed volume; if it's ever removed/recreated, they're silently lost. Fixes applied via a bind-mounted cont-init.d init script do survive, since they reapply on every boot — this pattern is recommended for any permanent fix.
- Silent disk accumulation is a real, recurring risk. Any Wazuh module that phones home to infrastructure this architecture doesn't have can silently consume many gigabytes with zero visible symptoms. Happened twice during development (9.4GB and 9.5GB). Periodically check `docker system df -v`.
- A misconfigured secret fails silently, not loudly. During testing, the HMAC secret was accidentally reset to a placeholder. Escalations continued to be "sent" but were silently rejected by the receiver's signature check, visible only in a Debug tab most people wouldn't think to check.
- Docker Desktop's own updater has repeatedly failed on this deployment, requiring manual reinstallation each time.

## Scope limitations by design

- Single point of failure — one Mac, no redundancy, no failover.
- Host-based only — no network-level visibility.
- No redundant alerting path — if Discord or Google's services are unavailable, escalations have no fallback delivery mechanism.

## What this means for anyone considering deploying this pipeline

A genuinely working, tested, host-based detection and escalation pipeline for a single macOS machine, validated against real technique execution. Well suited to personal security monitoring, a home lab, or a portfolio demonstration. Not a substitute for enterprise-grade tooling with redundancy, network visibility, and professionally-maintained severity baselines. The gap between "detects real things" and "escalates real things at a useful severity" is real and must be closed deliberately through custom rule work.
