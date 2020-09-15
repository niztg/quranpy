from .editions import Editions
from .exceptions import SurahNotFound, IncorrectAyahArguments, IncorrectPageNumber, IncorrectJuzNumber
from requests import get as request
from typing import Optional

__all__ = ('Surah', 'Verse', 'Page', 'Juz', 'Search')

_URL = "http://api.alquran.cloud/v1/{0}/{1}/{2}"
SEARCH_URL = "http://api.alquran.cloud/v1/search/{0}/{1}/{2}"
SURAH_URL = "http://api.alquran.cloud/v1/surah/{0}/editions/{1}"


class Surah:
    __slots__ = ('data', 'edition', 'chapter', 'number', 'arabic_name', 'name', 'translation', 'period', 'num_verses',)

    def __init__(
            self,
            chapter: int,
            edition: Optional[Editions] = Editions.sahih_international
    ):
        if chapter > 114:
            raise SurahNotFound(
                "%s is not a chapter number in the Qur'an. The number must be inbetween 1 and 114" % chapter)
        data = request(SURAH_URL.format(chapter, edition.value)).json()
        self.data = data['data'][0]
        self.chapter = chapter
        self.edition = edition
        self.number = self.data.get('number')
        self.arabic_name = self.data.get('name')
        self.name = self.data.get('englishName')
        self.translation = self.data.get('englishNameTranslation')
        self.period = self.data.get('revelationType')
        self.num_verses = self.data.get('numberOfAyahs')

    def __repr__(self):
        return f"Surah {self.name} - {self.translation}"

    def __iter__(self):
        return iter(self.verses)

    @property
    def verses(self):
        ayahs = list()
        for ayah in self.data.get('ayahs'):
            verse = ayah['number']
            ayahs.append(Verse(verse, self.edition))
        return ayahs

    def show_verses(
            self,
            first: int,
            last: Optional[int] = None
    ):
        if not last:
            return Verse(f"{self.chapter}:{first}", self.edition)
        else:
            to_return = list()
            if first > last:
                first = last
                last = first
            for verse in range(first, last + 1):
                to_return.append(Verse(f"{self.chapter}:{verse}", self.edition))
        return to_return


class Verse:
    __slots__ = ('data', 'edition', 'number', 'text', 'number_in_surah')

    def __init__(
            self,
            ayah,
            edition: Optional[Editions] = Editions.sahih_international
    ):
        data = request(_URL.format('ayah', ayah, edition.value)).json()
        if data.get('code') != 200:
            raise IncorrectAyahArguments(data['data'])
        self.data = data['data']
        self.edition = edition
        self.number = self.data.get('number')
        self.text = self.data.get('text')
        self.number_in_surah = self.data.get('numberInSurah')

    def __repr__(self):
        return self.text

    @property
    def surah(self):
        return Surah(self.data['surah']['number'], self.edition)


class Page:
    __slots__ = ('edition', 'data', 'number', 'num_verses', 'num_surahs')

    def __init__(self,
                 page: int,
                 edition: Optional[Editions] = Editions.sahih_international):
        if page > 604:
            raise IncorrectPageNumber("Page number should be betwen 1 and 604")
        data = request(_URL.format('page', page, edition.value)).json()
        self.edition = edition
        self.data = data['data']
        self.number = self.data.get('number')
        self.num_verses = len(self.data.get('ayahs'))
        self.num_surahs = len(self.data.get('surahs'))

    def __repr__(self):
        return f"Qur'an Page {self.number} : {self.num_verses} verses"

    @property
    def surahs(self):
        to_return = list()
        for surah in self.data.get('surahs').values():
            to_return.append(Surah(surah['number'], self.edition))
        return to_return


class Juz:
    __slots__ = ('edition', 'data', 'number', 'num_ayahs', 'num_surahs')

    def __init__(
            self,
            number: int,
            edition: Optional[Editions] = Editions.sahih_international
    ):
        if number > 30:
            raise IncorrectJuzNumber("Juz number should be inbetween 1 and 30.")
        data = request(_URL.format('juz', number, edition.value)).json()
        self.edition = edition
        self.data = data['data']
        self.number = self.data.get('number')
        self.num_ayahs = len(self.data.get('ayahs'))
        self.num_surahs = len(self.data.get('surahs'))

    def __repr__(self):
        return f"Juz {self.number} - {self.num_surahs}"

    @property
    def surahs(self):
        to_return = list()
        for surah in self.data.get('surahs').values():
            to_return.append(Surah(surah['number'], self.edition))
        return to_return


class Search:
    __slots__ = ('_surah', 'term', 'edition', 'data', 'count')

    def __init__(
            self,
            term: str,
            surah: Optional[Surah] = None
    ):
        self._surah = surah
        edition = Editions.sahih_international
        if not surah:
            surah = "all"
        else:
            surah = surah.number
        data = request(SEARCH_URL.format(term, surah, edition.value)).json()
        self.term = term
        self.edition = edition
        self.data = data['data']
        self.count = self.data.get('count')

    def __repr__(self):
        if self._surah:
            return f"{self.count} count(s) of \"{self.term}\" in {self._surah}"
        else:
            return f"{self.count} count(s) of \"{self.term}\" in the Qur'an"

    @property
    def verses(self):
        ayahs = list()
        for ayah in self.data.get('matches'):
            verse = ayah['number']
            ayahs.append(Verse(verse, self.edition))
        return ayahs
