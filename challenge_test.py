#!/usr/bin/env python3
#
# Implementation for the get-in-IT and Bertrandt cooding challenge on:
# https://www.get-in-it.de/coding-challenge#mitmachen
#
# Author: Christian Rebischke - <christian.rebischke@tu-clausthal.de>
# Date: 2019-05-04
#
# This is our unittest for testing our calculation

import unittest
from challenge import Challenge


class TestMain(unittest.TestCase):

    # This is a small test to verify our result
    def test_result(self):
        # this is our expected result for the shortest path
        expected_result = [18, 810, 595, 132, 519, 71, 432, 246]
        challenge = Challenge()
        path = challenge.calculate_shortest_path()
        self.assertEqual(expected_result, path[0])


if __name__ == '__main__':
    unittest.main()
