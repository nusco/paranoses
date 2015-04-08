import unittest
import os
import keymaster_factory

class ParallelTest(unittest.TestCase):
    @classmethod
    def setup_class(cls):
        with keymaster_factory.lock:
            if keymaster_factory.keymaster == None:
                keymaster_factory.keymaster = "something (later it will be the process itself)"
                print "GLOBAL SETUP in " + str(os.getpid())
                # TODO: make it a daemon process? send it a poison pill at the end?

    @classmethod
    def teardown_class(cls):
        with keymaster_factory.lock:
            if keymaster_factory.keymaster != None:
                keymaster_factory.keymaster = None
                print "GLOBAL TEARDOWN in " + str(os.getpid())

