from requests import get as request
from islampy.editions import Editions
from islampy.exceptions import SurahNotFound
from typing import Optional

base_url = "http://api.alquran.cloud/v1/surah/{0}/editions/{1}"


class Surah:
    def __init__(
            self,
            chapter: int,
            edition: Editions
    ):
        data = request(base_url.format(chapter, edition.value)).json()
        if data.get('code') != 200:
            raise SurahNotFound(
                "%s is not a chapter number in the Qur'an. The number must be inbetween 1 and 114" % chapter)
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

    @property
    def verses(self):
        return list()

    def show_verse(
            self,
            verse: int,
            last: Optional[int] = None
    ):
        pass



