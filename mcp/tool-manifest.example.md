# MCP tool manifest example

Use this file to describe MCP tools before implementing them.

## Tool: passive_dns_lookup

- Type: Passive network enrichment
- Authorization: User must provide authorized domain or asset scope
- Secrets: `PASSIVE_DNS_API_KEY`
- Default mode: Dry-run or read-only
- Inputs:
  - `domain`: domain name inside authorized scope
- Outputs:
  - Normalized JSON records
- Safety notes:
  - Do not query unrelated third-party targets.
  - Do not store raw API responses containing sensitive client data in Git.

## Tool: normalize_targets

- Type: Local-only
- Authorization: Fixture or user-provided target file
- Secrets: None
- Default mode: Read-only input, write normalized output
- Inputs:
  - `path`: local target file path
- Outputs:
  - Deduplicated normalized targets
- Safety notes:
  - Validate paths before reading.
  - Treat input as untrusted.

