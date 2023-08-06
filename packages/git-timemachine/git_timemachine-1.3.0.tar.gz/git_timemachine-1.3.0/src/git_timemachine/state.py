import json
from os import PathLike, path
from typing import Any
from datetime import datetime


class StateFile:
    raw: dict = {}
    filename: PathLike

    def __init__(self, filename: PathLike):
        self.filename = filename

        if path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as fp:
                self.raw = json.load(fp)

    def get(self, key: str, default=None) -> Any:
        if key not in self.raw:
            return default

        value = self.raw[key]

        if isinstance(value, dict) and 'type' in value:
            if value['type'] == 'datetime':
                return datetime.fromisoformat(value['value'])

        return self.raw[key]

    def set(self, key: str, value: Any):
        if isinstance(value, datetime):
            self.raw[key] = {
                'type': 'datetime',
                'value': value.replace(microsecond=0).astimezone().isoformat()
            }
        else:
            self.raw[key] = value

        with open(self.filename, 'w', encoding='utf-8') as fp:
            json.dump(self.raw, fp, ensure_ascii=False, indent=4)
