# Software Architecture

Goal: low-level robot functions that double as **agentic tools** for a local LLM
(Raspberry Pi 5, 8 GB, on order; the robot currently runs a Pi 3). Everything is organised in strict layers.

## Decisions

| Topic | Decision | Notes |
|---|---|---|
| LLM location | Local, on the Pi 5 | Tools run in the same process as the agent |
| Tool protocol | Plain function-calling schemas | MCP may be added later as a thin wrapper over layer 4 |
| Concurrency | Threads + a hardware lock | SDK is blocking; executor is the only hardware owner |
| Target hardware | Pi 5 (8 GB) | Robot runs a Pi 3 (B+) until the Pi 5 arrives. Design for the Pi 5, keep Pi 3 code lightweight, no local LLM on the Pi 3 |
| Development method | Test-first | See "Development method: tests first" |
| HAL return values | Plain values (`float`, `bool`, ...) | HAL is low-level. Skills (layer 3) wrap outcomes in `Result` |
| HAL errors | Raise, never return magic numbers | `ValueError` for a request outside hardware limits. `HardwareError` when the hardware fails (e.g. sensor timeout) |
| Real vs mock location | Separate files, real ones imported lazily | Interface + mock in `hal/<name>.py`, real in `hal/real/<name>.py`, chosen by a factory |

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

## HAL design
Each interface (`Distance`, `Battery`, `Legs`, `Speaker`, `Camera`) has three parts:
1. **Interface:** an abstract class in `hal/<name>.py`.
2. **Mock:** e.g. `MockDistance`, in the same file. Runs on the Mac, returns values tests control, and can be told to fail on demand.
3. **Real:** e.g. `RealDistance`, in `hal/real/<name>.py`. Wraps the SDK and runs only on the Pi.

```
hal/
  distance.py      interface + MockDistance
  battery.py       ...
  real/            Pi only, imported lazily
    distance.py
```

- A factory function (e.g. `create_hal(real=True/False)`) is the single place that picks mock or real. It imports `hal/real/` only on the Pi, so the Mac never imports the SDK.
- Any implementation, mock or real, must pass the same shared contract tests.
- Error handling: `ValueError` for a bad request (outside hardware capability, e.g. speed above the maximum). `HardwareError` for a hardware failure with a valid request. `HardwareError` lives in `core/errors.py`.
- The SDK's `Ultrasonic.read()` returns `-1` on timeout and `-2` on a bad pulse. The real `Distance` must convert these into `HardwareError`, never pass them up as distances.
- The safety layer (layer 2) catches `HardwareError` and turns it into a `Result.failure(...)`.

HAL build order: `Distance`, `Battery`, `Legs`, `Speaker`, `Camera` (simple to complex).

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
1. Project skeleton and conventions  (done)
2. HAL and mocks  <- in progress
   - Done: `HardwareError`, `Distance` interface, `MockDistance` (with fail on demand), shared contract tests
   - Next: `Battery` (interface, mock, contract tests)
   - Pending on the Pi: `RealDistance` (add a `"real"` entry to the contract fixture, mark `@pytest.mark.hardware`)
3. Safety and executor
4. Skills catalog
5. Tool registry
6. Agent and behaviors
7. Dev workflow (Mac -> Pi sync/deploy, testing)
