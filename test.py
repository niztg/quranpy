import quranpy

results = quranpy.Search("moses", edition=quranpy.Editions.yusufali, surah=quranpy.Surah(21, quranpy.Editions.yusufali))

nisa = quranpy.Surah(
    chapter=quranpy.Chapters.nisa,
    edition=quranpy.Editions.pickthall
)
print(nisa.translation)
print(results.verses)
