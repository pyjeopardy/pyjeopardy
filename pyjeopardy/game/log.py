class Log:
    def __init__(self):
        # dict: answer -> list of log entries
        self._entries = {}

        # "timestamp": incrementing number for identification and ordering of
        # entries
        self._next_time = 0

    def add(self, answer, player, points):
        if answer not in self._entries:
            self._entries[answer] = []

        entry = LogEntry(player, points, self._get_next_time())
        self._entries[answer].append(entry)

    def get(self, answer):
        return self._entries.get(answer, [])

    def get_winner(self, answer):
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
