from src.pytrng.DataCollector import DataCollector
from src.pytrng.DataPool import DataPool


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

    def __init__(self, length=256):
        self.length = length
        self.dc = DataCollector(256)

    def generate_random(self, data_pool: DataPool = None) -> bytes:
        custom_dp = True

        if data_pool is None:
            custom_dp = False
            data_pool = DataPool(self.length)
            data_pool.append(self.dc.get_mouse_pos_pool())
            data_pool.append(self.dc.get_time_since_epoch())
            data_pool.append(self.dc.get_sys_uptime())
            data_pool.append(self.dc.get_disk_speed())
            data_pool.append(self.dc.get_sensors())

        if check_balance(data_pool.to_bits().tolist(), 20):
            return data_pool.to_bytes()
        else:
            if not custom_dp:
                return self.generate_random()
            else:
                raise ValueError("DataPool not balanced.")


if __name__ == "__main__":
    print("*****************************************")
    print("* Welcome to pytrng.                    *")
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
