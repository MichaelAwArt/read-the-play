# CLAUDE.md — working notes for Claude Code

Project: **Read the Play**, Team AwArt's entry for the SIC Data-hack 2026 (ThinkSport × Spengler Cup Davos).
Owner: Michael Rohrer (non-technical, writes in French; answer him in French, keep code/comments/UI in English).

## Hard rules

- The challenge data (Wisehockey CSV/XLSX, game videos) is **confidential**. Never commit it, never paste it into issues, PRs or public files. Only `data/sample-sequence.js` (invented) is public.
- Real data lives in `private/` (git-ignored): `private/sequence.js`, `private/clip.mp4`.
- Never write passwords, tokens or download links of the challenge data into the repo.
- Keep it a static site: no build step, no backend, until the team reaches the final.

## Structure

- `index.html` — the whole app (HTML + CSS + JS, single file). Loads `data/sample-sequence.js`, then `private/sequence.js` if present (overrides `window.RTP_DATA`).
- `assets/awart-logo.png` — AwArt round badge.
- `data/sample-sequence.js` — invented sequence: `snaps` (time → player positions in metres), `puckFree` (puck keyframes when free), `carry` ([playerId, from, to]), `players` (name, team, stats).
- `scripts/extract_sequence.py` — builds `private/sequence.js` from a Wisehockey events CSV (`--period --from --to`, MatchClock seconds). `puckFree`/`carry` are filled by hand from the printed PuckControl events.

## Key conventions in index.html

- Rink SVG in metres: viewBox `-31 -16 62 32`, zoom box `VB_ZOOM=[-30.5,-13.6,29.5,15.2]`, svg y = −data y.
- Video sync: data t = video t + `V_OFF` (2.4 s for the Kessler clip). Marker keyframes `MK` in 960×492 video pixels. Slow-mo zoom: `ZOOM_FROM 1.9`, `ZOOM_TO 4.9`, scale 2.1, rate 0.4, origin keyframes `ZO`.
- No video (missing file or error) → `window.NO_VIDEO` → 2D tracking replay.
- i18n: `I18N` dictionary EN → [FR, DE], MutationObserver translates text nodes; choice saved in localStorage.
- Theme tokens: background gradient #0A2650 → #061631 → #041027 with cyan glow; panels rgba(19,51,95,.72); text #FFF / muted #A9BED6; data cyan #4FD3E0 / #00CCD9; AwArt red #FF1A1A; fonts Anton (titles) + Poppins. Vote colours: bad #7F93B0, neutral #C9D6E3, good #2FC28C, exceptional #F2C230.

## Flow

Start → setup ("Watch #72 Kessler") → clean clip → auto zoomed slow-mo (Skip) → vote (Watch again / Slow-mo zoom) → 4 reveal stories (crowd · decision time vs fan time · what he saw, tap a player · what came next) → expert verdict → share card.

## Run / test

`python -m http.server 8000` → http://localhost:8000. For automated checks use Playwright (headless Chromium has no H.264, so it tests the 2D fallback).
