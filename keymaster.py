import threading

_call_lock = threading.Lock()
_context_locks = {}

def lock(key):
  with _call_lock:
    if not _context_locks.has_key(key):
      _context_locks[key] = threading.Lock()
    _context_locks[key].acquire(3600)

def unlock(key):
  with _call_lock:
    if not _context_locks.has_key(key):
      raise Exception("Unknown key: " + key)
    _context_locks[key].release()

