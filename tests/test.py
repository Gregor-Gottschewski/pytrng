import unittest
from src import pytrng


class Test(unittest.TestCase):
    def test_160_bit(self):
        """Test 160 bit – 20 byte"""
        r = pytrng.pytrng(160).generate_random()
        self.assertIsNotNone(r)
        self.assertEqual(len(r), 20)
        self.assertIsNot(r, bytes(20))

    def test_224_bit(self):
        """Test 224 bit – 28 byte"""
        r = pytrng.pytrng(224).generate_random()
        self.assertIsNotNone(r)
        self.assertEqual(len(r), 28)
        self.assertIsNot(r, bytes(28))

    def test_256_bit(self):
        """Test 256 bit – 32 byte"""
        r = pytrng.pytrng(256).generate_random()
        self.assertIsNotNone(r)
        self.assertEqual(len(r), 32)
        self.assertIsNot(r, bytes(32))

    def test_384_bit(self):
        """Test 384 bit – 48 byte"""
        r = pytrng.pytrng(384).generate_random()
        self.assertIsNotNone(r)
        self.assertEqual(len(r), 48)
        self.assertIsNot(r, bytes(48))

    def test_512_bit(self):
        """Test 512 bit – 64 byte"""
        r = pytrng.pytrng(512).generate_random()
        self.assertIsNotNone(r)
        self.assertEqual(len(r), 64)
        self.assertIsNot(r, bytes(64))

    def test_balance_checker(self):
        bits1 = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1]  # five zeros and ones
        bits2 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1]  # eleven zeros and five ones
        self.assertTrue(pytrng.check_balance(bits1, max_diff=0))
        self.assertFalse(pytrng.check_balance(bits2, max_diff=5))

    def test_custom_random_generator(self):
        r_list = pytrng.RandomBitList()
        r_list.append(b"7erwer")
        r_list.append(b"73jfdh")
        r_list.append(b"92927W")
        r = pytrng.pytrng(256).generate_random(data=r_list)
        self.assertIsNotNone(r)
        self.assertEqual(r, b'\xbe\x1dM>\xeb"bcA\x93/\xcd\xc7\x98Z\x13\x8f\xf1G\xa5\x1d(\x82\xe1'
                            b'\xbc2\xde\x06F\x1f\xf5E')


if __name__ == '__main__':
    unittest.main()
