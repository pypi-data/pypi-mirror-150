#!/usr/bin/env python3
# coding: utf-8

import base64
import hashlib
import mimetypes
import os
from os import PathLike
from typing import Generator, Union, Iterable

PATH = Union[str, PathLike]
FILE = Union[str, PathLike, Iterable[bytes]]


def read_as_chunks(path: PATH, length=-1, offset=0, chunksize=65536) \
        -> Generator[bytes, None, None]:
    if length == 0:
        return
    if length < 0:
        length = float('inf')
    chunksize = min(chunksize, length)
    with open(path, 'rb') as fin:
        fin.seek(offset)
        while chunksize:
            chunk = fin.read(chunksize)
            if not chunk:
                break
            yield chunk
            length -= chunksize
            chunksize = min(chunksize, length)


def compute_checksum(path_or_chunks: FILE, algo='sha1'):
    hashobj = hashlib.new(algo) if isinstance(algo, str) else algo
    # path_or_chunks:str - a path
    if isinstance(path_or_chunks, str):
        chunks = read_as_chunks(path_or_chunks)
    else:
        chunks = path_or_chunks
    for chunk in chunks:
        hashobj.update(chunk)
    return hashobj


def checksum(path: PATH, algo='sha1', length=-1, offset=0):
    chunks = read_as_chunks(path, length=length, offset=offset)
    return compute_checksum(chunks, algo=algo)


def checksum_hexdigest(path: PATH, algo='sha1', length=-1, offset=0):
    hashobj = checksum(path, algo=algo, length=length, offset=offset)
    return hashobj.hexdigest()


def b64_encode_data_url(mediatype: str, content: bytes) -> str:
    b64 = base64.b64encode(content).decode('ascii')
    return 'data:{};base64,{}'.format(mediatype, b64)


def b64_encode_local_file(path: PATH) -> str:
    mediatype = mimetypes.guess_type(path)[0]
    with open(path, 'rb') as fin:
        return b64_encode_data_url(mediatype, fin.read())


def spread_by_prefix(filename: str, depth: int = 2) -> list:
    names = []
    for i in range(depth):
        start = i * 2
        stop = start + 2
        part = filename[start: stop]
        if not part:
            break
        names.append(part)
    names.append(filename)
    return names


def random_hex(length=24) -> str:
    size = sum(divmod(length, 2))
    bs = os.urandom(size)
    return bs.hex()[:length]


def guess_content_type(content: bytes):
    if content.startswith(b'%PDF-'):
        return 'application/pdf'
    if content.startswith(b'\x89PNG\r\n\x1a\n'):
        return 'image/png'
    if content.startswith(b'\xFF\xD8\xFF'):
        return 'image/jpeg'
