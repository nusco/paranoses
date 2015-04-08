import unittest
import parallel_test
import time, os

class Test2(parallel_test.ParallelTest):
    _multiprocess_shared_ = True
#    _multiprocess_can_split_ = True

    def setUp(self):
        print "setup Test2 in " + str(os.getpid())

    def tearDown(self):
        print "teardown Test2 in " + str(os.getpid())

    def test_c(self):
        for i in range(5):
            time.sleep(1)
            print "c" + str(i)

    def test_d(self):
        for i in range(5):
            time.sleep(1)
            print "d" + str(i)
