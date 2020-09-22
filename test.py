"""
Copy and paste this file into your IDE to get a feel for the Lib.
Play around with it!
"""

import quranpy

results = quranpy.Search(
    term="Moses",
    surah=quranpy.Chapters.anbiyaa,
    edition=quranpy.Editions.yusufali
)
print(results)
print(results.verses[0].position)
print("_____________________________________")
Anfal = quranpy.Surah(
    chapter=quranpy.Chapters.anfal,
    edition=quranpy.Editions.sahih_international
)

print("\n".join(Anfal.show_str_verses("1-5")))
print("_____________________________________")
print("\n".join(list(map(str, Anfal.show_verses("1-5")))))
print("_____________________________________")
print(quranpy.__author__)
print("_____________________________________")
print(quranpy.Search(
    "Messiah"
))
print(quranpy.Surah(29).show_str_verses("28-29"))


def get_v(ayah, edition=quranpy.Editions.sahih_international):
    """Example function"""
    if isinstance(ayah, int) or ayah.isdigit():
        try:
            verse = quranpy.Verse(ayah, edition)
            surah = verse.surah
            return \
f"""
{surah.arabic_name} | {surah.__str__()}

{verse.position}
{verse.text}

{surah.period}
"""
        except Exception as error:
            raise error
    else:
        try:
            surah, verses = ayah.split(":")
        except ValueError:
            raise quranpy.IncorrectAyahArguments(
                "Please enter your verses in the following format: 2:225 (For Surah Baqarah verse 255)") from ValueError
        try:
            surah = int(surah)
        except:
            raise quranpy.IncorrectAyahArguments("You may not use any words to define your verse")
        try:
            surah = quranpy.Surah(int(surah))
            _verses = list(surah.show_str_verses(verses))
            msg = f"{surah.arabic_name} | {surah.__str__()}"
            split = verses.split("-")
            if len(split) == 1:
                  msg += f"\n\n{ayah}\n{_verses[0]}"
                  return msg
            else:
                _range = list(range(int(split[0]), int(split[1])+1))
                for number, verse in zip(_range, _verses):
                      msg += f"\n\n{surah.number}:{number}\n{verse}"
                msg += f"\n\n{surah.period}"
                return msg

        except Exception as error:
            raise error

if __name__ == '__main__':
    print(get_v("1:1-7"))