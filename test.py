"""
Copy and paste this file into your IDE to get a feel for the Lib.
Play around with it!
"""

import quranpy

ama = quranpy.Juz(30)
print(ama)

# with quranpy.EditionInfo(quranpy.Editions.korean) as e:
#     print(e.verse(262))
# print(e)
#
# print([v.position for v in quranpy.Search("abraham")])
# print("_____________________________________")
# Anfal = quranpy.Surah(
#     chapter=quranpy.Chapters.anfal,
#     edition=quranpy.Editions.sahih_international
# )
#
# print("\n".join(Anfal.show_str_verses("1-5")))
# print("_____________________________________")
# print("\n".join(list(map(str, Anfal.show_verses("1-5")))))
# print("_____________________________________")
# print(quranpy.__author__)
# print("_____________________________________")
# print(quranpy.Surah(29).show_str_verses("28-29"))
#
#
# def get_v(ayah, edition=quranpy.Editions.sahih_international):
#     """Example function"""
#     if isinstance(ayah, int) or ayah.isdigit():
#         try:
#             verse = quranpy.Verse(ayah, edition)
#             surah = verse.surah
#             return \
#                 f"""
# {surah.arabic_name} | {surah.__str__()}
#
# {verse.position}
# {verse.text}
#
# {surah.period}
# """
#         except Exception as error:
#             raise error
#     else:
#         try:
#             surah, verses = ayah.split(":")
#         except ValueError:
#             raise quranpy.IncorrectAyahArguments(
#                 "Please enter your verses in the following format: 2:225 (For Surah Baqarah verse 255)") from ValueError
#         try:
#             surah = int(surah)
#         except:
#             raise quranpy.IncorrectAyahArguments("You may not use any words to define your verse")
#         finally:
#             surah = quranpy.Surah(int(surah))
#             _verses = list(surah.show_str_verses(verses))
#             msg = f"{surah.arabic_name} | {surah.__str__()}"
#             split = verses.split("-")
#             if len(split) == 1:
#                 msg += f"\n\n{ayah}\n{_verses[0]}"
#                 return msg
#             else:
#                 _range = list(range(int(split[0]), int(split[1]) + 1))
#                 for number, verse in zip(_range, _verses):
#                     msg += f"\n\n{surah.number}:{number}\n{verse}"
#                 msg += f"\n\n{surah.period}"
#                 return msg
#
#
# print(quranpy.Surah(5).get_str_verses('72', '110-120'))
#
# if __name__ == '__main__':
#     print(get_v("5:72", quranpy.Editions.kids))
#
# print(quranpy.Ayah(1))