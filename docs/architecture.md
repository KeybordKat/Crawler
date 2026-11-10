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

## Diagram

```
 5 ┌─────────────────────────────────────────────────────────┐
   │ AGENTS / BEHAVIORS      src/crawler/agents/             │
   │ LLM loop · voice · person-following · remote control    │
   └──────────────────────────┬──────────────────────────────┘
                              │ calls only layer 4
 4 ┌──────────────────────────▼──────────────────────────────┐
   │ TOOL REGISTRY           src/crawler/tools/              │
   │ function-calling schemas · risk + blocking tags         │
   └──────────────────────────┬──────────────────────────────┘
                              │
 3 ┌──────────────────────────▼──────────────────────────────┐
   │ SKILLS                  src/crawler/skills/             │
   │ stand · walk · turn · read_distance ...                 │
   │ typed args, always return Result(ok, data, error)       │
   └──────────────────────────┬──────────────────────────────┘
                              │
 2 ┌──────────────────────────▼──────────────────────────────┐
   │ SAFETY / EXECUTOR       src/crawler/core/               │
   │ lock · limits · timeouts · cancel · e-stop              │
   │ battery / fall / obstacle guards                        │
   │ (the ONLY owner of the hardware)                        │
   └──────────────────────────┬──────────────────────────────┘
                              │
 1 ┌──────────────────────────▼──────────────────────────────┐
   │ HAL                     src/crawler/hal/                │
   │ Legs · Distance · Camera · Speaker · Battery            │
   │ ┌───────────────┐        ┌───────────────┐              │
   │ │ Mock versions │        │ Real versions │              │
   │ │ (run on Mac)  │        │ (run on Pi)   │              │
   │ └───────────────┘        └───────┬───────┘              │
   └──────────────────────────────────┼──────────────────────┘
                                      │
 0 ┌──────────────────────────────────▼──────────────────────┐
   │ SUNFOUNDER SDK (read-only)   vendor/                    │
   │ picrawler · robot-hat · vilib                           │
   └──────────────────────────┬──────────────────────────────┘
                              │
                        ┌─────▼─────┐
                        │ Hardware  │
                        └───────────┘
```

A request travels down one layer at a time and results travel back up.

## Rules
- Skills never touch the SDK directly, only the HAL (this enables mocks on the Mac).
- Every skill is a plain Python function usable without an LLM.
- Every skill returns `crawler.core.result.Result` (`ok`, `data`, `error`).
- Agents only call layer 4.
- Never edit `vendor/`.

## Development method: tests first
Every piece is built test-first (red, green, refactor):
1. **Red:** write a unit test for behavior that does not exist yet and watch it fail.
2. **Green:** write the smallest code that makes it pass.
3. **Refactor:** tidy up while the tests stay green.

- Tests live in `tests/`, in files named `test_<module>.py`.
- Test names describe the behavior, e.g. `test_failure_keeps_error_message`.
- Mac tests run against mock hardware. Tests that need the real robot are marked `@pytest.mark.hardware` and run only on the Pi.
- Each section below starts with its tests.

## Sections (build order)
1. Project skeleton and conventions  <- in progress
2. HAL and mocks
3. Safety and executor
4. Skills catalog
5. Tool registry
6. Agent and behaviors
7. Dev workflow (Mac -> Pi sync/deploy, testing)
