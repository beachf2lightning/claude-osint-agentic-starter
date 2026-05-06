# Passive OSINT playbook

This playbook is for defensive, authorized, passive collection only.

## Inputs

- Authorized scope file.
- Public documentation or asset inventory.
- API keys stored outside Git.

## Workflow

1. Confirm scope and non-goals.
2. Normalize domains, IP ranges, and hostnames.
3. Deduplicate and validate inputs.
4. Enrich with passive sources only.
5. Record source, timestamp, confidence, and limitations.
6. Generate a report that separates confirmed facts from hypotheses.

## Claude prompt

```text
Use /recon-pipeline.

Pipeline goal: Normalize and deduplicate an authorized scope file, then prepare records for passive enrichment.
Input: examples/osint-targets/authorized-scope.example.txt
Output: JSONL records with type, value, source, and confidence.
Safety: Offline tests only. No live lookups unless I explicitly approve them.
```

