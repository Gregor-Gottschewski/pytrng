from src.pytrng.DataCollector import DataCollector
from src.pytrng.RandomBitList import RandomBitList
from bitarray import bitarray
import hashlib


def check_balance(bits: list, max_diff):
    """
    Checks if bits array contains same amount of ones and zeros.

    Parameters
    ----------
    bits : list
        the bits list to check
    max_diff : int
        the maximal difference between the amount of ones and zeros

    Returns
    -------
    True
        if input bits list contains same amount of ones and zeros
    """

    zeros = 0
    ones = 0
    for bit in bits:
        if bit == 0:
            zeros += 1
        else:
            ones += 1

    return ones in range(zeros - max_diff, zeros + max_diff + 1)


class pytrng:
    """
    The main class of pytrng to generate random numbers

    Attributes
    ----------
    dc : DataCollector
        DataCollector instance to get data

    Methods
    -------
    generate_random(data: RandomBitList = None)
        generates bytes and uses the DataCollector if no input data is given
    """

    def __init__(self, length):
        if length not in [160, 224, 256, 384, 512]:
            raise ValueError("Length has to be 160, 224, 256, 384 or 512.")

        self.length = length
        self.dc = DataCollector(256)

    def hash_input(self, data: bytes) -> bytes:
        """Hashes the input data

        Parameters
        ----------
        data : bytes
            data to hash

        Returns
        -------
        bytes
            hash as bytes
        """

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

    def generate_random(self, data: RandomBitList = None) -> bytes:
        """
        Generates bytes and uses the DataCollector if no input data is given
        
        Parameters
        ----------
        data : RandomBitList

        """
        if data is None:
            data = RandomBitList()
            data.append(self.dc.get_mouse_pos_pool())
            data.append(self.dc.get_time_since_epoch())
            data.append(self.dc.get_sys_uptime())
            data.append(self.dc.get_disk_speed())
            data.append(self.dc.get_sensors())

        hashed_data = list()

        for d in data:
            hashed_d = self.hash_input(d)
            b = bitarray()
            b.frombytes(hashed_d)
            hashed_data.append(b)

        pool = hashed_data[0]
        del hashed_data[0]
        for i in hashed_data:
            pool ^= i
            b = bitarray()
            b.frombytes(self.hash_input(pool.tobytes()))
            pool = b

        if check_balance(pool.tolist(), 20):
            return pool.tobytes()
        else:
            return self.generate_random()


if __name__ == "__main__":
    print("*****************************************")
    print("* Welcome to pytrng 0.0.1c0!            *")
    print("* A small true random number generator. *")
    print("* ------------------------------------- *")
    print("* License: MIT License                  *")
    print("* (c) Gregor Gottschewski               *")
    print("*****************************************")

    while True:
        while True:
            bit_length = int(input("Enter bit length [160, 224, 256, 384, 512] (Ctrl+C to quit): "))
            if bit_length in [160, 224, 256, 384, 512]:
                break

        print("Collecting data ...")
        print("Generated number: " + str(int.from_bytes(pytrng(bit_length).generate_random(), byteorder="big")))
