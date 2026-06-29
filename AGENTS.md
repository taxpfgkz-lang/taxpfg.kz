# Project Instructions

This repository follows the project guidance currently documented in `.claude/CLAUDE.md`.

Kilo should treat `.claude/CLAUDE.md` as the primary project instruction source for:
- product and milestone context
- stack and runtime constraints
- code conventions and naming
- CSS/JS/HTML editing rules
- architecture and workflow expectations

Additional repo-specific enforcement for Kilo:
- Prefer editing only `css/custom.css`, `css/base.css`, and `js/custom.js` unless the task explicitly requires broader markup changes.
- Treat vendor/theme assets as read-only unless the user explicitly asks otherwise.
- Preserve Russian-language comments and rationale style when modifying project-authored CSS/JS.
- When changing shared header/footer/page chrome, remember the markup is duplicated across all HTML pages and must stay consistent.
- Keep `custom.css` as the last stylesheet and `custom.js` as the last script when touching page asset order.
- Do not introduce a build step, bundler, or backend runtime into this static site.

If any instruction here conflicts with `.claude/CLAUDE.md`, follow `.claude/CLAUDE.md`.
