import re
from typing import Iterator
from constants.constants import PRIMITIVES, TYPE_MAPPING
from constants.formats import XML, XML_TYPE, XML_ITEM, XML_PRIMITIVE
from funcs.funcs import get_key, get_items, type_from_str, create_object

class XMLSerializer:

    def dumps(self, obj) -> str:
        if type(obj) in PRIMITIVES:
            obj_type = get_key(type(obj), TYPE_MAPPING)
            return f'<primitive type="{obj_type}">{obj}</primitive>'

        return XML.format(
            type=get_key(type(obj), TYPE_MAPPING) if type(obj) in TYPE_MAPPING.values() else "object",
            id=id(obj),
            items=self.__load_to_xml(get_items(obj))
        )

    def loads(self, xml):
        if not len(xml):
            return

        if "primitive" in xml.split("\n")[0]:
            obj_data = re.search(
                XML_PRIMITIVE.format(
                    type="\w+",
                    obj="(.*)"
                ), xml).group(1)
            obj_type = type_from_str(
                s=xml.split("\n")[0],
                pattern=XML_TYPE
            )

            if obj_type == type(None):
                return None

            if obj_type == bool:
                return obj_data == "True"

            if obj_type == type(Ellipsis):
                return ...

            return obj_type(obj_data)

        return create_object(
            type_from_str(xml, XML_TYPE),
            self.__load_from_xml(xml)
        )

    def __load_to_xml(self, obj: dict) -> str:
        xml_format = ""

        for k, v in obj.items():
            xml_format += f"\t{XML_ITEM.format(key=self.dumps(k), value=self.dumps(v))}"
        return xml_format

    def __load_from_xml(self, template: str) -> dict:
        obj: dict = {}
        lines: list[str] = template.split("\n")
        it: Iterator[str] = enumerate(lines)

        for i, line in it:
            if "<item>" == line.strip("\t\n "):
                item = self.__get_tag("item", lines[i + 1:])
                key = self.__get_tag("key", item[1:])
                value = self.__get_tag("value", item[len(key) + 2:])

                obj[self.loads("\n".join(key[:-1]))] = self.loads("\n".join(value[:-1]))

                [next(it, None) for _ in range(len(item))]

        return obj

    def __get_tag(self, tagname: str, lines) -> str:
        counter = 1
        it = enumerate(lines)

        for i, line in it:
            if not counter:
                return lines[:i]

            counter += bool(re.search(rf"<{tagname}.*>", line.strip("\t\n ")))
            counter -= bool(re.search(rf"</{tagname}>", line.strip("\t\n ")))

    def dump(self, obj, file_to):
        file_to.write(self.dumps(obj))

    def load(self, file_from):
        return self.loads(file_from.read())