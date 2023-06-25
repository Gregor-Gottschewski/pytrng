from bitarray import bitarray
import hashlib


def _bytes_to_bitarray(__data: bytes):
    b = bitarray()
    b.frombytes(__data)
    return b


class DataPool:
    def __init__(self, length):
        if length not in [160, 224, 256, 384, 512]:
            raise ValueError("Length has to be 160, 224, 256, 384 or 512.")

        self.pool = bitarray()
        self.length = length

    def _hash_input(self, data: bytes) -> bytes:
        if self.length == 256:
            m = hashlib.sha256()
        elif self.length == 160:
            m = hashlib.sha1()
        elif self.length == 384:
            m = hashlib.sha384()
        elif self.length == 224:
            m = hashlib.sha224()
        else:
            m = hashlib.sha512()

        m.update(data)
        return m.digest()

    def append(self, __object: bytes):
        if __object is None:
            return

        hashed_obj = self._hash_input(__object)

        b = _bytes_to_bitarray(hashed_obj)

        if len(self.pool) == 0:
            self.pool = b
            return

        if self.pool == b:
            print("Data in pool same as input. Skip!")
            return

        self.pool ^= b
        self.pool = _bytes_to_bitarray(self._hash_input(self.pool.tobytes()))

    def to_bits(self):
        return self.pool

    def to_bytes(self):
        return self.pool.tobytes()
