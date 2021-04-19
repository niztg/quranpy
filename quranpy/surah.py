"""
﷽
Alhamdulillah.
"""

from typing import Optional, List, Union, Iterable
from requests import get as request
from json import load

from .dict_data import LANGUAGES
from .enums import Editions, Chapters
from .exceptions import (
    SurahNotFound,
    IncorrectAyahArguments,
    IncorrectPageNumber,
    IncorrectJuzNumber,
    SearchError
)

__all__ = (
    'Surah',
    'Verse',
    'Page',
    'Juz',
    'Search',
    'EditionInfo',
    'show_verses',
    'Ayah',
    'Chapter'
)

_URL = "http://api.alquran.cloud/v1/{0}/{1}/{2}"
SEARCH_URL = "http://api.alquran.cloud/v1/search/{0}/{1}/{2}"
SURAH_URL = "http://api.alquran.cloud/v1/surah/{0}/editions/{1}"


class Surah:
    __slots__ = (
        'data',
        'edition',
        'chapter',
        'number',
        'arabic_name',
        'name',
        'translation',
        'period',
        'num_verses',
        'str_verses'
    )

    def __init__(
            self,
            chapter: Union[int, str, Chapters],
            edition: Optional[Editions] = Editions.sahih_international
    ):
        if isinstance(chapter, (int, str)):
            chapter = int(chapter)
            if (chapter > 114) or (chapter < 1):
                raise SurahNotFound(
                    "%s is not a chapter number in the Qur'an. The number must be inbetween 1 and 114" % chapter)
            self.chapter = chapter
        else:
            chapter = chapter.value
            self.chapter = chapter
        data = request(SURAH_URL.format(self.chapter, edition.value)).json()
        self.data = data['data'][0]
        self.edition = edition
        self.number = self.data.get('number')
        self.arabic_name = self.data.get('name')
        self.name = self.data.get('englishName')
        self.translation = self.data.get('englishNameTranslation')
        self.period = self.data.get('revelationType')
        self.num_verses = self.data.get('numberOfAyahs')
        self.str_verses = [verse['text'] for verse in self.data.get('ayahs')]

    def __repr__(self):
        return f"Surah {self.name} ({self.translation})"

    def __iter__(
            self
    ) -> Iterable:
        return iter(list(self.verses))

    @property
    def verses(
            self
    ) -> List:
        ayahs = list()
        for ayah in self.data.get('ayahs'):
            verse = ayah['number']
            ayahs.append(Verse(verse, self.edition))
        return ayahs

    def show_verses(
            self,
            ayah: Union[int, str],
    ) -> List:
        try:
            verse = int(ayah)
            if (verse < 1) or (verse > len(self.str_verses)):
                raise IncorrectAyahArguments("Ayah must be inbetween 1 and %s" % len(self.str_verses))
        except:
            _range = ayah.split("-")
            if len(_range) != 1:
                if len(_range) != 2:
                    raise IncorrectAyahArguments(
                        "Please enter your ayahs in the following format: 1:1-4 (For verses 1-4 of Surah Fatiha)"
                    )
                else:
                    verse = list()
                    try:
                        offset, limit = list(map(int, _range))
                    except ValueError:
                        raise IncorrectAyahArguments("You may not use any words to define your ayah!") from ValueError
                    if offset > limit:
                        offset = limit
                        limit = offset
                    for x in range(offset, limit + 1):
                        try:
                            verse.append(Verse(f"{self.chapter}:{x}", self.edition))
                        except:
                            break
            else:
                verse = [Verse(f"{self.chapter}:{ayah}", self.edition)]
        if isinstance(verse, int):
            return [Verse(f"{self.chapter}:{verse}")]
        else:
            return list(verse)

    def show_str_verses(
            self,
            ayah: Union[int, str],
    ) -> List[str]:
        try:
            verse = int(ayah)
            if (verse < 1) or (verse > len(self.str_verses)):
                raise IncorrectAyahArguments("Ayah must be inbetween 1 and %s" % len(self.str_verses))
        except:
            _range = ayah.split("-")
            if len(_range) != 1:
                if len(_range) != 2:
                    raise IncorrectAyahArguments(
                        "Please enter your ayahs in the following format: 1:1-4 (For verses 1-4 of Surah Fatiha)"
                    )
                else:
                    try:
                        offset, limit = list(map(int, _range))
                    except ValueError:
                        raise IncorrectAyahArguments("You may not use any words or special characters to define your "
                                                     "ayah other than -.") from ValueError
                    _return = list(self.str_verses[offset - 1:limit])
                    if not _return:
                        raise IncorrectAyahArguments(f"Verse {self.chapter}:{offset} does not exist!")
                    return _return
            else:
                try:
                    return [self.str_verses[int(ayah) - 1]]
                except Exception as error:
                    if isinstance(error, IndexError):
                        raise IncorrectAyahArguments(f"Verse {self.chapter}:{int(ayah)} does not exist!")
                    elif isinstance(error, ValueError):
                        raise IncorrectAyahArguments("You may not use any words or special characters to represent "
                                                     "your verses other than -.")
                    else:
                        raise error
        if isinstance(verse, int):
            return [self.str_verses[verse - 1]]

    def get_verses(
            self,
            *verses
    ):
        return list(map(self.show_verses, list(verses)))

    def get_str_verses(
            self,
            *verses
    ):
        return list(map(self.show_str_verses, list(verses)))


class Page:
    __slots__ = (
        'edition',
        'data',
        'number',
        'num_verses',
        'num_surahs'
    )

    def __init__(
            self,
            page: Union[int, str],
            edition: Optional[Editions] = Editions.sahih_international
    ):
        page = int(page)
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
    def surahs(self) -> List[Surah]:
        to_return = list()
        for surah in self.data.get('surahs').values():
            to_return.append(Surah(surah['number'], self.edition))
        return to_return


class Juz:
    __slots__ = (
        'edition',
        'data',
        'number',
        'num_ayahs',
        'num_surahs'
    )

    def __init__(
            self,
            number: Union[int, str],
            edition: Optional[Editions] = Editions.sahih_international
    ):
        number = int(number)
        if (number > 30) or (number < 1):
            raise IncorrectJuzNumber("Juz number should be inbetween 1 and 30.")
        data = request(_URL.format('juz', number, edition.value)).json()
        self.edition = edition
        self.data = data['data']
        self.number = self.data.get('number')
        self.num_ayahs = len(self.data.get('ayahs'))
        self.num_surahs = len(self.data.get('surahs'))

    def __repr__(self):
        return f"Juz {self.number} - {self.num_surahs} surahs"

    @property
    def surahs(self) -> List[Surah]:
        to_return = list()
        for surah in self.data.get('surahs').keys():
            to_return.append(Surah(surah, self.edition))
        return to_return


class Verse:
    __slots__ = (
        'data',
        'edition',
        'number',
        'text',
        'number_in_surah',
        'position',
        'is_sajda'
    )

    def __init__(
            self,
            ayah: Union[int, str],
            edition: Optional[Editions] = Editions.sahih_international
    ):
        data = request(_URL.format('ayah', ayah, edition.value)).json()
        if data.get('code') != 200:
            raise IncorrectAyahArguments(f"Verse {ayah} of the quran does not exist!")
        self.data = data['data']
        self.edition = edition
        self.number = self.data.get('number')
        self.text = self.data.get('text')
        self.number_in_surah = self.data.get('numberInSurah')
        self.position = f"{self.data['surah']['number']}:{self.number_in_surah}"
        self.is_sajda = self.data.get('sajda')

    def __repr__(self) -> str:
        return self.text

    @property
    def surah(self) -> Surah:
        return Surah(self.data['surah']['number'], self.edition)

    @property
    def juz(self) -> Juz:
        return Juz(self.data['juz'], self.edition)

    @property
    def page(self) -> Page:
        return Page(self.data['page'], self.edition)


class Search:
    __slots__ = (
        '_surah',
        'term',
        'edition',
        'data',
        'count',
        'str_verses'
    )

    def __init__(
            self,
            term: str,
            surah: Optional[Union[int, str, Chapters]] = None,
            edition: Optional[Editions] = Editions.sahih_international
    ):
        self._surah = surah
        if not self._surah:
            surah = "all"
        else:
            if isinstance(surah, Chapters):
                surah = surah.value
        try:
            data = request(SEARCH_URL.format(term, surah, edition.value)).json()
        except:
            raise SearchError("There are no results of this term in this edition.")
        self.term = term
        self.edition = edition
        self.data = data['data']
        self.count = self.data.get('count')
        self.str_verses = [verse['text'] for verse in self.data.get('matches')]

    def __repr__(self):
        if self._surah:
            return f"{self.count} count(s) of \"{self.term}\" in" \
                   f" Surah {self.data['matches'][0]['surah']['englishName']}" \
                   f" (in this edition)"
        else:
            return f"{self.count} count(s) of \"{self.term}\" in the Qur'an (in this edition)"

    def __iter__(self) -> Iterable:
        return iter(list(self.verses))

    @property
    def verses(self) -> List[Verse]:
        ayahs = list()
        for ayah in self.data.get('matches'):
            verse = ayah['number']
            try:
                ayahs.append(Verse(verse, self.edition))
            except:
                break
        return sorted(ayahs, key=lambda x: x.number)


class EditionInfo:
    __slots__ = (
        'usable',
        'english_name',
        'name',
        'identifier',
        'format',
        'type',
        'language',
        'direction'
    )

    def __init__(
            self,
            edition: Editions
    ):
        edition_data = load(open("quranpy/editions.json"))
        index = [e['identifier'] for e in edition_data].index(edition.value)
        data = edition_data[index]
        self.usable = edition
        self.english_name = data.get('englishName')
        self.name = data.get('name')
        self.identifier = data.get('identifier')
        self.format = data.get('format')
        self.type = data.get('type')
        self.language = (LANGUAGES.get(data.get('language')) or data.get('language')).capitalize()
        if data.get('direction'):
            self.direction = " ".join(
                list(data.get('direction'))). \
                replace("t", "to"). \
                replace("l", "Left"). \
                replace("r", "Right")
        else:
            self.direction = None

    def __repr__(self):
        return f"{self.name if self.english_name == 'Unknown' else self.english_name} " \
               f"Quran Edition (Indicator={self.identifier}, " \
               f"Language={self.language}, " \
               f"Direction={self.direction})"

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return

    def surah(
            self,
            chapter: Union[int, str, Chapters]
    ) -> Surah:
        return Surah(chapter, self.usable)

    def verse(
            self,
            verse: Union[int, str]
    ) -> Verse:
        return Verse(verse, self.usable)

    def page(
            self,
            page: Union[int, str]
    ) -> Page:
        return Page(page, self.usable)

    def juz(
            self,
            juz: Union[int, str]
    ) -> Juz:
        return Juz(juz, self.usable)


def show_verses(
        ayah: Union[int, str],
        edition: Optional[Editions] = Editions.sahih_international
) -> List[str]:
    if isinstance(ayah, int) or ayah.isdigit():
        return [str(Verse(ayah, edition))]
    else:
        try:
            surah, verses = ayah.split(":")
        except ValueError:
            raise IncorrectAyahArguments(
                "Please enter your verses in the following format: 2:225 (For Surah Baqarah verse 255)") from ValueError
        try:
            surah = int(surah)
        except:
            raise IncorrectAyahArguments("You may not use any words to define your verse")
        return list(Surah(int(surah), edition).show_str_verses(verses))


class Ayah(Verse):
    pass


class Chapter(Surah):
    pass
