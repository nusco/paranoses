import threading
import multiprocessing
import os
import time

class Keymaster(multiprocessing.Process):
  def __init__(self, contexts_to_owners, bookings):
    multiprocessing.Process.__init__(self, name="keymaster")
    self.contexts_to_owners = contexts_to_owners
    self.bookings = bookings

  def run(self):
    print "Keymaster process started with id " + str(os.getpid())
    while True:
      for booker, context in self.bookings.items():
          if self._is_available(context):
              del self.bookings[booker]
              self.contexts_to_owners[context] = booker
              print "Keymaster allowed " + booker + " to own context " + context
      time.sleep(1)

  def _is_available(self, context):
    return not self.contexts_to_owners.has_key(context)