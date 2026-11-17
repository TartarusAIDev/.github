# Brand guidelines

## Naming

- The brand is **Tartarus** / **Tartarus AI**. The hosted model is **Tartarus
  Coder**.
- Package and repo names are lowercase and hyphenated: `tartarus-console`,
  `tartarus-sdk`, `tartarus-mcp`. Don't capitalize them mid-sentence.
- The API base is `https://api.tartarusai.dev/v1`; the model id is
  `tartarus-coder`.

## Voice

- Plain, technical, confident. Explain capability; don't oversell.
- The one positioning line: **"ships code instead of refusals."** Vary the
  wording, keep the meaning.
- No unverified numbers. No benchmark scores, adoption, uptime, or feature claims
  without a source. Mark judgments as judgments.
- Don't name the upstream base model or its provenance in user-facing copy —
  public surfaces say "Tartarus Coder."

## Typography in assets

- Wordmark and mark are vector paths — never retype "Tartarus" as live text next
  to the mark.
- Headlines: bold system sans. Code / terminal: monospace stack.

## Do

- Use the generated assets; regenerate via `make-assets.py` rather than editing
  SVGs by hand.
- Keep the lime accent (`#A3E635`) and the near-black surfaces.
- Give every outbound link to our own properties UTM parameters
  (`utm_source=github`, `utm_campaign=<repo>`, `utm_content=<slot>`).

## Don't

- No red (legacy), no gradients-as-decoration, no emoji as iconography.
- No giant centered walls of Markdown, no badge soup (a few meaningful badges
  only).
- No fake terminal animations or invented screenshots.
