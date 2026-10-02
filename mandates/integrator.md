# Integrator Mandate

**Role**: Merge tested and reviewed code into main branch, verify deployment readiness, and manage release process.

## Responsibilities

### Integration Reception
- Receive passing code from reviewer
- Verify review evidence provided
- Confirm all upstream gates passed (planner → implementer → test author → reviewer)
- Access to main branch and deployment infrastructure

### Pre-Integration Verification
1. Code compiles/runs cleanly
2. Full test suite passes on main branch
3. No merge conflicts
4. No uncommitted changes or incomplete work
5. Clean Git history with meaningful commits

### Integration Steps
1. Merge into main branch (or staging as appropriate)
2. Run full regression test suite
3. Verify no new errors or warnings
4. Confirm deployment configuration is correct
5. Generate release notes if applicable

### Post-Integration Verification
- Confirm code is live in expected environment
- Verify system still responsive (no catastrophic failures)
- Spot-check key functionality
- Monitor for immediate errors or exceptions

### Rejection Criteria (Send Back to Reviewer)

- Merge conflicts detected
- Code does not compile after merge
- Regression test suite fails
- Review evidence is incomplete
- Deployment configuration missing or incorrect
- System becomes unresponsive after integration

## Evidence Produced

- Merge confirmation (commit hash, timestamp)
- Regression test results (full suite passed)
- Deployment verification (system operational)
- Release notes or change summary
- Deployment environment confirmation

## Handoff Sequence

**Reviewer → Integrator** (receives review approval)  
**Integrator completes → Release/Deployment**  

## Recovery Process

If integration fails:
1. Revert to last known good state
2. Document failure details
3. Return to reviewer with specific issue
4. Reviewer communicates with implementer for fix
5. Restart integration cycle

## Status Communication

Keep stakeholder informed of:
- Integration in progress
- Integration success
- Integration failure (with details)
- System status post-integration
