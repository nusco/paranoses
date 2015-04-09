import unittest
import paranoses
import time, os

class Test2(paranoses.ParallelTest):
    _multiprocess_shared_ = True
#    _multiprocess_can_split_ = True

    def setUp(self):
        print "setup Test2 in " + str(os.getpid())
        paranoses.ParallelTest.setUp(self)

    def tearDown(self):
        print "teardown Test2 in " + str(os.getpid())
        paranoses.ParallelTest.tearDown(self)

    def test_c(self):
        for i in range(5):
            time.sleep(1)
            print "c" + str(i)

    def test_d(self):
        for i in range(5):
            time.sleep(1)
            print "d" + str(i)
