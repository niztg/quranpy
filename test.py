import quranpy

results = quranpy.Search("abraham", edition=quranpy.Editions.yusufali, surah=quranpy.Surah(21))

nisa = quranpy.Surah(
    chapter=quranpy.Chapters.nisa,
    edition=quranpy.Editions.pickthall
)
print(nisa.translation)
print(results)
