# python-eris

This is a Python implementation of the [Encoding for Robust Immutable Storage (ERIS)](http://purl.org/eris).

# Usage

## Computing an ERIS URN

```
from eris import ERISEncoder

encoder = ERISEncoder(block_size = 1024)

encoder.update(b'Hello world!')

read_capability = encoder.digest()

print(read_capability)
```

Will print `urn:erisx2:BIAD77QDJMFAKZYH2DXBUZYAP3MXZ3DJZVFYQ5DFWC6T65WSFCU5S2IT4YZGJ7AC4SYQMP2DM2ANS2ZTCP3DJJIRV733CRAAHOSWIYZM3M`.

This uses the [`hashlib`](https://docs.python.org/3/library/hashlib.html) interface of `ERISEncoder`.

The `update` method can be called multiple times:

```
from eris import ERISEncoder

encoder = ERISEncoder(block_size = 1024)

encoder.update(b'Hello ')
encoder.update(b'world!')

read_capability = encoder.digest()

print(read_capability)
```

Note that the object returned by the `digest` method is a `ERISReadCapability`. It can be converted to a string URN representation or to a binary encoding (see [Binary Encoding of Read Capability](http://purl.org/eris#name-binary-encoding-of-read-cap)):

```
>>> read_capability
<ERISReadCapability block_size:1024 level:0, root_ref:b'?\xfe\x03K\n\x05g\x07\xd0\xee\x1ag\x00~\xd9|\xeci\xcdK\x88te\xb0\xbd?v\xd2(\xa9\xd9i', root_key: b'\x13\xe62d\xfc\x02\xe4\xb1\x06?Cf\x80\xd9k3\x13\xf64\xa5\x11\xaf\xf7\xb1D\x00;\xa5dc,\xdb'>

>>> str(read_capability)
'urn:erisx3:BIAD77QDJMFAKZYH2DXBUZYAP3MXZ3DJZVFYQ5DFWC6T65WSFCU5S2IT4YZGJ7AC4SYQMP2DM2ANS2ZTCP3DJJIRV733CRAAHOSWIYZM3M'

>>> bytes(read_capability)
b'\n\x00?\xfe\x03K\n\x05g\x07\xd0\xee\x1ag\x00~\xd9|\xeci\xcdK\x88te\xb0\xbd?v\xd2(\xa9\xd9i\x13\xe62d\xfc\x02\xe4\xb1\x06?Cf\x80\xd9k3\x13\xf64\xa5\x11\xaf\xf7\xb1D\x00;\xa5dc,\xdb'
```

## Encoding to Blocks

```
from eris import ERISEncoder

encoder = ERISEncoder(block_size = 1024)

for block in encoder.update_generate_blocks(b'Hello world!')
    do_something_with_block(block)

for block in encoder.finalize():
    do_something_with_block(block)

read_capability = encoder.read_capability()

print(read_capability)
```

## Decoding

TODO: not yet implemented

# Development

## Publishing to PyPi

```
python -m build
python3 -m twine upload --repository pypi dist/*
```

# License

[LGPL-3.0-or-later](./LICENSE/LGPL-3.0-or-later)
