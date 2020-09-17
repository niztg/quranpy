import quranpy

results = quranpy.Search(
      term="Moses",
      surah=quranpy.Chapters.anbiyaa
)
print(results)
print(results.verses[0].position)
print("_____________________________________")
anfal = quranpy.Surah(
      quranpy.Chapters.anfal,
      quranpy.Editions.sahih_international
)

print("\n".join(anfal.show_str_verses("1-5")))
print("_____________________________________")
print("\n".join(list(map(str, anfal.show_verses("1-5")))))
