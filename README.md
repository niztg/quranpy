# quranpy
Python Package to interact with the Glorious Qur'an!

This package uses the [Al Quran Cloud](https://alquran.cloud/) API to bring you verses and surahs of the Qur'an.


**Start by importing the package:**
```py
import quranpy
```

You can then create an instance of a Surah, Verse, Page, Juz or Search.

*Example:*
```py
al_fatiha = quranpy.Surah(
    chapter=quranpy.Chapters.fatiha, 
    edition=quranpy.Editions.sahih_international
)
print(al_fatiha)
```

*Returns:*
```py
Surah Al-Faatiha - The Opening
```

```py
al_ikhlas = quranpy.Surah(112, edition=quranpy.Editions.sahih_international)
verses = al_ikhlas.show_verses(1, 4) # Will show verses 1-4. If you only want one verse, the second argument is not necessary
print("\n".join(map(str, verses)))
```

*Returns:*
```
Say, "He is Allah, [who is] One,
Allah, the Eternal Refuge.
He neither begets nor is born,
Nor is there to Him any equivalent."
```
<hr>

```py
ayatul_kursi = quranpy.Verse("2:255") # Verse may also take an integer as it's first argument. `Verse(262)` would accomplish the same thing here.
print(ayatul_kursi)
```

*Returns:*
```
Allah! There is no deity save Him, the Alive, the Eternal. Neither slumber nor sleep overtaketh Him. Unto Him belongeth whatsoever is in the heavens and whatsoever is in the earth. Who is he that intercedeth with Him save by His leave? He knoweth that which is in front of them and that which is behind them, while they encompass nothing of His knowledge save what He will. His throne includeth the heavens and the earth, and He is never weary of preserving them. He is the Sublime, the Tremendous.
```

**Exceptions:**
```py
while True:
    msg = input("Enter a verse you want to see: ")
    try:
        verse = quranpy.Verse(msg, ediition=quranpy.Editions.pickthall)
    except quranpy.IncorrectAyahArguments as error:
        print(error)
        continue
    print(verse)
```

*Returns:*
```
Enter a verse you want to see: not a real verse
Please specify an Ayah number (1 to 6236) or a reference in the format Surah:Ayat (2:255).
Enter a verse you want to see: 
```

**Editions:**
There are 137 editions of Qur'an which can all be found [here](https://github.com/niztg/quranpy/blob/master/quranpy/editions.py)

Usage:
```py
quranpy.Verse("93:7", edition=quranpy.Editions.edition) # `edition` here is being replaced
```

*Notable Editions:*
- sahih_international (Default)
- yusufali
- pickthall
- korean
- japanese
- thai
- bengali
- jalalayn
- tamil
- english_transliteration
