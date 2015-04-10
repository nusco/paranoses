import unittest
import multiprocessing
import os
import time
import random
import context_dealer

_queue_to_context_dealer = None
_queue_from_context_dealer = None
_context_dealer = None
_context_dealer_process_lock = multiprocessing.Lock()

class ParallelTest(unittest.TestCase):
    _multiprocess_shared_ = True
    
    @classmethod
    def setup_class(cls):
        with _context_dealer_process_lock:
            global _context_dealer
            global _queue_to_context_dealer
            global _queue_from_context_dealer
            if _context_dealer == None:
                print "Starting context_dealer in main process (" + str(os.getpid()) + ")"
                
                _queue_to_context_dealer = multiprocessing.Queue()
                _queue_from_context_dealer = multiprocessing.Queue()
                _context_dealer = context_dealer.ContextDealer(_queue_to_context_dealer, _queue_from_context_dealer)
                _context_dealer.daemon = True
                _context_dealer.start()

    def setUp(self):
        self.test_id = str(random.randint(0, 1000000000)) # TODO: temporary. use a serial that is different for each test instead
        print "Test " + self.test_id + " in process " + str(os.getpid()) + " asks to own a context"

        _queue_to_context_dealer.put("GET")
        self.context = _queue_from_context_dealer.get()

        print "Test " + self.test_id + " in process " + str(os.getpid()) + " acquired context " + self.context + " and can proceed."
        
    def tearDown(self):
        _queue_to_context_dealer.put(self.context)

        print "Test " + self.test_id + " in process " + str(os.getpid()) +  " released context " + self.context + "."
