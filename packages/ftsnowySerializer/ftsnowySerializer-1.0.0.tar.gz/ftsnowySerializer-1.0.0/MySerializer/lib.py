import argparse

from base import Serializer
from serialize import JSONSerializer, XMLSerializer


def main():
    parser = argparse.ArgumentParser(prog="xjst")
    parser.add_argument('file_from')
    parser.add_argument('file_to')
    parser.add_argument('format_from')
    parser.add_argument('format_to')

    args = parser.parse_args()
    file_from, file_to, format_from, format_to = (
        args.file_from,
        args.file_to,
        args.format_from,
        args.format_to
    )

    format_mapping: dict[str, Serializer] = {
        'json': JSONSerializer(),
        'xml': XMLSerializer()
    }

    with open(file_from, 'r') as ff, open(file_to, 'w+') as ft:
        ser_from: Serializer = format_mapping[format_from]
        ser_to: Serializer = format_mapping[format_to]

        ser_to.dump(ser_from.load(ff), ft)


if __name__ == '__main__':
    main()
