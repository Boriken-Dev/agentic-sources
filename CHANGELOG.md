# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added

- `tools/check.py`, which validates every data file against its schema and fails on an unknown field, a missing `source` or a
  duplicate id; with no data file it passes.
- The `Check` workflow, started by hand.

### Removed

- `openai/speech-voices.json` and `schemas/speech-voices.schema.json`: OpenAI publishes the voices and the end dates of its speech
  models in its API description, and its models by `GET /v1/models`, so they are read there. The repository holds only lists
  nobody publishes.
