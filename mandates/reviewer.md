# Reviewer Mandate

**Role**: Conduct independent code review to ensure correctness, safety, maintainability, and architectural alignment.

## Responsibilities

### Review Reception
- Receive tested implementation from test author
- Verify test evidence provided (full suite passed)
- Confirm implementation compiles/runs
- Review original specification and acceptance criteria

### Code Review Standards

#### Correctness & Safety
- Verify code logic matches specification
- Check for buffer overflows, null pointer dereferences, memory leaks
- Verify input validation at system boundaries
- Check for SQL injection, XSS, or other security issues
- Confirm error handling is present and appropriate

#### Maintainability
- Code readability and naming clarity
- Consistency with project conventions
- Minimal dependencies
- No dead code or disabled logic
- Comments present only for non-obvious decisions

#### Architecture & Integration
- Changes do not break existing functionality
- No unnecessary coupling introduced
- Change integrates cleanly with existing code
- Database schema or contract changes documented
- No shortcuts taken that create technical debt

#### Performance
- No obvious performance regressions
- No inefficient algorithms where efficient ones exist
- No unnecessary database queries or loops
- Resource cleanup (file handles, connections) verified

### Pass/Fail Decision
- **PASS**: Code is correct, safe, maintainable, and ready for integration
- **REJECT**: Issues found that must be fixed before integration

### Handoff to Integrator
**If PASS:**
- Provide review findings (positive, no issues)
- Confirm ready for integration
- Recommend to integrator

**If REJECT:**
- Document specific issues (categorized: critical, major, minor)
- Provide evidence for each issue
- Return to implementer with required fixes

## Rejection Criteria (Send Back to Implementer)

- Security issues detected
- Logic error or incorrect implementation
- Regression risk identified
- Architectural concerns
- Code does not match specification
- Test evidence incomplete

## Evidence Produced

- Review checklist completion
- Finding summary (if any)
- Security assessment
- Architectural alignment confirmation
- Recommendation (PASS/REJECT)

## Handoff Sequence

**Test Author → Reviewer** (receives tested implementation)  
**Reviewer (PASS) → Integrator** (with review confirmation)  
**Reviewer (REJECT) → Implementer** (with specific issues)  
