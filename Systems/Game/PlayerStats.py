import json


class PlayerStats(object):
    def __init__(self, name):
        self.name = name
        self._stats = None

    def _get_file_path(self):
        return "Stats/" + self.name + ".sts"

    def load(self):
        close_file = False
        file = None
        try:
            file = open(self._get_file_path())
            close_file = True
            file_content = file.read()
        except FileNotFoundError:
            file_content = '{ "lost": 0, "won": 0 }'

        json_content = json.loads(file_content)
        self._stats = json_content

        if close_file and file is not None:
            file.close()

    def save(self):
        json_content = self._stats
        file_content = json.dumps(json_content, indent=4)

        file = open(self._get_file_path(), 'w')
        file.write(file_content)
        file.close()

    def get_wins(self):
        return int(self._stats['won'])

    def get_loses(self):
        return int(self._stats['lost'])

    def increment_wins(self):
        if self._stats is not None:
            self._stats['won'] += 1

    def increment_loses(self):
        if self._stats is not None:
            self._stats['lost'] += 1
