class Category:
    def __init__(self, name):
        self.name = name
        self.answers = []

    def add(self, answer):
        self.answers.append(answer)
