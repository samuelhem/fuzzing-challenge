import re


def int_to_hex_tuple(int_val):
    from_hex = hex(int_val)[2:]
    # fill up odd hex with leading 0
    if len(from_hex) % 2 == 1:
        from_hex = "0" + from_hex
    hex_ar = re.findall('..', from_hex)
    assembled = ""
    for hex_val in hex_ar:
        assembled += "\\x" + hex_val
    return assembled
