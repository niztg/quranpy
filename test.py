import quranpy

results = quranpy.Search(
      term="Moses",
      surah=quranpy.Chapters.anbiyaa
)
print(results)
print(results.verses[0].position)
print("_____________________________________")
Anfal = quranpy.Surah(
      quranpy.Chapters.anfal,
      quranpy.Editions.sahih_international
)

print("\n".join(Anfal.show_str_verses("1-5")))
print("_____________________________________")
print("\n".join(list(map(str, Anfal.show_verses("1-5")))))
