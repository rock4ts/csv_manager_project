import ast
import csv


def parse_bytes(row):
    """Converts string represented in Python byte-string literal b'' syntax
    into a decoded character string - otherwise return it unchanged.
    """
    result = row
    try:
        result = ast.literal_eval(row)
    finally:
        return result.decode() if isinstance(result, bytes) else result


def parse_file_bytes(file_obj):
    """Parses file object containing Python byte-string literal b'' syntax
    into a decoded iterable of strings.
    """
    for row in file_obj:
        yield parse_bytes(row)


def find_delimiter(file_obj):
    """Determines csv-file delimiter by evaluating its content.
    """
    sniffer = csv.Sniffer()
    delimiter = sniffer.sniff(file_obj.read(5000).decode()).delimiter
    file_obj.seek(0)
    return delimiter
