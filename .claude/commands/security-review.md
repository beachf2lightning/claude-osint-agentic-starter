# Security review workflow

Review the requested code or change from a defensive security perspective.

## Focus areas

- Secret handling.
- Input validation.
- Unsafe file path handling.
- Shell command injection.
- Authentication and authorization boundaries.
- Logging of sensitive data.
- Dependency risk.
- Error messages that disclose too much.

## Required output

For each finding, include:

- Severity.
- File and line, if available.
- Risk.
- Concrete remediation.
- Suggested test, if relevant.

If no issues are found, say what was reviewed and why it appears safe.

