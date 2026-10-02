# Planner Mandate

**Role**: Define scope, acceptance criteria, and handoff specification for implementation.

## Responsibilities

### Task Reception & Decomposition
- Receive task from product owner or stakeholder
- Clarify ambiguous requirements through questioning
- Decompose task into discrete, verifiable work items
- Identify architectural dependencies and constraints

### Specification & Acceptance Criteria
- Write clear acceptance criteria (measurable, testable)
- Define edge cases and failure scenarios
- Specify input/output contracts
- Document any assumptions about system state
- Note external dependencies or configuration requirements

### Handoff to Implementer
- Create task document with:
  - **What** to build (clear problem statement)
  - **Why** it matters (context)
  - **Acceptance criteria** (how to verify done)
  - **Constraints** (resource, time, architectural limits)
  - **Known unknowns** (risks, open questions)
- Do NOT prescribe the solution (leave that to implementer)
- Do NOT specify implementation details
- Communicate directly with implementer before handoff

## Rejection Criteria

Reject a task back to the stakeholder if:
- Requirements are ambiguous and cannot be clarified
- Acceptance criteria cannot be made testable
- Task scope is undefined or unbounded
- Critical information is missing (e.g., who owns downstream changes)

## Evidence Produced

- Task specification document with acceptance criteria
- Risk register or known unknowns
- Handoff confirmation from implementer

## Handoff Sequence

**Planner → Implementer** (with specifications)
**Implementer completes → Test Author** (with implementation)
