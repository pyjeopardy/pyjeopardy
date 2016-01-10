class Answer:
    TEXT = 1
    IMAGE = 2
    AUDIO = 3
    VIDEO = 4

    def __init__(self, type, data, question, double):
        self._type = type
        self._data = data
        self._question = question
        self._double = double

    def is_text(self):
        return self._type == Answer.TEXT

    def is_double(self):
        return self._double
