# quranpy
Python Package to interact with the Glorious Qur'an!

This package uses the [Al Quran Cloud](https://alquran.cloud/) API to bring you verses and surahs of the Qur'an.


**Start by importing the package:**
```py
import quranpy
```

You can then create an instance of a Surah or Verse.

*Example:*
```py
al_fatiha = quranpy.Surah(1, edition=quranpy.Editions.sahih_international)
print(al_fatiha)
```

*Returns:*
```py
Surah Al-Faatiha - The Opening
```

```py
al_ikhlas = quranpy.Surah(112) # Sahih International is the default edition
verses = al_ikhlas.show_verses(1, 4) # Will show verses 1-4
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
