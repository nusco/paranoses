import threading
import multiprocessing
import os
import time

class Keymaster(multiprocessing.Process):
  def __init__(self, queue_in, queue_out):
    multiprocessing.Process.__init__(self, name="keymaster")
    self.queue_in = queue_in
    self.queue_out = queue_out
    self.locked_contexts = {"X" : False, "Y" : False, "Z" : False, "W" : False, "XX" : False, "YY" : False, "ZZ" : False, "WW" : False}
    self.access_lock = threading.Lock()

  def run(self):
    print "Keymaster process started with id " + str(os.getpid())
    while True:
        request = self.queue_in.get()
        with self.access_lock:
            if (request == "GET"):
                self._return_context()
            else:
                self._release_context(request)

  def _return_context(self):
      for context, locked in self.locked_contexts.items():
          if not locked:
              self.locked_contexts[context] = True
              self.queue_out.put(context)
              print "Keymaster got a locking request. Returning context: " + context
              return
      raise Exception("No available context left. Go easy on those parallel processes.")

  def _release_context(self, context):
      print "Keymaster got a release request. Releasing context: " + context
      self.locked_contexts[context] = False
