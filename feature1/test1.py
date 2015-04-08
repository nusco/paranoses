import unittest
import parallel_test
import time, os

class Test1(parallel_test.ParallelTest):
    _multiprocess_shared_ = True
#    _multiprocess_can_split_ = True

    def setUp(self):
        print "setup Test1 in " + str(os.getpid())

    def tearDown(self):
        print "teardown Test1 in " + str(os.getpid())

    def test_a(self):
        for i in range(5):
            time.sleep(1)
            print "a" + str(i)

    def test_b(self):
        for i in range(5):
            time.sleep(1)
            print "b" + str(i)
