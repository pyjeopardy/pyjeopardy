import json

from .category import Category
from .answer import Answer


class ParserError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value


class Round:
    def __init__(self):
        self.name = None
        self.categories = []

    def load(self, filename):
        try:
            f = open(filename)
            data = json.load(f)
        except (OSError, IOError) as e:
            raise ParserError("Cannot open file {}: {}".format(filename,
                                                               str(e)))
        except ValueError as e:
            raise ParserError("Invalid JSON: {}".format(str(e)))

        if type(data) != dict:
            raise ParserError("Invalid format, expected dict")

        # remove current categories
        del self.categories[:]

        # name
        if "name" in data:
            self.name = data["name"]
        else:
            raise ParserError("Name is missing")

        # categories
        if "categories" not in data:
            raise ParserError("Categories are missing")

        for category in data["categories"]:
            category_obj = self._parse_category(category)
            self.categories.append(category_obj)

    def _parse_category(self, json):
        if type(json) != dict:
            raise ParserError("Invalid format, expected dict inside "
                              "categories")

        # name
        if "name" not in json:
            raise ParserError("Name for category is missing")

        # create category
        category_obj = Category(json["name"])

        # answers
        if "answers" not in json:
            raise ParserError("Answers for category are missing")

        points = 0
        for answer in json["answers"]:
            points = points + 100
            answer_obj = self._parse_answer(answer, points)
            category_obj.add(answer_obj)

        return category_obj

    def _parse_answer(self, json, points):
        if type(json) != dict:
            raise ParserError("Invalid answer format, expected "
                              "dict")

        # get data
        answer_type = Answer.TEXT

        if "answer" not in json:
            raise ParserError("Answer for answer is missing")

        if "question" not in json:
            raise ParserError("Question for answer is missing")

        answer_double = False
        if "doublejeopardy" in json:
            if type(json["doublejeopardy"]) == bool:
                answer_double = json["doublejeopardy"]
            else:
                raise ParserError("Doublejeopardy field in answer must be "
                                  "true or false")

        # create answer
        return Answer(answer_type, json["answer"], json["question"],
                      answer_double, points)
