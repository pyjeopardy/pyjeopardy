import json

class ParserError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

def parse_answer_file(filename):
    try:
        f = open(filename)
        data = json.load(f)
    except (OSError, IOError) as e:
        raise ParserError("Cannot open file {}: {}".format(filename, str(e)))
    except ValueError as e:
        raise ParserError("Invalid JSON: {}".format(e.msg))

    print(repr(data))
