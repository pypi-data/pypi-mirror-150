# SPDX-FileCopyrightText: 2022 pukkamustard <pukkamustard@posteo.net>
#
# SPDX-License-Identifier: LGPL-3.0-or-later

from Crypto.Hash import BLAKE2b
from Crypto.Cipher import ChaCha20 as ChaCha20_IETF

from . import read_capability


def Blake2b_256_keyed(input, convergence_secret):
    h_obj = BLAKE2b.new(digest_bits=256, key=convergence_secret)
    h_obj.update(input)
    return h_obj.digest()


def Blake2b_256(input):
    h_obj = BLAKE2b.new(digest_bits=256)
    h_obj.update(input)
    return h_obj.digest()


def ChaCha20(input, key, nonce):
    cipher = ChaCha20_IETF.new(key=key, nonce=nonce)
    return cipher.encrypt(input)


class ERISEncoder:
    def __init__(self, block_size=32768, convergence_secret=bytes(32)):
        assert block_size == 1024 or block_size == 32768
        self.block_size = block_size

        assert len(convergence_secret) == 32
        self.convergence_secret = convergence_secret

        # init levels
        self.levels = []

        # init buffer
        self.buffer = b""

    def _buffer_leaf_nodes(self):
        while len(self.buffer) >= self.block_size:
            yield self.buffer[: self.block_size]
            self.buffer = self.buffer[self.block_size :]

    def _buffer_pad(self):
        # buffer is smaller than block_size
        assert len(self.buffer) < self.block_size

        # pad what remains in the buffer
        required_padding = self.block_size - len(self.buffer) - 1
        self.buffer += bytes([0x80]) + bytes(required_padding)

    def _encrypt_leaf_node(self, node):
        key = Blake2b_256_keyed(node, self.convergence_secret)
        nonce = bytearray(12)
        block = ChaCha20(node, key, nonce)
        ref = Blake2b_256(block)
        return block, ref, key

    def _encrypt_internal_node(self, node, tree_level):
        key = Blake2b_256(node)
        nonce = bytearray(12)
        nonce[11] = tree_level
        block = ChaCha20(node, key, nonce)
        ref = Blake2b_256(block)
        return block, ref, key

    # adds reference key pair to a level
    def _add_ref_key_to_levels(self, level, ref, key):
        # ensure that level exists
        if len(self.levels) < level + 1:
            self.levels.append(b"")

        # levels exist at least up to current level
        assert len(self.levels) >= level + 1

        # append reference-key pair to current level
        self.levels[level] += ref + key

        # a level is never larger than the block size
        assert len(self.levels[level]) <= self.block_size

    def _force_collect(self, level):
        node = self.levels[level]

        # add padding to make node exaclty of size block_size
        required_padding = self.block_size - len(node)
        node += bytes(required_padding)

        # node has exactly size block_size
        assert len(node) == self.block_size

        # clear the level
        self.levels[level] = b""

        # return the encrypted block
        return self._encrypt_internal_node(node, level + 1)

    # attempt to collect levels starting at the given level
    def _collect(self, start_level):

        # iterator for level we are currently processing
        level = start_level

        while level < len(self.levels):
            # if level is full block size
            if len(self.levels[level]) == self.block_size:
                # then collect the level to an encrypted node (a block)
                block, ref, key = self._force_collect(level)
                # yield the reference, block
                yield block
                # add the reference-key pair to the next level
                self._add_ref_key_to_levels(level + 1, ref, key)
                # continue processing next level
                level += 1
            else:
                # stop continuing to next level
                break

    def _encode_buffer(self):
        # iterate over leaf nodes that are ready in buffer
        for leaf_node in self._buffer_leaf_nodes():

            # encrypt node to block
            block, ref, key = self._encrypt_leaf_node(leaf_node)

            # yield the reference to the encrypted block and block itself
            yield block

            # add reference-key pair to levels and yield nodes
            self._add_ref_key_to_levels(0, ref, key)

            # recursively attempt to collect all reference-key pairs to encrypted nodes
            yield from self._collect(0)

    def update_generate_blocks(self, data):
        self.buffer += data
        return self._encode_buffer()

    def update(self, data):
        # consume and forget about blocks
        all(self.update_generate_blocks(data))

    def finalize_generate_blocks(self):
        self._buffer_pad()
        yield from self._encode_buffer()

        # prevent the buffer from being used
        del self.buffer

        level = 0

        while level < len(self.levels):
            # if we are at top level and there is only a single reference-key pair
            if len(self.levels) == level + 1 and len(self.levels[level]) == 64:
                # then we are at the root reference-key pair

                # extract reference-key pair
                ref = self.levels[level][:32]
                key = self.levels[level][32:]

                # encode and yield the read capability
                self.read_capability = read_capability.ERISReadCapability(
                    self.block_size, level, ref, key
                )

                # break the loop
                break

            elif len(self.levels[level]) > 0:
                # then collect the level and encrypt to block
                block, ref, key = self._force_collect(level)
                # yield the reference, block
                yield (ref, block)
                # add the reference-key pair to the next level
                self._add_ref_key_to_levels(level + 1, ref, key)
                # and continue at the next level
                level += 1

            else:
                # this level is empty, continue finalizing at next
                level += 1

    def digest(self):
        # consume and forget about blocks
        all(self.finalize_generate_blocks())

        return self.read_capability
