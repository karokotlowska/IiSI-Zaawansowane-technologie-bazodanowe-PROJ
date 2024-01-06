class Error:
    message: str
    action: str
    thread: str
    exception: Exception

    def __init__(self, message: str, action: str, thread: str, exception: Exception = None):
        self.message = message
        self.action = action
        self.thread = thread
        self.exception = exception

    def __str__(self):
        return f"Error: {self.message}"
