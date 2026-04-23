# Scenario Modes

Each `<mode>.txt` in this folder is an extra prompt snippet that gets
appended to the synthesiser's prompt when the pipeline is run with that
mode.

## How it works

```
python pipeline.py <doc_key> <system_key> [<mode>]
```

If `<mode>` is supplied, `main/modes/<mode>.txt` is loaded and merged
into the synthesiser prompt **after** the document requirements, under
a `SCENARIO INSTRUCTIONS` header. Without a mode, the pipeline behaves
exactly as before.

## Available modes

| Mode | Purpose |
|---|---|
| `date_mismatch` | Deliberately generate Protocol dates that don't match the contract's `maintenance_frequency` (two per interval, or a missing interval) |
| `device_type_mismatch` | Deliberately make `device_type` disagree across Device / Contract / Protocol |

## Adding a new mode

1. Create `main/modes/<your_mode>.txt`.
2. Write the scenario instructions in plain English. Be concrete — give
   example values and date patterns.
3. Run `python pipeline.py <doc_key> <system_key> <your_mode>`.
