import unittest
import multiprocessing
import os
import keymaster
import keymaster_commands

_keymaster = None
_keymaster_locking_queue = multiprocessing.Queue()
_keymaster_process_lock = multiprocessing.Lock()

class ParallelTest(unittest.TestCase):
    @classmethod
    def setup_class(cls):
        with _keymaster_process_lock:
            global _keymaster
            if _keymaster == None:
                print "Starting keymaster from main process (" + str(os.getpid()) + ")"
                _keymaster = keymaster.Keymaster(_keymaster_locking_queue)
                _keymaster.daemon = True
                _keymaster.start()

    @classmethod
    def teardown_class(cls):
        pass # TODO: the daemon terminates on its own, but do we need to do anything else here?

    def setUp(self):
        context = "X" # temporary catch-all value
        command = keymaster_commands.LockCommand(context)
        _keymaster_locking_queue.put(command)
        print "Process " + str(os.getpid()) + " send a locking command. Waiting on event..."
        # TODO: wait until we have permission to run
        print "...event triggered. Process " + str(os.getpid()) + " owns context " + context + "."

    def tearDown(self):
        context = "X" # temporary catch-all value
        command = keymaster_commands.ReleaseCommand(context)
        _keymaster_locking_queue.put(command)
        print "Process " + str(os.getpid()) + " sent a release command."
