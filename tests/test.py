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
        dp = pytrng.DataPool(512)
        dp.append(b'2hags')
        dp.append(b'83fgd')
        dp.append(b'#sdfx')
        r = pytrng.pytrng(512).generate_random(dp)
        self.assertEqual(r, b'\x02P\t~\xad\x9c\x7f\xa3\xe0[\x96Z\x8a\xcb\xc8\xbb{\x96\xe1m\x8d\x8a\xc0\xe9o\xae\xc0?,'
                            b'\xb2\\z\x04\xfcv\xcb.\xa9r1\x98\xe9\\@r\xf1\x9f\xb0\xfa!\xfb\x0c#\xb5y\x06~3\x8azA9\x85'
                            b'\xad'
)


if __name__ == '__main__':
    unittest.main()
