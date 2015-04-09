import threading
import multiprocessing
import os
import time

class Keymaster(multiprocessing.Process):
  def __init__(self, locking_queue):
    multiprocessing.Process.__init__(self, name="keymaster")
    self.locking_queue = locking_queue
    self.call_lock = threading.Lock()
    self.context_locks = {}

  def run(self):
    print "Keymaster process started with id " + str(os.getpid())
    while True:
      command = self.locking_queue.get()
      print "Keymaster got command: " + command

  def lock(self, context):
    print "Keymaster acquiring lock of " + context
    self.lock_of[context].acquire(3600)
    print "Keymaster acquired lock of " + context

  def release(self, context):
    print "Keymaster releasing lock of " + context
    self.lock_of[context].release()
    print "Keymaster released lock of " + context

  def _lock_of(self, context):
    with self.call_lock:
      if not self.context_locks.has_key(context):
        self.context_locks[context] = threading.Lock()
      return self.context_locks[context]

