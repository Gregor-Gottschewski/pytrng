import os
import time
import psutil
from sys import platform



class DataCollector:
    """The DataCollector collects input data and hashes it."""

    def __init__(self, bit_length: int):
        """Sets the length of the output

        Parameters
        ----------
        bit_length : int
            bit length of the output (160, 224, 256, 384, 512)
        """

        if bit_length % 2 != 0:
            raise ValueError("")

        self.bit_length = bit_length
        self.byte_length = bit_length // 8

    def get_cpu_jitter(self) -> bytes:
        """ Builds a random number from the CPU jitter.

        The process sleeps for 0.1 ms and then compares the time before and after the sleep.
        Only the last bit of the time difference is used to create a random number.
        The process is repeated for the number of bits in the output.

        Returns
        -------
        bytes
            the hashed CPU jitter
        """
        out: bytes = b""
        for _ in range(self.bit_length):
            t1 = time.perf_counter_ns()
            time.sleep(0.0001)
            t2 = time.perf_counter_ns()
            out += ((t2 - t1) & 1).to_bytes(length=1, byteorder="big")
        return out

    def get_time_since_epoch(self) -> bytes:
        """Returns the hashed time since epoch.

        Returns
        -------
        bytes
            the hashed time since epoch
        """

        t = round(time.time() * 100 % ((2 ** self.bit_length) - 1))
        return t.to_bytes(length=self.byte_length, byteorder="big")

    def get_sys_uptime(self) -> bytes:
        """Returns the hashed system uptime.

        Returns
        -------
        bytes
            the hashed time since boot
        """

        uptime = time.time() - psutil.boot_time()
        t = round(uptime % ((2 ** self.bit_length) - 1))
        return t.to_bytes(length=self.byte_length, byteorder="big")

    def get_disk_speed(self) -> bytes:
        """Measures the time between file creation and deletion.

        Returns
        -------
        bytes
            time between file creation and deletion
        """

        file_path = os.path.join(os.path.expanduser("~"), "temp_trng_file")

        start_t = time.time() * 100000

        f = open(file_path, "w")
        f.close()
        os.remove(file_path)

        end_t = time.time() * 100000

        t = round((end_t - start_t) % ((2 ^ self.bit_length) - 1))
        return t.to_bytes(length=self.byte_length, byteorder="big")

    def get_sensors(self) -> bytes:
        """Returns all sensor temperatures multiplied.

        Returns
        -------
        bytes
            hashed sensor temperatures
        """

        if platform != "linux":
            return b""

        out = 1
        sensor_classes = psutil.sensors_temperatures()
        for sensor_in_class in sensor_classes:
            temp = sensor_classes[sensor_in_class]
            for list_element in temp:
                if list_element.current > 1:
                    out *= round(list_element.current) % ((2 ** self.bit_length) - 1)

        return out.to_bytes(length=self.byte_length, byteorder="big")
