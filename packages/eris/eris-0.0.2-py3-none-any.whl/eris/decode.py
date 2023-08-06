# SPDX-FileCopyrightText: 2022 pukkamustard <pukkamustard@posteo.net>
#
# SPDX-License-Identifier: LGPL-3.0-or-later

from io import BufferedReader


class ERISBufferedReader(BufferedReader):
    def __init__(self, read_capability):
        print(read_capability)
