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
      "Jesus"
))
print(quranpy.Surah(29).show_str_verses("28-29"))


