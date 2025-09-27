from __future__ import annotations

def ensure_semicolon(value: str) -> str:
    if value is None:
        return ""
    s = str(value).rstrip()
    if not s:
        return s
    if s.endswith(";") or s.endswith("}"):
        return s
    return s + ";"


def normalize_actions(values):
    if not values:
        return []
    return [ensure_semicolon(v) for v in values]


class FilterModule(object):
    def filters(self):
        return {
            'ensure_semicolon': ensure_semicolon,
            'normalize_actions': normalize_actions,
        }

