from quranpy.editions import Editions
from quranpy.exceptions import SurahNotFound, IncorrectAyahArguments
from requests import get as request
from typing import Optional

__all__ = ('Surah', 'Verse')

AYAH_URL = "http://api.alquran.cloud/v1/ayah/{0}/{1}"
SURAH_URL = "http://api.alquran.cloud/v1/surah/{0}/editions/{1}"


class Surah:
    """Represents a Surah of the Qur'an"""
    __slots__ = ('edition', 'chapter', 'data', 'number', 'arabic_name', 'name', 'translation', 'period', 'num_verses',)

    def __init__(
            self,
            chapter: int,
            edition: Optional[Editions] = Editions.sahih_international
    ):
        data = request(SURAH_URL.format(chapter, edition.value)).json()
        if data.get('code') != 200:
            raise SurahNotFound(
                "%s is not a chapter number in the Qur'an. The number must be inbetween 1 and 114" % chapter)
        self.edition = edition
        self.chapter = chapter
        self.data = data['data'][0]
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

    # these two tend to take a while

    @property
    def verses(self):
        ayahs = list()
        for ayah in self.data.get('ayahs'):
            verse = ayah['number']
            ayahs.append(Verse(verse))
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
    """Represents an ayah/verse of the Qur'an"""
    __slots__ = ('data', 'number', 'text', 'number_in_surah')

    def __init__(
            self,
            ayah,
            ediition: Optional[Editions] = Editions.sahih_international
    ):
        data = request(AYAH_URL.format(ayah, ediition.value)).json()
        if data.get('code') != 200:
            raise IncorrectAyahArguments(data['data'])
        self.data = data['data']
        self.number = self.data.get('number')
        self.text = self.data.get('text')
        self.number_in_surah = self.data.get('numberInSurah')

    def __repr__(self):
        return self.text

    @property
    def surah(self):
        return Surah(self.data['surah']['number'])
