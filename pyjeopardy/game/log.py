class Log:
    def __init__(self, cur_round):
        # dict: answer -> list of log entries
        self._entries = {}
        self._round = cur_round

        # "timestamp": incrementing number for identification and ordering of
        # entries
        self._next_time = 0

    def add(self, answer, player, points):
        if answer not in self._entries:
            self._entries[answer] = []

        entry = LogEntry(player, points, self._get_next_time())
        self._entries[answer].append(entry)

    def answer_closed(self, answer):
        if answer not in self._entries:
            self._entries[answer] = []

        self._entries[answer].append(LogEnd())

    def get(self, answer):
        entries = self._entries.get(answer)

        if not entries:
            return []

        if type(entries[-1]) == LogEnd:
            return entries[:-1]
        return entries

    def is_closed(self, answer):
        entries = self._entries.get(answer, [])
        try:
            return type(entries[-1]) == LogEnd
        except IndexError:
            return False

    def round_finished(self):
        for category in self._round.categories:
            for answer in category.answers:
                if not self.is_closed(answer):
                    return False
        return True

    def get_winner_of_answer(self, answer):
        entries = self.get(answer)
        try:
            if entries[-1].points > 0:
                    return entries[-1].player
        except IndexError:
            return None

    def _get_next_time(self):
        tmp = self._next_time
        self._next_time += 1
        return tmp

class LogEntry:
    def __init__(self, player, points, time):
        self.player = player
        self.points = points
        self.time = time

class LogEnd:
    pass
