# Software Architecture

Goal: low-level robot functions that double as **agentic tools** for a local LLM
(Raspberry Pi 5, 8 GB). Everything is organised in strict layers.

## Decisions

| Topic | Decision | Notes |
|---|---|---|
| LLM location | Local, on the Pi 5 | Tools run in the same process as the agent |
| Tool protocol | Plain function-calling schemas | MCP may be added later as a thin wrapper over layer 4 |
| Concurrency | Threads + a hardware lock | SDK is blocking; executor is the only hardware owner |

## Layers (a layer only calls the one directly below it)

| # | Layer | Purpose | Path |
|---|---|---|---|
| 0 | SunFounder SDK | `picrawler`, `robot-hat`, `vilib` (read-only) | `vendor/` |
| 1 | HAL | Interfaces (`Legs`, `Distance`, `Camera`, `Speaker`, `Battery`) with real + mock implementations | `src/crawler/hal/` |
| 2 | Safety / executor | Sole hardware owner: lock, limits, timeouts, cancel, e-stop, battery/fall/obstacle guards | `src/crawler/core/` |
| 3 | Skills | Agent-facing functions with typed args, returning `Result` | `src/crawler/skills/` |
| 4 | Tool registry | Generates function-calling schemas from skills; risk + blocking tags | `src/crawler/tools/` |
| 5 | Agents / behaviors | LLM loop, voice, person-following, remote control | `src/crawler/agents/` |

## Rules
- Skills never touch the SDK directly, only the HAL (this enables mocks on the Mac).
- Every skill is a plain Python function usable without an LLM.
- Every skill returns `crawler.core.result.Result` (`ok`, `data`, `error`).
- Agents only call layer 4.
- Never edit `vendor/`.

## Sections (build order)
1. Project skeleton and conventions  <- in progress
2. HAL and mocks
3. Safety and executor
4. Skills catalog
5. Tool registry
6. Agent and behaviors
7. Dev workflow (Mac -> Pi sync/deploy, testing)
