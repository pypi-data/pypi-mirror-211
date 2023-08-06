import argparse
from ..package.basicjsonserializer import JSONSerializer
from ..package.basicxmlserializer import XMLSerializer


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("read_from")
    parser.add_argument("write_to")
    parser.add_argument("format_from")
    parser.add_argument("format_to")

    args = parser.parse_args()

    read_from, write_to, format_from, format_to = args.read_from, args.write_to, \
        args.format_from, args.format_to

    with open(read_from, 'r') as file, \
            open(write_to, 'w+') as file_to:
        format_from: JSONSerializer | XMLSerializer = JSONSerializer() if format_from == "json" else XMLSerializer()
        format_to: JSONSerializer | XMLSerializer = JSONSerializer() if format_to == "json" else XMLSerializer()

        format_to.dump(format_from.load(file), file_to)


if __name__ == '__main__':
    main()
