# pytrng

![License: MIT](https://img.shields.io/github/license/gregor-gottschewski/pytrng)
![Language: Python](https://img.shields.io/badge/Language-Python-blue)

**A Python module to generate true random numbers.**

_pytrng_ contains a true random number generator (TRNG) based on physical events, and a
pseudo random number generator (PRNG).
It uses multiple inputs to generate a random bit array and does not need any extra hardware.

> Do not use the output of this package for encryption software!

## Input Pool
The following TRNG input data is hashed (SHA1 to SHA512) and connected with XOR:

* mouse position
* time since _epoch_
* system uptime
* disk speed (create and delete a temporary file)
* sensor temperatures

Every input is hashed and concatenated with the previous input.
This result is hashed again and concatenated with the next input.
When all inputs are hashed and concatenated, the result is hashed again used as output.

This model shows how that process works:

![pytrng structure image](images/pytrng_structure.jpg)

## Installation and quickstart

> pytrng is under development.
> You find it on [**TestPyPi**](https://test.pypi.org/project/pytrng/) and [**GitHub**](https://github.com/Gregor-Gottschewski/pytrng).

You install pytrng via pip:

    pip install -i https://test.pypi.org/simple/ --no-deps pytrng

Initialize `pytrng` with `512` as a parameter to generate a 512-bit number (only `160`, `224`, `256`, `384` and `512` are
allowed):

```python
from pytrng import pytrng
trng = pytrng(512)
random_num = trng.generate_random()
print(random_num) # random_num as bytes
print(int.from_bytes(random_num, byteorder='big')) # random_num as int
```

You receive raw data using the `DataCollector` class (TRNG-data):

```python
from pytrng import DataCollector
dc = DataCollector(256) # 256-bit output data
print("Mouse position: " + str(dc.get_mouse_position()))
print("Time since epoch: " + str(dc.get_time_since_epoch()))
print("System uptime: " + str(dc.get_sys_uptime()))
print("Disk speed: " + str(dc.get_disk_speed()))
print("Sensor temperatures: " + str(dc.get_sensors()))
```

You create your own `DataPool` to use custom input data:

```python
from src.pytrng import pytrng
from src.pytrng import DataPool
from src.pytrng import DataCollector

# custom data pool
dp = DataPool(512)

# collect data
dc = DataCollector(512)
dp.append(b'sh273w')            # a static custom value
dp.append(dc.get_sensors())     # DataCollector sensor data
dp.append(dc.get_sys_uptime())  # DataCollector system uptime

# generate random bytes
r = pytrng()
r.generate_random(dp)
```

## License

**MIT License**

> Copyright (c) 2023 - 2025 Gregor Gottschewski
>
> Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
> documentation files (the “Software”), to deal in the Software without restriction, including without limitation the
> rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit
> persons to whom the Software is furnished to do so, subject to the following conditions:
>
> The above copyright notice and this permission notice shall be included in all copies or substantial portions of the
> Software.
>
> THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
> WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS
> OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
> OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.