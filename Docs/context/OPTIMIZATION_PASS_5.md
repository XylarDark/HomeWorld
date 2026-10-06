# Optimization pass 5

Main when audited: `408080f`. Door check already passed.

- [x] No start-read regression. Metrics stay named. Index has no numbers. Claude import is intact.
- [x] The check now fails if the door names a markdown file that is not on disk. The tutorial path is exempt until it is committed. `route-context.md` is named by the read path, not this scan.
- [x] No always-apply Cursor rule added. The automation rule is `alwaysApply: false`.
