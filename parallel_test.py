import unittest
import os
from multiprocessing import Lock

_keymaster_process_lock = Lock()
_keymaster = None

class ParallelTest(unittest.TestCase):
    @classmethod
    def setup_class(cls):
        with _keymaster_process_lock:
            global _keymaster
            if _keymaster == None:
                _keymaster = "something (later it will be the process itself)"
                print "GLOBAL SETUP in " + str(os.getpid())
                # TODO: make it a daemon process? send it a poison pill at the end?

    @classmethod
    def teardown_class(cls):
        global _keymaster
        with _keymaster_process_lock:
            if _keymaster != None:
                _keymaster = None
                print "GLOBAL TEARDOWN in " + str(os.getpid())

