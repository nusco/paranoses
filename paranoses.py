import unittest
import multiprocessing
import os
import time
import random
import keymaster

_keymaster_contexts_to_owners = None
_keymaster_bookings = None
_keymaster = None
_keymaster_locking_queue = multiprocessing.Queue()
_keymaster_process_lock = multiprocessing.Lock()

class ParallelTest(unittest.TestCase):
    @classmethod
    def setup_class(cls):
        with _keymaster_process_lock:
            global _keymaster_contexts_to_owners
            global _keymaster_bookings
            if _keymaster_contexts_to_owners == None:
                print "Starting keymaster in main process (" + str(os.getpid()) + ")"
                manager = multiprocessing.Manager()
                _keymaster_contexts_to_owners = manager.dict()
                _keymaster_bookings = manager.dict()
                _keymaster = keymaster.Keymaster(_keymaster_contexts_to_owners, _keymaster_bookings)
                _keymaster.daemon = True
                _keymaster.start()
        
    @classmethod
    def teardown_class(cls):
        pass # TODO: the daemon terminates on its own, but do we need to do anything else here?

    def setUp(self):
        self.test_id = str(random.randint(0, 1000000000)) # TODO: temporary. use a serial that is different for each test instead
        context = "X" # temporary catch-all value
        print "Test " + self.test_id + " in process " + str(os.getpid()) + " asks to own context " + context
        _keymaster_bookings[self.test_id] = context

        # TODO: use polling for now. Maybe events later?
        while not self._is_owner_of(context):
            time.sleep(0.1)

        print "Test " + self.test_id + " in process " + str(os.getpid()) + " acquired context " + context + " and can proceed."

    def _is_owner_of(self, context):
        if not _keymaster_contexts_to_owners.has_key(self.test_id):
            return False
        return _keymaster_contexts_to_owners[self.test_id] == context
        
    def tearDown(self):
        context = "X" # temporary catch-all value
        _keymaster_contexts_to_owners.remove(self.test_id)
        print "Test " + self.test_id + " in process " + str(os.getpid()) +  " released context " + context + "."
