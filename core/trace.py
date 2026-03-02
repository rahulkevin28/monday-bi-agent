class TraceLogger:
    def __init__(self):
        self.steps = []

    def log(self, message):
        self.steps.append(message)

    def get_steps(self):
        return self.steps