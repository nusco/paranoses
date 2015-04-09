import threading
import multiprocessing
import os

class Keymaster(multiprocessing.Process):
  def __init(self):
    multiprocessing.Process.__init__(self, name="keymaster")
    self._call_lock = threading.Lock()
    self._context_locks = {}

  def run(self):
    print "Keymaster process started with id " + str(os.getpid())
    while True:
      pass

  def lock(self, context):
    self._lock_for[context].acquire(3600)

  def release(self, context):
    self._lock_for[context].release()

  def _lock_for(self, context):
    with self._call_lock:
      if not self._context_locks.has_key(context):
        self._context_locks[context] = threading.Lock()
      return self._context_locks[context]

