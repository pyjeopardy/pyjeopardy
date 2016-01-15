class Answer:
    TEXT = 1
    IMAGE = 2
    AUDIO = 3
    VIDEO = 4

    def __init__(self, type_, data, question, double, points):
        self._type = type_
        self._data = data
        self._question = question
        self._double = double
        self._points = points

    def is_text(self):
        return self._type == Answer.TEXT

    def is_double(self):
        return self._double

    def get_points(self):
        return self._points
