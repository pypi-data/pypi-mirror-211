from re import Match


class Replacer:
    def __init__(self, replace_str: str):
        self.replace_str = replace_str

    def replacement(self, match: Match):
        group1 = match.group(1)
        group6 = match.group(6)
        group7 = self.replace_str
        group8 = match.group(8)
        return f'{group1}{group6}{group7}{group8}'

