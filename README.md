# agentic-sources

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/Boriken-Dev/agentic-sources/blob/main/LICENSE)
[![CI](https://img.shields.io/github/actions/workflow/status/Boriken-Dev/agentic-sources/check.yml)](https://github.com/Boriken-Dev/agentic-sources/actions/workflows/check.yml)

**The lists a catalog needs when nobody publishes them**, as plain JSON, one file per publisher and list. A list that its
publisher gives in any form (an API, an OpenAPI description, a release feed) is read from there and has no file here: this
repository holds only what no publisher makes available. [Canoa](https://github.com/Boriken-Dev/canoa)'s extensions, and anything
else, read a file at a branch, a tag or a pinned commit, so a new name reaches every host without a new build of the software that
shows it. Every file names the documentation page it comes from and the date it was last compared with it.

## Features

- **Plain data**: JSON, no code to run; any language reads it.
- **A schema per list format** (`schemas/`), and a check that fails on an unknown field, a missing source or a duplicate id.
- **Cited**: each file's `source` is the publisher's own page, so a change is verified against it, never against memory.

## Reading a file

By raw URL, at a branch, a tag or a commit:

```text
https://raw.githubusercontent.com/Boriken-Dev/agentic-sources/main/<publisher>/<list>.json
https://raw.githubusercontent.com/Boriken-Dev/agentic-sources/<tag-or-commit>/<publisher>/<list>.json
```

Or with git, at a ref:

```bash
git clone --depth 1 https://github.com/Boriken-Dev/agentic-sources.git
git -C agentic-sources show main:<publisher>/<list>.json
```

Follow a branch to receive new entries as they land; pin a tag or a commit only when a consumer must not change under you. A
reader ignores a field it does not know and takes a missing optional field as "no information", so a file can gain fields without
breaking it.

## Layout

| Path | Holds |
| --- | --- |
| `<publisher>/<list>.json` | One list: the entries and where they come from |
| `schemas/<list>.schema.json` | The JSON Schema of a list format; a list's file and its schema share the list's name |
| `tools/check.py` | Validates every data file against its schema (standard library only) |

### Lists

None yet. OpenAI's speech voices and models, the first candidate, are not here: OpenAI publishes them in its API description
(`components.schemas.CreateSpeechRequest` of <https://github.com/openai/openai-openapi>) and by `GET /v1/models`, which Canoa reads
directly.

## Adding or changing an entry

1. Check that the publisher gives the list in no form a program can read (an API, a machine-readable description, a feed): if it
   does, read it there instead of adding a file.
2. Open the publisher's documentation page named by the file's `source` and compare it with the file.
3. Edit the entry or add it; set `checked` to today's date. A new publisher or list gets a `<publisher>/<list>.json` and a
   `schemas/<list>.schema.json` of the same list name, with `additionalProperties: false` and `source` required.
4. Run `python tools/check.py`; it prints `PASS` or one `FAIL` line per problem.
5. Add a line to `CHANGELOG.md` under `[Unreleased]` and commit with a `type: description` message.

Public text only: no private paths, hostnames or credentials, and no entry the publisher does not document.

## Development

```bash
python tools/check.py        # validate every data file
```

The `Check` workflow runs the same command and is started by hand.

## License

MIT, see [LICENSE](LICENSE).
