# .github

This repository powers the **[Tartarus AI](https://tartarusai.dev/?utm_source=github&utm_medium=readme&utm_campaign=dotgithub&utm_content=intro)** GitHub organization. It is infrastructure, not an end-user product.

It holds:

- **`profile/README.md`** — the public organization profile shown at
  [github.com/TartarusAIDev](https://github.com/TartarusAIDev).
- **`profile/assets/`** — the generated brand art (hero, ecosystem diagram,
  feature cards, mark and wordmark).
- **`brand/`** — the design system: palette, usage guidelines, and the
  `make-assets.py` generator that produces every SVG from the real mark geometry.
- **Community health defaults** — `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`,
  `SECURITY.md`, `SUPPORT.md`, and the issue / pull-request templates under
  `.github/`. GitHub applies these to every repo in the org that doesn't define
  its own.

## Regenerating the brand assets

```bash
cd brand
python make-assets.py
```

Pure standard library, deterministic. Assets are written into `profile/assets/`
and into each repo's `assets/` folder. See [`brand/README.md`](brand/README.md).

## Looking for the product?

- Website — https://tartarusai.dev
- Dashboard — https://dash.tartarusai.dev
- CLI — `pip install tartarus-console` ([repo](https://github.com/TartarusAIDev/tartarus-console))
