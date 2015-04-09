import unittest
import paranoses
import time, os

class Test2(paranoses.ParallelTest):
    _multiprocess_shared_ = True

    def test_c(self):
        for i in range(5):
            time.sleep(1)
            print "c" + str(i)

    def test_d(self):
        for i in range(5):
            time.sleep(1)
            print "d" + str(i)
