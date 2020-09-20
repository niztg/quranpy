import quranpy

# results = quranpy.Search(
#       term="Moses",
#       surah=quranpy.Chapters.anbiyaa,
#       edition=quranpy.Editions.yusufali
# )
# print(results)
# print(results.verses[0].position)
# print("_____________________________________")
# Anfal = quranpy.Surah(
#       chapter=quranpy.Chapters.anfal,
#       edition=quranpy.Editions.sahih_international
# )
#
# print("\n".join(Anfal.show_str_verses("1-5")))
# print("_____________________________________")
# print("\n".join(list(map(str, Anfal.show_verses("1-5")))))
# print("_____________________________________")
# print(quranpy.__author__)
# print(quranpy.Surah(29).show_verses("28-29"))
# print("_____________________________________")
# print(quranpy.Search(
#       "Jesus"
# ))
____________________________________________________ = "just a comment"
# msg = input("Enter verse you want: ")
# try:
#       surah, verse = msg.split(":")
# except:
#       print(str(quranpy.IncorrectAyahArguments()))
# try:
#       all_verses = quranpy.Surah(surah).show_str_verses(verse)
# except Exception as error:
#       print(error)
al_fatihah = quranpy.Surah(
      quranpy.Chapters.fatiha
)
al_ikhlas = quranpy.Surah(
      quranpy.Chapters.ikhlas
)
print(al_fatihah.show_str_verses("2-6"))
print(al_ikhlas.show_str_verses("2-4"))
print(al_ikhlas.show_str_verses(2))

