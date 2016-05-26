class Answer:
    TEXT = 1
    IMAGE = 2
    AUDIO = 3
    VIDEO = 4

    def __init__(self, answertype, data, question, double, points):
        self._type = answertype
        self._data = data
        self._question = question
        self._double = double
        self._points = points

    def is_text(self):
        return self._type == Answer.TEXT

    def is_image(self):
        return self._type == Answer.IMAGE

    def get_text(self):
        if self.is_text():
            return self._data
        return None

    def get_path(self):
        if self.is_image():
            return self._data
        return None

    def is_double(self):
        return self._double

    def get_points(self):
        return self._points
