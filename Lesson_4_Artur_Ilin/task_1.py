import unittest


def get_sum(num_1=None, num_2=None):
    if num_1 and num_2:
        return num_1 + num_2
    return False


class TestGetSum(unittest.TestCase):
    def test_get_sum(self):
        """ test with input data """
        self.assertEqual(get_sum(2, 2), 4)

    def test_get_sum_empty(self):
        """ test without input data """
        self.assertFalse(get_sum())

    def test_get_sum_wrong(self):
        """ test with wrong input data """
        with self.assertRaises(TypeError):
            get_sum(2, 2, 2)
