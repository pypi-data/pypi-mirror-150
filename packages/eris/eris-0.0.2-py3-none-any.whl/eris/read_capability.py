# SPDX-FileCopyrightText: 2022 pukkamustard <pukkamustard@posteo.net>
#
# SPDX-License-Identifier: LGPL-3.0-or-later

import base64


def _b32encode(b):
    return base64.b32encode(b).decode().rstrip("=")


class ERISReadCapability:
    def _of_string(urn):
        pring("should be doing something...")

    def __repr__(self):
        return "<ERISReadCapability block_size:{} level:{}, root_ref:{}, root_key: {}>".format(
            self.block_size,
            self.level,
            self.root_ref,
            self.root_key,
        )

    def __bytes__(self):

        block_size_byte = 0x00

        if self.block_size == 1024:
            block_size_byte = bytes([0x0A])
        elif self.block_size == 32768:
            block_size_byte = bytes([0x0F])

        return block_size_byte + bytes([self.level]) + self.root_ref + self.root_key

    def __str__(self):
        read_cap = _b32encode(bytes(self))
        return "urn:erisx3:" + read_cap

    def __init__(self, *args, **kwargs):
        if len(args) == 1 and isinstance(args[0], str):
            of_string(args[0])
        elif len(args) == 1 and isinstance(args[0], bytes):
            of_bytes(args[0])
        elif len(args) == 4:
            if args[0] != 1024 and args[0] != 32768:
                raise ValueError("invalid block size")
            self.block_size = args[0]
            self.level = args[1]
            self.root_ref = args[2]
            self.root_key = args[3]
