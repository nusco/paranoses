import unittest
import paranoses
import time, os

class Test1(paranoses.ParallelTest):
    def test_a(self):
        for i in range(5):
            time.sleep(1)
            print "a" + str(i)

    def test_b(self):
        for i in range(5):
            time.sleep(1)
            print "b" + str(i)
