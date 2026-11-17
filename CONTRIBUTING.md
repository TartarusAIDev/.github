# Contributing to Tartarus AI

Thanks for helping improve the Tartarus open-source ecosystem. These are the
org-wide defaults; a repo may add its own `CONTRIBUTING.md` with specifics.

## Ways to contribute

- **Report a bug** or **request a feature** with the issue templates.
- **Improve docs** — READMEs, examples, and the guides are all fair game.
- **Add examples** to [`tartarus-cookbook`](https://github.com/TartarusAIDev/tartarus-cookbook).
- **Fix a link or a fact** in [`awesome-uncensored-ai`](https://github.com/TartarusAIDev/awesome-uncensored-ai)
  or the guides — one verifiable change per PR.

## Pull requests

1. Fork and branch from `main` (`fix/…`, `feat/…`, `docs/…`).
2. Keep PRs focused — one logical change each.
3. Run whatever the repo ships: `npm test` (SDK/MCP), `python -m pytest` or the
   repo's validator (benchmark, lists). CI must pass.
4. Describe **what** changed and **why**. Link any issue it closes.
5. For anything user-facing, match the existing product terminology (see
   [`brand/guidelines.md`](brand/guidelines.md)).

## Facts over hype

Across these repos we don't publish unverified numbers — benchmark scores,
adoption, uptime, or feature claims. If you add a claim, cite a source or mark it
`unverified`. Editorial judgments should be labelled as such and kept separate
from source-backed facts.

## Reporting security issues

Do **not** open a public issue for a vulnerability. See [`SECURITY.md`](SECURITY.md).

## Code of conduct

Participation is governed by our [Code of Conduct](CODE_OF_CONDUCT.md).
