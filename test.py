import quranpy

results = quranpy.Search("moses", edition=quranpy.Editions.yusufali, surah=quranpy.Surah(21, quranpy.Editions.yusufali))

nisa = quranpy.Surah(
    chapter=quranpy.Chapters.nisa,
    edition=quranpy.Editions.pickthall
)
print(nisa.translation)
print(results.verses)
print(quranpy.show_verses("12:1-4", quranpy.Editions.english_transliteration))
