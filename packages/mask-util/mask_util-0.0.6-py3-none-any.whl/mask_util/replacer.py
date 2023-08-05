from re import Match


class Replacer:
    def __init__(self, replace_str: str):
        self.replace_str = replace_str

    def replacement(self, match: Match):
        group1 = match.group(1)
        group2 = self.replace_str
        group3 = match.group(3)
        return f'{group1}{group2}{group3}'
