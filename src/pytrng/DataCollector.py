from bitarray import bitarray
import os
import time
import psutil

try:
    from pynput.mouse import Controller
    gui = True
except ImportError as e:
    gui = False
    print(e)
    print("WARNING: Skip mouse input.")


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

    def get_mouse_position(self) -> bytes | None:
        """Reads the current mouse x and y position and multiplies them

        Returns
        -------
        bytes
            the hashed mouse position
        None
            if pynput couldn't been imported
        """

        if not gui:
            return

        mouse = Controller()
        x = mouse.position[0] % ((2 ^ self.bit_length) - 1)
        y = mouse.position[1] % ((2 ^ self.bit_length) - 1)
        return (y * x).to_bytes(length=self.byte_length, byteorder="big")

    def get_mouse_pos_pool(self, strength=5) -> bytes | None:
        """Calls the get_mouse_position function multiple times and links their outputs using XOR.

        Parameters
        ----------
        strength : int
            sets how many times the mouse position should been read

        Returns
        -------
        bytes
            the hashed output
        None
            if pynput couldn't been imported
        """

        if not gui:
            return

        mouse_pos = bitarray()
        for i in range(0, strength):
            pos1 = bitarray()
            pos1.frombytes(self.get_mouse_position())
            time.sleep(0.15)
            pos2 = bitarray()
            pos2.frombytes(self.get_mouse_position())

            if pos1 != pos2:
                mouse_pos_new = pos1 ^ pos2
            else:
                mouse_pos_new = pos1

            if len(mouse_pos) == 0:
                mouse_pos = mouse_pos_new
            else:
                if mouse_pos_new != mouse_pos:
                    mouse_pos ^= mouse_pos_new

        return mouse_pos.tobytes()

    def get_time_since_epoch(self) -> bytes:
        """Returns the hashed time since epoch.

        Returns
        -------
        bytes
            the hashed time since epoch
        """

        t = round(time.time() * 100 % ((2 ^ self.bit_length) - 1))
        return t.to_bytes(length=self.byte_length, byteorder="big")

    def get_sys_uptime(self) -> bytes:
        """Returns the hashed system uptime.

        Returns
        -------
        bytes
            the hashed time since boot
        """

        uptime = time.time() - psutil.boot_time()
        t = round(uptime % ((2 ^ self.bit_length) - 1))
        return t.to_bytes(length=self.byte_length, byteorder="big")

    def get_disk_speed(self) -> bytes:
        """Measures the time the machine needs to create a new file and deleting it.

        Returns
        -------
        bytes
            the time between file creation and deletion
        """

        file_path = os.path.expanduser("~") + os.sep + "temp_trng_file"

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

        out = 1
        sensor_classes = psutil.sensors_temperatures()
        for sensor_in_class in sensor_classes:
            temp = sensor_classes[sensor_in_class]
            for list_element in temp:
                if list_element.current > 1:
                    out *= round(list_element.current) % ((2 ^ self.bit_length) - 1)

        return out.to_bytes(length=self.byte_length, byteorder="big")
