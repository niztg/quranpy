from .enums import *
from .exceptions import SurahNotFound, IncorrectAyahArguments, IncorrectPageNumber, IncorrectJuzNumber, SearchError
from requests import get as request
from typing import Optional, List, Union

__all__ = ('Surah', 'Verse', 'Page', 'Juz', 'Search')

_URL = "http://api.alquran.cloud/v1/{0}/{1}/{2}"
SEARCH_URL = "http://api.alquran.cloud/v1/search/{0}/{1}/{2}"
SURAH_URL = "http://api.alquran.cloud/v1/surah/{0}/editions/{1}"


class Surah:
    __slots__ = ('data', 'edition', 'chapter', 'number', 'arabic_name', 'name', 'translation', 'period', 'num_verses', 'str_verses')

    def __init__(
            self,
            chapter: Union[int, Chapters],
            edition: Optional[Editions] = Editions.sahih_international
    ):
        if isinstance(chapter, int):
            if (chapter > 114) or (chapter < 1):
                raise SurahNotFound(
                    "%s is not a chapter number in the Qur'an. The number must be inbetween 1 and 114" % chapter)
        else:
            chapter = chapter.value
        data = request(SURAH_URL.format(chapter, edition.value)).json()
        self.data = data['data'][0]
        if isinstance(chapter, Chapters):
            self.chapter = chapter.value
        else:
            self.chapter = chapter
        self.edition = edition
        self.number = self.data.get('number')
        self.arabic_name = self.data.get('name')
        self.name = self.data.get('englishName')
        self.translation = self.data.get('englishNameTranslation')
        self.period = self.data.get('revelationType')
        self.num_verses = self.data.get('numberOfAyahs')
        self.str_verses = [verse['text'] for verse in self.data.get('ayahs')]

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
            ayah: Union[int, str],
    ):
        try:
            verse = int(ayah)
            if (verse < 1) or (verse > 6236):
                raise IncorrectAyahArguments("Ayah must be inbetween 1 and 6236")
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
                    for x in range(offset, limit+1):
                        verse.append(Verse(f"{self.chapter}:{x}", self.edition))
            else:
                verse = [Verse(f"{self.chapter}:{ayah}", self.edition)]
        if isinstance(verse, int):
            return [Verse(f"{self.chapter}:{verse}")]
        else:
            return list(verse)

    def show_str_verses(
            self,
            ayah: Union[int, str],
    ):
        try:
            verse = int(ayah)
            if (verse < 1) or (verse > 6236):
                raise IncorrectAyahArguments("Ayah must be inbetween 1 and 6236")
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
                        raise IncorrectAyahArguments("You may not use any words to define your ayah!") from ValueError
                    if offset > limit:
                        offset = limit
                        limit = offset
                    verse = "http://api.alquran.cloud/v1/surah/{0}/editions/{1}?offset={2}&limit={3}".format(self.chapter,
                                                                                                             self.edition.value,
                                                                                                             offset - 1,
                                                                                                             limit)
            else:
                verse = f"{self.chapter}:{ayah}"
        if isinstance(verse, int):
            data = request(_URL.format('ayah', f"{self.number}:{verse}", self.edition.value)).json()
            return [data['data']['text']]
        elif check_format(verse):
            data = request(_URL.format('ayah', verse, self.edition.value)).json()
            return [data['data']['text']]
        else:
            data = request(verse).json()
            ayahs = data['data'][0]['ayahs']
            if not isinstance(ayahs, list):
                raise IncorrectAyahArguments(ayahs)
            else:
                to_return = list()
                for ayah in ayahs:
                    to_return.append(ayah['text'])
            return to_return



class Verse:
    __slots__ = ('data', 'edition', 'number', 'text', 'number_in_surah', 'position')

    def __init__(
            self,
            ayah,
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

    def __repr__(self):
        return self.text

    @property
    def surah(self) -> Surah:
        return Surah(self.data['surah']['number'], self.edition)

    @property
    def juz(self):
        return Juz(self.data['juz'])

    @property
    def page(self):
        return Page(self.data['page'])


class Page:
    __slots__ = ('edition', 'data', 'number', 'num_verses', 'num_surahs')

    def __init__(
            self,
            page: int,
            edition: Optional[Editions] = Editions.sahih_international
    ):
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
    __slots__ = ('edition', 'data', 'number', 'num_ayahs', 'num_surahs')

    def __init__(
            self,
            number: int,
            edition: Optional[Editions] = Editions.sahih_international
    ):
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
        for surah in self.data.get('surahs').values():
            to_return.append(Surah(surah['number'], self.edition))
        return to_return


class Search:
    __slots__ = ('_surah', 'term', 'edition', 'data', 'count', 'str_verses')

    def __init__(
            self,
            term: str,
            surah: Optional[Union[int, Chapters]] = None,
            edition: Optional[Editions] = Editions.sahih_international
    ):
        self._surah = surah
        if not surah:
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
            return f"{self.count} count(s) of \"{self.term}\" in Surah {self.data['matches'][0]['surah']['englishName']} (in this edition)"
        else:
            return f"{self.count} count(s) of \"{self.term}\" in the Qur'an (in this edition)"

    @property
    def verses(self) -> List[Verse]:
        ayahs = list()
        for ayah in self.data.get('matches'):
            verse = ayah['number']
            try:
                ayahs.append(Verse(verse, self.edition))
            except:
                break
        return ayahs


def show_verses(
        ayah: Union[int, str],
        edition: Optional[Editions] = Editions.sahih_international
):
    # this doesn't return a list of the Verse object, it just returns text
    # good for when you just want the verse and nothing else
    try:
        verse = int(ayah)
        if (verse < 1) or (verse > 6236):
            raise IncorrectAyahArguments("Ayah must be inbetween 1 and 6236")
    except:
        _data = ayah.split(":")
        if len(_data) != 2:
            raise IncorrectAyahArguments(
                "Please enter your ayahs in the following format: 2:255 (For Surah Baqarah verse 255)"
            )
        _range = _data[1].split("-")
        if len(_range) != 1:
            if len(_range) != 2:
                raise IncorrectAyahArguments(
                    "Please enter your ayahs in the following format: 1:1-4 (For verses 1-4 of Surah Fatiha)"
                )
            else:
                try:
                    offset, limit = list(map(int, _range))
                except ValueError:
                    raise IncorrectAyahArguments("You may not use any words to define your ayah!") from ValueError
                if offset > limit:
                    offset = limit
                    limit = offset
                verse = "http://api.alquran.cloud/v1/surah/{0}/editions/{1}?offset={2}&limit={3}".format(_data[0],
                                                                                                         edition.value,
                                                                                                         offset - 1,
                                                                                                         limit)
        else:
            verse = f"{_data[0]}:{_data[1]}"
    if isinstance(verse, int) or check_format(verse):
        data = request(_URL.format('ayah', verse, edition.value)).json()
        return [data['data']['text']]
    else:
        data = request(verse).json()
        ayahs = data['data'][0]['ayahs']
        if not isinstance(ayahs, list):
            raise IncorrectAyahArguments(ayahs)
        else:
            to_return = list()
            for ayah in ayahs:
                to_return.append(ayah['text'])
        return to_return


def check_format(text: str) -> bool:
    return len(text.split(":")) == 2 and not text.startswith("http")
