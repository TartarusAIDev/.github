# Palette

Lime accent on neutral near-black surfaces. The accent matches the live
`tartarusai.dev` / `dash.tartarusai.dev` brand.

## Accent (lime)

| Token | Hex | Use |
|---|---|---|
| `LIME`  | `#A3E635` | Primary accent — prompts, checks, bars, primary badge |
| `LIME2` | `#BEF264` | Light accent — gradient highlight end |
| `LIME3` | `#84CC16` | Deep accent — arrows, gradient mid |
| `LIMED` | `#4D7C0F` | Deepest accent — gradient start |

## Surfaces & text (neutral)

| Token | Hex | Use |
|---|---|---|
| `BG0`  | `#0B0D12` | Primary background |
| `BG1`  | `#151820` | Secondary surface (cards) |
| `BG2`  | `#1C2029` | Elevated surface (title bars) |
| `LINE` | `#2A2F3A` | Hairline border |
| `LINE2`| `#363C47` | Brighter border |
| `TXT`  | `#F5F6F8` | Main text / the mark |
| `MUT`  | `#A5AAB5` | Secondary text |
| `DIM`  | `#6B7280` | Faint text |

## The mark

The pinwheel mark is `TXT` white with two **lime** accent "eyes" (`LIME`). On a
light background use the light mark variant (dark body, lime eyes).

## Shields

Badges use `A3E635` for the accent and `0B0D12` as the label background
(`labelColor`), e.g. `style=for-the-badge&labelColor=0B0D12`.

> The brand previously used red (`#ED1C24`). Everything migrated to lime on
> 2026-11-16 to match the live sites. Don't reintroduce red.
