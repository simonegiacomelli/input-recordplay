from pathlib import Path


class DotoolKeys:
    def __init__(self):
        self.content = Path(__file__).parent / 'dotool_keys.txt'
        self.keys = set()
        for line in self.content.read_text().splitlines(keepends=False):
            key = line.split()[0]
            self.keys.add(key)

