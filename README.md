# agentic-sources

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/Boriken-Dev/agentic-sources/blob/main/LICENSE)
[![CI](https://img.shields.io/github/actions/workflow/status/Boriken-Dev/agentic-sources/check.yml)](https://github.com/Boriken-Dev/agentic-sources/actions/workflows/check.yml)

**The lists a catalog needs when the publisher has no API that lists them**, as plain JSON, one file per publisher and list.
[Canoa](https://github.com/Boriken-Dev/canoa)'s extensions, and anything else, read a file at `main` or at a pinned commit, so a
new voice or model name reaches every host without a new build of the software that shows it. Every file names the
documentation page it comes from and the date it was last compared with it.

## Features

- **Plain data**: JSON, no code to run; any language reads it.
- **A schema per list format** (`schemas/`), and a check that fails on an unknown field, a missing source or a duplicate id.
- **Cited**: each file's `source` is the publisher's own page, so a change is verified against it, never against memory.

## Reading a file

By raw URL, at `main` or at a commit:

```text
https://raw.githubusercontent.com/Boriken-Dev/agentic-sources/main/openai/speech-voices.json
https://raw.githubusercontent.com/Boriken-Dev/agentic-sources/<commit>/openai/speech-voices.json
```

Or with git, at a ref:

```bash
git clone --depth 1 https://github.com/Boriken-Dev/agentic-sources.git
git -C agentic-sources show main:openai/speech-voices.json
```

Pin a commit when a consumer must not change under you; follow `main` to receive new entries as they land. A reader ignores a
field it does not know and takes a missing optional field as "no information", so a file can gain fields without breaking it.

## Layout

| Path | Holds |
| --- | --- |
| `<publisher>/<list>.json` | One list: the entries and where they come from |
| `schemas/<list>.schema.json` | The JSON Schema of a list format; a list's file and its schema share the list's name |
| `tools/check.py` | Validates every data file against its schema (standard library only) |

### Lists

| File | Holds | Format |
| --- | --- | --- |
| [`openai/speech-voices.json`](openai/speech-voices.json) | The voices of OpenAI's text-to-speech call, and the models the newer ones work with | [`speech-voices.schema.json`](schemas/speech-voices.schema.json) |

`speech-voices` entries: `id` (the name a request sends), optional `models` (the only models the voice works with; absent means
every model of the call), optional `languages` (BCP 47 tags) and optional `source` (a page for that voice). The file carries
`source` (a documentation page, `https://`), `checked` (`YYYY-MM-DD`) and `voices`.

## Adding or changing an entry

1. Open the publisher's documentation page named by the file's `source` and compare it with the file.
2. Edit the entry or add it; set `checked` to today's date. A new publisher or list gets a `<publisher>/<list>.json` and a
   `schemas/<list>.schema.json` of the same list name, with `additionalProperties: false` and `source` required.
3. Run `python tools/check.py`; it prints `PASS` or one `FAIL` line per problem.
4. Add a line to `CHANGELOG.md` under `[Unreleased]` and commit with a `type: description` message.

Public text only: no private paths, hostnames or credentials, and no entry the publisher does not document.

## Development

```bash
python tools/check.py        # validate every data file
```

The `Check` workflow runs the same command and is started by hand.

## License

MIT, see [LICENSE](LICENSE).
