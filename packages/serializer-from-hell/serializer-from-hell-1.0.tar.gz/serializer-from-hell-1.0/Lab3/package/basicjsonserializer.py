from constants.formats import JSON, JSON_TYPE
from constants.constants import BOOL_TYPES, PRIMITIVES, TYPE_MAPPING
from funcs.funcs import get_key, to_number, get_items, type_from_str, create_object
import re
from typing import Iterator


class JSONSerializer:

    def dumps(self, obj):
        if type(obj) == str:
            return f'"{obj}"'

        if type(obj) in (int, float, complex):
            return str(obj)

        if type(obj) in [bool, type(None)]:
            return BOOL_TYPES[obj]

        return JSON.format(
            type=type(obj) if type(obj) in TYPE_MAPPING.values() else object,
            id=id(obj),
            items=self.__load_to_json(get_items(obj))
        )

    def loads(self, load_from: str):
        if not len(load_from):
            return

        if load_from == ' ':
            return ...
        if load_from.startswith('"'):
            return load_from.strip('"')
        if load_from in BOOL_TYPES.values():
            return get_key(load_from, BOOL_TYPES)
        if to_number(load_from) is not None:
            return to_number(load_from)
        return create_object(
            type_from_str(load_from, JSON_TYPE),
            self.__load_from_json(load_from)
        )


    def __load_to_json(self, obj: dict):
        json_format = ""

        for k, v in obj.items():
            if type(v) in PRIMITIVES:

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

    def dump(self, obj, file_to):
        file_to.write(self.dumps(obj))

    def load(self, file_from):
        return self.loads(file_from.read())

