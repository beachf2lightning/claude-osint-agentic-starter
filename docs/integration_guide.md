# Kent Analytic Framework - Integration Guide

## Files Delivered

| File | Purpose |
|---|---|
| estimative_language.py | Probability/confidence lexicon + helpers |
| kent_report_schema.py | Dataclass schema for structured report output |
| kent_system_prompt.md | System prompt block for Claude API calls |
| integration_guide.md | This file |

---

## Repo: claude-osint-agentic-starter

```
~/claude-osint-agentic-starter/
├── src/
│   └── osint_agentic_starter/
│       ├── estimative_language.py      <- copy here
│       └── kent_report_schema.py       <- copy here
└── docs/
    └── prompts/
        └── kent_system_prompt.md       <- copy here
```

---

## Production Stack: /opt/osintmcp

```
/opt/osintmcp/
└── app/
    ├── estimative_language.py          <- copy here
    ├── kent_report_schema.py           <- copy here
    └── agent.py                        <- edit: add system prompt injection
```

---

## agent.py - System Prompt Injection

```python
from pathlib import Path

KENT_SYSTEM_PROMPT = (
    Path(__file__).parent.parent / "docs" / "prompts" / "kent_system_prompt.md"
).read_text()

response = anthropic_client.messages.create(
    model="claude-sonnet-4-5",
    max_tokens=4096,
    system=KENT_SYSTEM_PROMPT,          # <- add this line
    messages=[
        {"role": "user", "content": findings_payload}
    ],
)
```

If you already have a system prompt, prepend:

```python
system = KENT_SYSTEM_PROMPT + "\n\n" + YOUR_EXISTING_SYSTEM_PROMPT
```

---

## Step 6 Payload - Add Schema Hint

```python
payload = {
    "target": target_domain,
    "threat_context": { ... },
    "report_schema": "kent_v1",
    "analytic_standard": "ICD-203",
}
```

---

## Validation After Integration

```bash
cd ~/claude-osint-agentic-starter
source .venv/bin/activate
./scripts/check.sh
```

Expected: ruff clean, mypy clean, all tests pass.

---

## Commit Message

```
Add Kent-style analytic framework (estimative language, report schema, system prompt)
```
