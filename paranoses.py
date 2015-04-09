import unittest
import multiprocessing
import os
import keymaster

_keymaster_process_lock = multiprocessing.Lock()
_keymaster = None

class ParallelTest(unittest.TestCase):
    @classmethod
    def setup_class(cls):
        with _keymaster_process_lock:
            global _keymaster
            if _keymaster == None:
                print "Starting keymaster from main process (" + str(os.getpid()) + ")"
                _keymaster = keymaster.Keymaster()
                _keymaster.daemon = True
                _keymaster.start()

    @classmethod
    def teardown_class(cls):
      pass # let the daemon terminate on its own. do we need anything else here? think about it

    def setUp(self):
      self._keymaster_queue = multiprocessing.Queue()
      pass

    def tearDown(self):
      pass

