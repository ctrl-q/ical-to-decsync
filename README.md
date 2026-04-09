# ical-to-decsync

Sync an iCal/ICS calendar file into a [DecSync CC](https://github.com/39aldo39/DecSync) directory, so it can be picked up by calendar apps that support DecSync (e.g. Etar, DAVx⁵ with DecSync).

## Requirements

- Python 3.8+
- `libdecsync` (native library for DecSync)

Install Python dependencies:

```bash
pip install -r requirements.txt
```

## Usage

```bash
python main.py <ics_file> \
  --decsync-cc-dir <path_to_decsync_dir> \
  --decsync-collection <calendar_name> \
  --decsync-cc-app-id <app_id> \
  [--default-alarm-minutes <minutes>]
```

**Arguments:**

| Argument | Default | Description |
|---|---|---|
| `ics_file` | — | Path to the `.ics` file to import |
| `--decsync-cc-dir` | — | Path to the DecSync CC directory |
| `--decsync-collection` | — | Name of the target calendar collection |
| `--decsync-cc-app-id` | — | App ID to identify this sync client |
| `--default-alarm-minutes` | `15` | Default reminder added to events without an alarm |
