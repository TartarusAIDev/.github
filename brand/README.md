# Tartarus AI — brand kit

The design system behind the org profile and every repo banner. One generator,
one palette, one mark.

## Files

| Path | What |
|---|---|
| `make-assets.py` | Generates every SVG from the real mark geometry. Pure stdlib. |
| `src/logo-src.svg` | The production pinwheel mark (source of truth for geometry). |
| `src/wordmark-src.svg` | The production "Tartarus AI" wordmark. |
| `colors.md` | The palette, with hex values and roles. |
| `guidelines.md` | Usage rules: naming, voice, do / don't. |

Generated output lands in `../profile/assets/` (hero, ecosystem, feature cards,
mark, wordmark) and in each repo's `assets/banner.svg`.

## Regenerate

```bash
python make-assets.py
```

Deterministic — same input, same bytes. Commit the regenerated SVGs.

## How it works

The generator loads the real mark and wordmark, recolours the accent from the
legacy red to the live-site **lime** (`#A3E635`), converts CSS classes to inline
fills (so GitHub's SVG sanitizer renders them), then composes each asset from
shared primitives: the dot-grid background, the lime radial glow, the terminal
card, chips, and the bottom accent bar.

Because the mark and wordmark are **vector paths**, they render identically
everywhere and don't depend on any font being installed. Headline and body text
use a system font stack and fall back cleanly.

## Rendering notes

- Assets are self-contained SVG (no external fonts, scripts, or images), so they
  render in GitHub light and dark mode and can't phone home.
- Each hero/banner bakes in its own dark background, so it looks the same against
  GitHub's light or dark page.
- To preview as raster: `node -e "require('sharp')('file.svg').png().toFile('out.png')"`.
