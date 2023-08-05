import re
from typing import Iterator

from helpers.constants import JSON, BOOL_TYPE, TYPE_MAPPING, JSON_TYPE, PRIMITIVE_TYPES
from helpers.functions import get_items, get_key, to_number, create_object, type_from_str


class JSONSerializer:
    def dumps(self, obj) -> str:
        if type(obj) == str:
            return f'"{obj}"'
        if type(obj) in (int, float, complex):
            return str(obj)
        if type(obj) in [bool, type(None)]:
            return BOOL_TYPE[obj]

        return JSON.format(
            type=type(obj) if type(obj) in TYPE_MAPPING.values() else object,
            id=id(obj),
            items=self.__load_to_json(get_items(obj))
        )

    def loads(self, json: str):
        if not len(json):
            return

        if json == ' ':
            return ...
        if json.startswith('"'):
            return json.strip('"')
        if json in BOOL_TYPE.values():
            return get_key(json, BOOL_TYPE)
        if to_number(json) is not None:
            return to_number(json)

        return create_object(
            type_from_str(json, JSON_TYPE),
            self.__load_from_json(json)
        )

    def __load_to_json(self, obj: dict) -> str:
        json_format = ""

        for k, v in obj.items():
            if type(v) in PRIMITIVE_TYPES:
                json_format += f"\t{self.dumps(k)}: {self.dumps(v)},\n"
                continue

            json_format += f"\t{self.dumps(k)}: {{\n"

            for line in self.dumps(v).split("\n")[1:]:
                json_format += f"\t{line}\n"

        return json_format

    def __load_from_json(self, template: str) -> dict:
        obj: dict = {}
        lines: list[str] = template.split("\n")
        it: Iterator[str] = enumerate(lines)

        for i, line in it:
            if not re.search(r'\s*(.+):\s*([^,]*)', line):
                continue

            key, value = re.search(r'\s*(.+):\s*([^,]*)', line).groups()

            if value != "{":
                obj[self.loads(key)] = self.loads(value)

            elif value == "{" and "<class" not in key:
                brackets = 1
                start = i + 1

                while brackets and i < len(lines) - 1:
                    i, line = next(it, None)
                    brackets += ("{" in lines[i]) - ("}" in lines[i])

                obj[self.loads(key)] = self.loads('\n'.join(lines[start:i]))

        return obj
