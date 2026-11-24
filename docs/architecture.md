# Software Architecture

Goal: low-level robot functions that double as **agentic tools** for a local LLM
(Raspberry Pi 5, 8 GB, now installed in the robot). Everything is organised in strict layers.

## Decisions

| Topic | Decision | Notes |
|---|---|---|
| LLM location | Local, on the Pi 5 | Tools run in the same process as the agent |
| Tool protocol | Plain function-calling schemas | MCP may be added later as a thin wrapper over layer 4 |
| Concurrency | Threads + a hardware lock | SDK is blocking; executor is the only hardware owner |
| Target hardware | Pi 5 (8 GB) | Pi 5 is installed in the robot (with fan), not yet set up. It replaces the earlier Pi 3 (B+) |
| Audio hardware | USB speaker and USB microphone | The HAT's onboard speaker was removed and the HAT has no mic. The real `Speaker` uses USB audio, not the HAT. See `docs/hardware_plan.md` |
| Display hardware | iPistBit 4.3" DSI screen (ordered) | Not yet tested on the Pi 5. Falls back to an SPI screen on the HAT if it does not work. A `Display` HAL interface will be added. See `docs/hardware_plan.md` |
| Development method | Test-first | See "Development method: tests first" |
| HAL return values | Plain values (`float`, `bool`, ...) | HAL is low-level. Skills (layer 3) wrap outcomes in `Result` |
| HAL errors | Raise, never return magic numbers | `ValueError` for a request outside hardware limits. `HardwareError` when the hardware fails (e.g. sensor timeout) |
| Real vs mock location | Separate files, real ones imported lazily | Interface + mock in `hal/<name>.py`, real in `hal/real/<name>.py`, chosen by the assembler |

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

- An assembler function (`assemble_hal(real=True/False)`, in `hal/assembler.py`) is the single place that picks mock or real. It imports `hal/real/` only on the Pi, so the Mac never imports the SDK.
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
   - Done: `Battery` interface, `MockBattery` (with fail on demand, `read_voltage()` returns volts as a float), shared contract tests
   - Done (mock side): `Legs` (interface, mock that records the actions it is asked to perform, contract tests). Only the real legs are left, which need the Pi
     - Done: `stand()` and `sit()` on the interface and `MockLegs` (records actions, fail on demand, failed actions are not recorded), with tests for each
     - Done: `walk(direction, steps, speed)` on the interface and `MockLegs`, the first method with arguments. Records `("walk", direction, steps, speed)` as a tuple, with fail on demand (failed walks are not recorded), and a test for each
     - Done: `ValueError` validation for `walk`, built one red test at a time. Speed must be 0-100 (0 is the slowest, not stopped), direction must be `"forward"` or `"backward"`, and steps must be a positive `int`. The checks run before the fail-on-demand check, so a bad request is always a `ValueError`
     - Done: refactored the repeated tests with `pytest.mark.parametrize` (failed actions are not recorded, actions are recorded, `walk` rejects bad requests)
     - Done: consistent recorded format. Every action is a tuple with the action name first, then its arguments: `("stand",)`, `("sit",)`, `("walk", direction, steps, speed)`
     - Done: shared contract tests for `Legs`, using a `legs` fixture (only a `"mock"` entry for now). They check that `walk` rejects bad requests, and that `stand`, `sit` and a valid `walk` (including speeds 0 and 100) succeed. Mock-only behavior (`actions`, `fail=True`) stays out of the contract tests
     - Done: `turn(direction, steps, speed)` on the interface and `MockLegs`, built test-first like `walk`. Direction must be `"left"` or `"right"`. Records `("turn", direction, steps, speed)`, with fail on demand (failed turns are not recorded). Bad requests raise `ValueError` before the fail check
     - Done: refactor. The shared request rules (speed 0-100, steps a positive `int`, direction in an allowed set) live in one helper, `Legs._check_request`, on the interface so every implementation, including the real one, gets the same rules. `walk` and `turn` call it with their own allowed directions
     - Done: `turn` added to the contract tests (`test_turn_succeeds`, plus bad-request tests that use the `legs` fixture)
     - Later: a `"real"` entry in the `legs` fixture on the Pi (marked `@pytest.mark.hardware`)
   - Done (mock side): `Speaker` (interface, mock that records what it is asked to say, contract tests). Only the real speaker is left, which needs the Pi
     - Done: `speak(text)` on the interface and `MockSpeaker`, built test-first. The mock records each text in a `spoken` list, with fail on demand (a failed speak is not recorded)
     - Done: `ValueError` validation, built one red test at a time. Text must be a string and must not be empty or whitespace-only. The checks run before the fail-on-demand check, so a bad request is always a `ValueError`
     - Done: refactor. The shared rules live in one helper, `Speaker._check_request`, on the interface so every implementation, including the real one, gets the same rules. The bad-request tests are one `pytest.mark.parametrize` test
     - Done: shared contract tests for `Speaker`, using a `speaker` fixture (only a `"mock"` entry for now). They check that `speak` succeeds and that bad requests raise `ValueError`. Mock-only behavior (`spoken`, `fail=True`) stays out of the contract tests
     - Later: a `"real"` entry in the `speaker` fixture on the Pi (marked `@pytest.mark.hardware`)
   - Done (mock side): `Camera` (interface, mock, contract tests). Only the real camera is left, which needs the Pi and the new 22-to-15-pin camera cable
     - Done: `take_photo()` on the interface and `MockCamera`, built test-first. It returns the photo as `bytes`, with fail on demand (`fail=True` raises `HardwareError`)
     - Done: shared contract test for `Camera`, using a `camera` fixture (only a `"mock"` entry for now). It checks that `take_photo` returns `bytes`. Mock-only behavior (`fail=True`) stays out of the contract tests
     - Later: a `"real"` entry in the `camera` fixture on the Pi (marked `@pytest.mark.hardware`)
   - Done (mock side): the `assemble_hal(real=False)` assembler in `hal/assembler.py`, built test-first one device at a time. It returns a `Hal` object holding `speaker`, `camera`, `legs`, `battery` and `distance` (all mocks). `Hal` has no default arguments, so it cannot be built with a part missing. One parametrized test checks that each device is the right mock class
     - Later: the `real=True` branch on the Pi. When real devices exist, change the test to check against the interfaces (`Speaker`, `Camera`, `Legs`, `Battery`, `Distance`) so it covers both mock and real
   - Next: the `Microphone` interface and mock
   - Planned: `Microphone` (USB mic, bought) and `Display` (DSI screen ordered). Not in the layer 1 list until they are built
   - Pending on the Pi: `RealDistance` and `RealBattery` (add a `"real"` entry to each contract fixture, mark `@pytest.mark.hardware`)
3. Safety and executor
4. Skills catalog
5. Tool registry
6. Agent and behaviors
7. Dev workflow (Mac -> Pi sync/deploy, testing)
