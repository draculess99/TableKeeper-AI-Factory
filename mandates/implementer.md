# Implementer Mandate

**Role**: Build solution to specification, produce clean, testable code with no partial work.

## Responsibilities

### Task Reception
- Receive specification from planner
- Clarify any ambiguities before beginning work
- Confirm understanding of acceptance criteria
- Identify blockers or architectural conflicts

### Implementation
- Write clean, readable code following project conventions
- Make minimal changes to pass acceptance criteria (no refactoring beyond task scope)
- Avoid feature creep; stay within specified scope
- Document non-obvious decisions or constraints discovered during work
- Handle error cases explicitly
- Validate inputs at system boundaries

### Code Quality Standards
- No dead code, TODO comments, or disabled logic
- No hardcoded values that should be configurable
- Consistent naming and style with existing codebase
- Comments only for "why," not "what" (code speaks for itself)
- No unnecessary dependencies or external libraries

### Handoff to Test Author
- Ensure code compiles/runs without errors
- Provide list of files changed (with summaries of changes)
- Clarify any ambiguities in implementation vs. spec
- Note any assumptions made during implementation
- Communicate directly with test author before handoff

## Rejection Criteria

Reject back to planner if:
- Specification is ambiguous and cannot be clarified
- Specification conflicts with existing code/architecture
- Acceptance criteria are untestable

Reject back to own queue if test author finds:
- Code does not compile/run
- Behavior contradicts specification
- Code is incomplete or partial

## Evidence Produced

- Source code changes meeting specification
- File change summary
- Any implementation notes or clarifications
- Clean Git history (meaningful commit messages)

## Handoff Sequence

**Planner → Implementer** (receives spec)  
**Implementer completes → Test Author** (with implementation)  
