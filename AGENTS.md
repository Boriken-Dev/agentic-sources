# agentic-sources: repository orientation

JSON lists a catalog needs when a publisher has no API that lists them (voice names, model names, ...). Consumers read a file at
`main` or a pinned commit; nothing is built or packaged.

## Layout

| Path | Responsibility |
| --- | --- |
| `<publisher>/<list>.json` | One list: its entries plus `source` (the publisher's documentation page) and `checked` (date compared) |
| `schemas/<list>.schema.json` | The schema of that list's format; same list name as the data file |
| `tools/check.py` | Validates every data file against its schema; standard library only |
| `.github/workflows/check.yml` | Runs `tools/check.py`; started by hand only |

## Rules

- Every list file has a schema of the same list name, with `additionalProperties: false`; a file without one fails the check.
- Every file cites its source and the date it was last compared; an entry the publisher does not document is not added.
- A change is checked against the publisher's page, then `checked` is set to the date.
- Public text only: no private paths, hostnames, credentials or plan names. No executables, archives, keys or opaque binaries.
- LF line endings everywhere (`.gitattributes`).
- No tag without the owner's say-so.

## Commands

```sh
python tools/check.py          # PASS, or one FAIL line per problem; exit 1 on any
```
