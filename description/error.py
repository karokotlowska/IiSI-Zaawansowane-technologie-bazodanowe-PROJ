class Error:
    message: str
    action: str
    thread: str

    def __init__(self, message: str, action: str, thread: str):
        self.message = message
        self.action = action
        self.thread = thread
