class LockCommand:
  def __init__(self, context):
      self.context = context

  def __str__():
    return "Command: Lock " + self.context

class ReleaseCommand:
  def __init__(self, context):
      self.context = context

  def __str__():
    return "Command: Release " + self.context
