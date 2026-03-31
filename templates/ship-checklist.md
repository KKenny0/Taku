# Pre-Ship Checklist

Run through this checklist before every ship. Every item must pass or be explicitly accepted.

---

## Tests

- [ ] All tests pass (fresh run, not cached output)
- [ ] No new tests are skipped or marked `todo`
- [ ] Regression tests have red-green verification

## Code Quality

- [ ] Code reviewed (all findings addressed)
- [ ] No `TODO` in new code (move to issue tracker or fix now)
- [ ] No `FIXME` in new code
- [ ] No `HACK` in new code
- [ ] No debug logging in new code:
  - No `console.log` / `console.debug`
  - No `print()` statements (except in CLI tools)
  - No `debug!` / `dbg!` macros
  - No `fmt.Println` / `log.Debug` left in

## Version & Documentation

- [ ] `VERSION` bumped (semantic versioning)
- [ ] `CHANGELOG.md` updated (every commit represented)
- [ ] Breaking changes documented if any

## Security

- [ ] No secrets, API keys, or credentials in new code
- [ ] No hardcoded URLs pointing to non-production environments
- [ ] Auth checks present on all new routes/endpoints
- [ ] Input validation on all user-facing inputs

## Git

- [ ] Commits are bisectable (each independently valid)
- [ ] No broken imports or missing dependencies
- [ ] Commit messages follow convention (`feat:`, `fix:`, `chore:`, etc.)

## Final Verification

- [ ] `git diff <base>...HEAD` reviewed one last time
- [ ] No unintended files included
- [ ] Build succeeds (if applicable)
