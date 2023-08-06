import argparse
from typing import Any

from ..serializers.jsonserializer import JSONSerializer
from ..serializers.xmlserializer import XMLSerializer


def main():
    parser = argparse.ArgumentParser()
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

    format_mapping: dict[str, Any] = {
        'json': JSONSerializer(),
        'xml': XMLSerializer()
    }

    with open(file_from, 'r') as ff, open(file_to, 'w+') as ft:
        format_from = format_mapping[format_from]
        format_to = format_mapping[format_to]

        format_to.dump(format_from.load(ff), ft)


if __name__ == "__main__":
    main()
    