import threading

__call_lock__ = threading.Lock()
__context_locks__ = {}

def lock(key):
  with __call_lock__:
    if not __context_locks__.has_key(key):
      __context_locks__[key] = threading.Lock()
    __context_locks__[key].acquire(3600)

def unlock(key):
  with __call_lock__:
    if not __context_locks__.has_key(key):
      raise Exception("Unknown key: " + key)
    __context_locks__[key].release()

