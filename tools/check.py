"""Validate every data file against its schema, with the standard library only.

Usage: python tools/check.py [ROOT]

A data file is any `<publisher>/<list>.json`. Its schema is `schemas/<list>.schema.json`; a file with no
schema fails. The validator implements the keywords the schemas use: type, required, properties,
additionalProperties, items, minItems, minLength, pattern, enum. A keyword outside that set fails, so a
schema never silently checks less than it says. Entries named `id` are unique within their array.
"""

import json
import re
import sys
from pathlib import Path

ANNOTATIONS = {"$schema", "title", "description"}
KEYWORDS = ANNOTATIONS | {
    "type",
    "required",
    "properties",
    "additionalProperties",
    "items",
    "minItems",
    "minLength",
    "pattern",
    "enum",
}
TYPES = {
    "object": dict,
    "array": list,
    "string": str,
    "boolean": bool,
    "number": (int, float),
    "integer": int,
    "null": type(None),
}


def validate(value, schema, path, errors):
    for key in schema:
        if key not in KEYWORDS:
            errors.append(f"{path}: schema keyword {key!r} is not supported by check.py")
    kind = schema.get("type")
    if kind:
        ok = isinstance(value, TYPES[kind])
        if kind in ("integer", "number") and isinstance(value, bool):
            ok = False
        if not ok:
            errors.append(f"{path}: expected {kind}, found {type(value).__name__}")
            return
    if "enum" in schema and value not in schema["enum"]:
        errors.append(f"{path}: {value!r} is not one of {schema['enum']}")
    if isinstance(value, str):
        if len(value) < schema.get("minLength", 0):
            errors.append(f"{path}: shorter than {schema['minLength']}")
        if "pattern" in schema and not re.search(schema["pattern"], value):
            errors.append(f"{path}: {value!r} does not match {schema['pattern']}")
    if isinstance(value, list):
        if len(value) < schema.get("minItems", 0):
            errors.append(f"{path}: fewer than {schema['minItems']} items")
        if "items" in schema:
            for i, item in enumerate(value):
                validate(item, schema["items"], f"{path}[{i}]", errors)
        ids = [i["id"] for i in value if isinstance(i, dict) and isinstance(i.get("id"), str)]
        for dup in sorted({i for i in ids if ids.count(i) > 1}):
            errors.append(f"{path}: id {dup!r} appears more than once")
    if isinstance(value, dict):
        props = schema.get("properties", {})
        for name in schema.get("required", []):
            if name not in value:
                errors.append(f"{path}: missing required field {name!r}")
        for name, item in value.items():
            if name in props:
                validate(item, props[name], f"{path}.{name}", errors)
            elif schema.get("additionalProperties", True) is False:
                errors.append(f"{path}: unknown field {name!r}")


def check(root):
    errors = []
    files = sorted(
        p
        for p in root.glob("*/*.json")
        if p.parent.name != "schemas" and not p.parent.name.startswith(".")
    )
    for file in files:
        name = file.relative_to(root).as_posix()
        schema_file = root / "schemas" / f"{file.stem}.schema.json"
        if not schema_file.is_file():
            errors.append(f"{name}: no schema schemas/{file.stem}.schema.json")
            continue
        try:
            data = json.loads(file.read_text(encoding="utf-8"))
            schema = json.loads(schema_file.read_text(encoding="utf-8"))
        except (OSError, ValueError) as err:
            errors.append(f"{name}: {err}")
            continue
        found = []
        validate(data, schema, "$", found)
        errors.extend(f"{name}: {e}" for e in found)
    return files, errors


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent)
    files, errors = check(root)
    for error in errors:
        print(f"FAIL {error}")
    if errors:
        return 1
    print(f"PASS {len(files)} data file(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
