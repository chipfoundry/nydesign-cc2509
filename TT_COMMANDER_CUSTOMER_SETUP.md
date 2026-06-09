# TT Commander Customer Setup (RP2040, SDK v2.0.4)

This runbook documents how to ship CC2509 boards that work with Tiny Tapeout Commander when using MicroPython SDK `v2.0.4`.

## Scope

- Demoboard: TT04 style board with RP2040
- Firmware: Tiny Tapeout MicroPython SDK `v2.0.4`
- Shuttle detected from ROM: `ttsky25b`
- Commander flow: `select_design(...)` from the web app

## Why this setup is required

Commander injects `ttcontrol.py`, and `select_design(...)` calls:

- `tt.shuttle[design].enable()`

That path requires a local shuttle index file on the RP2040 filesystem:

- `/shuttles/ttsky25b.json`

On SDK `v2.0.4`, each project entry in that JSON must include `clock_hz`. If missing, boot can fail with:

- `KeyError: clock_hz`

## Required files on RP2040

At minimum, board flash must contain:

- `main.py`
- `config.ini`
- `/shuttles/ttsky25b.json`

Notes:

- `tt-commander-app` files are not stored on the board.
- Commander sends `ttcontrol.py` each session over serial.

## Prepare a v2.0.4-compatible shuttle index

Starting from repo file:

- `shuttle_index.json`

Generate a compatible file that ensures `clock_hz` exists for every project:

```bash
python3 - <<'PY'
import json
src = "shuttle_index.json"
dst = "ttsky25b_for_sdk204.json"

with open(src) as f:
    data = json.load(f)

for p in data.get("projects", []):
    p.setdefault("clock_hz", 0)
    p.setdefault("danger_level", "safe")

with open(dst, "w") as f:
    json.dump(data, f)

print("wrote", dst)
PY
```

## Provision the board

Use explicit serial port (example shown below):

```bash
mpremote connect "/dev/cu.usbmodem3101" fs mkdir :/shuttles
mpremote connect "/dev/cu.usbmodem3101" fs cp "ttsky25b_for_sdk204.json" :/shuttles/ttsky25b.json
mpremote connect "/dev/cu.usbmodem3101" fs ls :/shuttles
mpremote connect "/dev/cu.usbmodem3101" reset
```

If `mkdir` reports it already exists, continue.

### Windows one-step script

Use the PowerShell script in this repo to flash UF2 and copy the shuttle index:

```powershell
.\provision_board_windows.ps1
```

Optional parameters:

```powershell
.\provision_board_windows.ps1 -Port COM5
.\provision_board_windows.ps1 -SkipFlash
.\provision_board_windows.ps1 -SkipFactoryCheck
.\provision_board_windows.ps1 -IndexJson .\my_index.json -ShuttleId ci2511
```

By default, the script also runs a final factory counter check (address `1`, `sel=1`) and asserts the counter increments by 1 across two clock pulses.

## Verify provisioning

### 1) Verify file persistence

```bash
mpremote connect "/dev/cu.usbmodem3101" exec "import os; print(os.listdir('/shuttles'))"
```

Expected: includes `ttsky25b.json`.

### 2) Verify board boots and loads shuttle index

```bash
mpremote connect "/dev/cu.usbmodem3101" exec "from ttboard.demoboard import DemoBoard; tt=DemoBoard.get(); print(tt.shuttle.run)"
```

Expected boot logs include:

- `Loading shuttle file /shuttles/ttsky25b.json`
- no `KeyError: clock_hz`
- final printed run: `ttsky25b`

### 3) Verify Commander selection path

In Commander REPL:

```python
select_design(1, 0)
dump_state()
```

Expected: no shuttle index error; design selection works.

### 4) Verify in tt-commander-app UI

1. Open your deployed Commander URL and click **Connect to Board**.
2. Confirm the **Project** dropdown shows the expected project titles for this shuttle.
3. Select address `1` (Factory Test), click **Select**, and verify no error appears in logs.
4. Confirm **Repo** opens the expected project repository page.
5. Optional smoke check:
   - set `rst_n=0`, set `ui_in=0xA5`, verify `uo_out=0xA5` (factory mirror mode).

## Factory test quick sanity (optional)

After selecting address `1` (factory test), verify:

- Mode 1: `rst_n=0` mirrors `ui_in` to `uo_out`
- Mode 2: `rst_n=1`, `sel=0` mirrors `uio_in` to `uo_out`
- Mode 3: `rst_n=1`, `sel=1` counter increments with manual clock

## Known issues and fixes

- `Could not open shuttle index /shuttles/ttsky25b.json`
  - File missing or wrong filename. Ensure exact path and shuttle ID match.

- `KeyError: clock_hz`
  - JSON schema mismatch for SDK `v2.0.4`. Regenerate with `clock_hz` for each project.

- `mpremote connect list` does not show `/dev/cu.usbmodem*`
  - Cable/USB path issue or board not enumerated.

- `mpremote` hangs
  - Another app may hold the port (Commander/Thonny/serial terminal). Close other tools and use explicit port.

## Customer release checklist

- [ ] Board flashed with known-good SDK `v2.0.4` UF2
- [ ] `/shuttles/ttsky25b.json` copied and persisted
- [ ] Boot check passes with no JSON schema error
- [ ] Commander `select_design(...)` works on at least addresses `0`, `1`, and one student project
- [ ] Factory test smoke check passes
