"""Visualize binary data using Braille characters.

A Braille cell's dots are numbered:

    1 4
    2 5
    3 6
    7 8

These numbers correspond with the low byte of the Unicode code point for
the cell, if the bits are numbered 87654321.

To visually represent a byte of arbitrary data, we want the dots to
correspond with different bits:

    8 4
    7 3
    6 2
    5 1

We can accomplish this by rearranging the bits from 87654321 to
15234678, and then looking up the corresponding Braille cell.

    1 4   →   8 4
    2 5   →   7 3
    3 6   →   6 2
    7 8   →   5 1

      8765 4321
      ↓↓↓↓ ↓↓↓↓
      1523 4678

"""

BRAILLE_START_POINT = 0x2800


def shuffle(byte):
    return (
        # ____ ___1
        # 1___ ____
        ((byte & 0b00000001) << 7) |
        # ____ __2_
        # __2_ ____
        ((byte & 0b00000010) << 4) |
        # ___5 _3__
        # _5_3 ____
        ((byte & 0b00010100) << 2) |
        # __6_ ____
        # ____ _6__
        ((byte & 0b00100000) >> 3) |
        # _7__ ____
        # ____ __7_
        ((byte & 0b01000000) >> 5) |
        # 8___ ____
        # ____ ___8
        ((byte & 0b10000000) >> 7) |
        # ____ 4___
        # <no change>
        ((byte & 0b00001000))
    )


def unshuffle(byte):
    return (
        # X___ ____
        # ____ ___X
        ((byte & 0b10000000) >> 7) |
        # __X_ ____
        # ____ __X_
        ((byte & 0b00100000) >> 4) |
        # _X_X ____
        # ___X _X__
        ((byte & 0b01010000) >> 2) |
        # ____ _X__
        # __X_ ____
        ((byte & 0b00000100) << 3) |
        # ____ __X_
        # _X__ ____
        ((byte & 0b00000010) << 5) |
        # ____ ___X
        # X___ ____
        ((byte & 0b00000001) << 7) |
        # ____ X___
        # <no change>
        ((byte & 0b00001000))
    )


def brailleify(data):
    """
    >>> brailleify([0b10001000, 0b00010001, 0b11110000, 0b00001111])
    '⠉⣀⡇⢸'
    """
    return ''.join(chr(BRAILLE_START_POINT + shuffle(byte)) for byte in data)


def unbrailleify(braille):
    """
    >>> [bin(byte) for byte in unbrailleify('⠉⣀⡇⢸')]
    ['0b10001000', '0b10001', '0b11110000', '0b1111']
    """
    return bytes(unshuffle(ord(c) - BRAILLE_START_POINT) for c in braille)
