import unittest

import numpy as np

from manly_randomization_test import RandomizationTest

class TestSimpleCase(unittest.TestCase):

    """unittest methods for testing"""

    def test_simple1(self):

        group1 = np.array([1, 2, 3, 4, 5])
        group2 = np.array([1, 2, 3, 4, 5])

        test = RandomizationTest(group1, group2)
        p_value = test.test()

        self.assertTrue(p_value > 0.1)

    def test_simple2(self):

        group1 = np.array([1, 2, 3, 4, 5])
        group2 = np.array([10, 20, 30, 40, 50])

        test = RandomizationTest(group1, group2)
        p_value = test.test()

        self.assertTrue(p_value < 0.05)

    def test_simple2(self):

        group1 = np.array([1, 2, 3, 4, 5])
        group2 = np.array([10, 20, 30, 40, 50])

        test = RandomizationTest(group1, group2)
        p_value = test.test()

        self.assertTrue(p_value < 0.05)

    def test_simple3(self):

        group1 = np.random.normal(0, 1, size=100)
        group2 = np.random.normal(0, 1, size=100)

        test = RandomizationTest(group1, group2)
        p_value = test.test()

        self.assertTrue(p_value > 0.05)

    def test_simple4(self):

        group1 = np.random.normal(0, 1, size=100)
        group2 = np.random.normal(0.5, 1, size=100)

        test = RandomizationTest(group1, group2)
        p_value = test.test()

        self.assertTrue(p_value < 0.05)