import os
import time
import psutil
from sys import platform


def _get_last_byte(__data: int) -> int:
    """Returns the last byte of the specified integer."""
    if __data is None:
        raise ValueError("__data is None")
    return __data & 0xFF


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

        The CPU jitter is the time between two calls to perf_counter_ns().
        Between these calls, the CPU is busy with a while loop.
        A sleep cannot be used, because it would not be precise enough due to OS scheduling.

        Returns
        -------
        bytes
            the hashed CPU jitter
        """
        out = bytearray()
        for _ in range(self.bit_length // 8):
            t1 = time.perf_counter_ns()
            while time.perf_counter_ns() - t1 < 10:
                pass
            t2 = time.perf_counter_ns()
            out.append(_get_last_byte(t2 - t1))
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

        out = bytearray()

        for _ in range(self.byte_length):
            start_t = time.perf_counter_ns()
            with open(file_path, "wb") as f:
                f.write(b"1")
            os.remove(file_path)
            end_t = time.perf_counter_ns()
            out.append(_get_last_byte(end_t - start_t))
        return bytes(out)

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
