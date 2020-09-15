import quranpy

# print(quranpy.Search("abraham", edition=quranpy.Editions.yusufali, surah=quranpy.Surah(21)))
ikhlas = quranpy.Surah(
    chapter=quranpy.Chapters.ikhlas,
    edition=quranpy.Editions.sahih_international
)
print(ikhlas.verses)