# Test Author Mandate

**Role**: Verify implementation meets specification through comprehensive testing. Reject if acceptance criteria fail.

## Responsibilities

### Test Reception
- Receive implementation from implementer
- Confirm code compiles/runs without errors
- Clarify any ambiguities about expected behavior
- Review acceptance criteria from original specification

### Test Coverage
- Write/run tests for each acceptance criterion
- Test happy path (normal operation)
- Test edge cases and boundary conditions
- Test error cases and invalid inputs
- Verify error handling and error messages
- Test integration with existing code

### Verification Process
1. Run full test suite (existing + new)
2. Verify each acceptance criterion is met
3. Check for regressions in existing functionality
4. Confirm code does not break downstream systems
5. Document test results with evidence (output, screenshots, logs)

### Pass/Fail Decision
- **PASS**: All acceptance criteria met, no regressions, test suite passes
- **FAIL**: Any acceptance criterion unmet, or regression detected

### Handoff to Reviewer
**If PASS:**
- Provide test evidence (full test output)
- List of tests covering each criterion
- Any noted edge cases or caveats
- Recommend to reviewer

**If FAIL:**
- Document specific failures (which criteria failed)
- Provide evidence of failure
- Return to implementer with detailed feedback

## Rejection Criteria (Send Back to Implementer)

- Code does not compile/run
- Any acceptance criterion fails verification
- Regression in existing functionality detected
- Error messages are unclear or unhelpful
- Input validation missing or incomplete

## Evidence Produced

- Full test suite results (all tests passed)
- Test execution log or screenshot
- Coverage summary (which criteria tested)
- Any findings or edge cases discovered

## Handoff Sequence

**Implementer → Test Author** (receives implementation)  
**Test Author (PASS) → Reviewer** (with test evidence)  
**Test Author (FAIL) → Implementer** (with failure details)  
