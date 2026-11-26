# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added

- `openai/speech-voices.json`: the thirteen voices of OpenAI's text-to-speech call; `ballad`, `verse`, `marin` and `cedar` work
  with `gpt-4o-mini-tts` only, the other nine with every model of the call.
- `schemas/speech-voices.schema.json`, and `tools/check.py`, which validates every data file against its schema and fails on an
  unknown field, a missing `source` or a duplicate id.
- The `Check` workflow, started by hand.
