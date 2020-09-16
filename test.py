import quranpy

results = quranpy.Search(term="Moses", edition=quranpy.Editions.yusufali, surah=quranpy.Chapters.anbiya)
print(results)
print(results.verses)


