import threading
import multiprocessing
import os
import time

class ContextDealer(multiprocessing.Process):
  def __init__(self, queue_in, queue_out):
    multiprocessing.Process.__init__(self, name="keymaster")
    self.queue_in = queue_in
    self.queue_out = queue_out
    self.locked_contexts = {"X" : False, "Y" : False, "Z" : False, "W": False}
    self.access_lock = threading.Lock()

  def run(self):
    print "ContextDealer process started with id " + str(os.getpid())

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
              print "ContextDealer got a locking request. Returning context: " + context

              self.locked_contexts[context] = True
              self.queue_out.put(context)
              return
      raise Exception("No available context left. You cannot have more parallel test processes than you have contexts.")

  def _release_context(self, context):
      print "ContextDealer got a release request. Releasing context: " + context

      self.locked_contexts[context] = False
