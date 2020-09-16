__all__ = ('SurahNotFound', 'IncorrectAyahArguments', 'IncorrectPageNumber', 'IncorrectJuzNumber', 'SearchError')


class SurahNotFound(Exception):
    def __init__(self, message="That Surah doesn't exist!"):
        self.message = message

    def __str__(self):
        return self.message


class IncorrectAyahArguments(Exception):
    def __init__(self, message="That ayah doesn't exist!"):
        self.message = message

    def __str__(self):
        return self.message


class IncorrectPageNumber(Exception):
    def __init__(self, message="That page doesn't exist!"):
        self.message = message

    def __str__(self):
        return self.message


class IncorrectJuzNumber(Exception):
    def __init__(self, message="That juz doesn't exist!"):
        self.message = message

    def __str__(self):
        return self.message


class SearchError(Exception):
    def __init__(self, message="There are no results of this term"):
        self.message = message

    def __str__(self):
        return self.message

