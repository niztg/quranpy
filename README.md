# quranpy
Python Package to interact with the Glorious Qur'an!

This package uses the [Al Quran Cloud](https://alquran.cloud/) API to bring you verses and surahs of the Qur'an.

**Start by importing the package:**
```py
import quranpy
```

**Features**:

<h3>Get verses of the Qur'an on demand</h3>

```py
verses = quranpy.show_verses(
      ayah="112:2-4",
      edition=quranpy.Editions.sahih_international
)
print(verses)
# will show Surah Ikhlas verses 2, 3 and 4 with Sahih International translation
```

```py
['Allah, the Eternal Refuge.', 'He neither begets nor is born,', 'Nor is there to Him any equivalent."']
```

<hr>



<h3>Easy info on Surahs of the Qur'an</h3>

```py
al_lail = quranpy.Surah(
      chapter=quranpy.Chapters.layl,
      edition=quranpy.Editions.pickthall # will show the Pickthall translations 
)
print(str(al_lail))
print(al_lail.number)
print(al_lail.arabic_name)
print(al_lail.name)
print(al_lail.translation)
print(al_lail.period)
print(al_lail.show_verses("1-3"))
```

```
Surah Al-Lail - The Night
92
سورة الليل
Al-Lail
The Night
Meccan
[By the night enshrouding, And the day resplendent, And Him Who hath created male and female,]
```

<hr>

<h3>Search for terms which appear in the Qur'an</h3>
      
```py
results = quranpy.Search(
      term="Moses",
      edition=quranpy.Editions.yusufali,
      surah=quranpy.Chapters.anbiya
)
print(results)
print(results.verses)
```

```
2 count(s) of "Moses" in Surah Al-Anbiyaa (in this edition)
[In the past We granted to Moses and Aaron the criterion (for judgment), and a Light and a Message for those who would do right,-, Before this We wrote in the Psalms, after the Message (given to Moses): My servants the righteous, shall inherit the earth."]
```

For more information, [read the documentation.](https://www.youtube.com/watch?v=oHg5SJYRHA0)<br>
See [test.py](https://github.com/niztg/quranpy/blob/master/test.py) for more in depth examples and ways to use the lib.

Assalamwalaikum warahmatullahi wa barakatuhu!
