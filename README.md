# wheel-it

> 繁體中文：[README.zh-TW.md](README.zh-TW.md)

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

**Find the wheel before you build it.** One skill lives here: `wheel` — prior-art search before building (official docs / community consensus / mature open-source repos → a wheel card with a 7-level verdict), plus an optional reverse pass that reads what a shipped, closed-source artifact actually depends on.

The coding-agent behavior doctrine (pre-work discipline, research-first, stop-loss, acceptance, dispatch) now lives in [royalskynet/ether-code](https://github.com/royalskynet/ether-code); its `coding-hermes` Layer 2 points back at this repo's `wheel`.

**Skill type:** doc-only discipline, no runtime dependency; ships one standard-library registry CLI.

## Install

```bash
npx skills add https://github.com/royalskynet/wheel-it --skill wheel
```

Installs to `~/.hermes/skills/wheel/`. **Start a new session** for it to be indexed.

## `/wheel` does three things by default

| # | Job | When |
|---|---|---|
| 1. Decision | official docs + community consensus + mature repos feed a 7-level verdict (build / don't / which one) | every time |
| 2. Wheels | inventory of mature options: adoption, license, maintenance, for glue or adoption | every time (Quick runs only this lane) |
| 3. Reverse | target is closed-source (Electron / APK / binary / private-registry package) → infer its dependencies and design from the artifact | when the context needs it or the user asks, not every time |

The reverse pass stops at facts and inventory: asar/package listings, `otool -L`, `codesign -dv`, strings, sourcemaps. No whole-binary decompilation, no DRM. Full REA (Ghidra/IDA deep decompilation) is out of scope.

## What it does

- **Restate** — "what if we did nothing?" can end at `不做`; a different real problem ends at `換題`.
- **Depth** — Quick / Standard / Full / Full+reverse; not everything runs every time.
- **Three lanes + a closed-source lane** — gh issues, HN, Stack Overflow for community consensus; `gh search repos` / npm / pip / brew for wheels; deps.dev + download counts to pick the leader; read-only commands for the closed-source lane.
- **Scoring** — activity, license, cost, reversibility, adoption, recurring complaints; stars sort candidates, they do not score them.
- **7-level verdict** — 不做 / 換題 / 設定 / 採用 / 改用 / 借鏡 / 自造; building is the last rung.
- **Asymmetric gate** — a second opinion only for `自造` or a warned adoption.
- **Wheel card** — ≤12 lines; the `輪子：` line of a plan is its first line.
- **Registry** — one row per card; `review_by` expires by domain speed (30 / 90 / 180 days).

## Registry

```bash
python3 skills/wheel/scripts/wheel_registry.py find "<keyword>" "<English term>"   # step 0
python3 skills/wheel/scripts/wheel_registry.py add "設定｜借鏡" "<problem>" "<choice>" 90
python3 skills/wheel/scripts/wheel_registry.py check
```

Five-column TSV: date, verdict, problem, choice, review_by; stored in `~/.wheel/registry.tsv` (`WHEEL_REGISTRY` overrides). Standard library only, no network. When the script is absent the skill has equivalent `grep`/`printf` fallbacks, and `scripts/test_skill.py` executes that prose verbatim to keep the two in agreement.

## Tests

```bash
python3 skills/wheel/scripts/test_wheel_registry.py   # 144 checks: grammar, expiry, exit codes
python3 skills/wheel/scripts/test_skill.py            # 30 checks: SKILL.md ↔ CLI contract, fallbacks run
```

## When it triggers / doesn't

**Triggers:** about to build, choosing a tool, "is there an existing/standard way", "what's the latest version", adding a dependency or subsystem, writing more than glue, or two failed attempts at the same approach.

**Does not trigger:** typos, editing existing code, concept explanations, continuing a fresh wheel card.

## Origin

`wheel` merges the design ideas of deja-vu (verdicts + asymmetric gate) with dont-reinvent (license / maintenance checks); Layer 2 of `coding-hermes` was extracted into this standalone skill in v2.4.0. See [HISTORY.md](HISTORY.md) for versions.

## License

MIT. Copyright (c) 2026 royalskynet.
