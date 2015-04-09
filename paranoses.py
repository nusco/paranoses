import unittest
import multiprocessing
import os
import time
import random
import keymaster

_queue_to_keymaster = None
_queue_from_keymaster = None
_keymaster = None
_keymaster_process_lock = multiprocessing.Lock()

class ParallelTest(unittest.TestCase):
    @classmethod
    def setup_class(cls):
        with _keymaster_process_lock:
            global _keymaster
            global _queue_to_keymaster
            global _queue_from_keymaster
            if _keymaster == None:
                print "Starting keymaster in main process (" + str(os.getpid()) + ")"
                
                _queue_to_keymaster = multiprocessing.Queue()
                _queue_from_keymaster = multiprocessing.Queue()
                _keymaster = keymaster.Keymaster(_queue_to_keymaster, _queue_from_keymaster)
                _keymaster.daemon = True
                _keymaster.start()

    def setUp(self):
        self.test_id = str(random.randint(0, 1000000000)) # TODO: temporary. use a serial that is different for each test instead
        print "Test " + self.test_id + " in process " + str(os.getpid()) + " asks to own a context"

        _queue_to_keymaster.put("GET")
        self.context = _queue_from_keymaster.get()

        print "Test " + self.test_id + " in process " + str(os.getpid()) + " acquired context " + self.context + " and can proceed."
        
    def tearDown(self):
        _queue_to_keymaster.put(self.context)

        print "Test " + self.test_id + " in process " + str(os.getpid()) +  " released context " + self.context + "."
