# Arabycia
Arabic NLP tool Built using NLTK, Pyaramorph, and Tashkeela to perform:
  1. Transliteration
  2. Sentence diacritization
  3. Text Search
  2. POS tagging
  3. Translation

## Usage
##### Input
```

text = 'يستعيد الكاتب في هذه الرواية كيف تحولت من مدينة للانوار الي مدينة للاشباح'
 
ara = Arabycia(text)
ara.print_result() 

```
##### Output
```

Sentence :
يستعيد الكاتب في هذه الرواية كيف تحولت من مدينة للانوار الي مدينة للاشباح
With Diacritics :
يَسْتَعِيد الكاتِب فِي هٰذِهِ الرِوايَة كَيْفَ تَحَوَّلْتُ مِن مَدِينَة لِلأَنْوار إِلَيَّ مَدِينَة لِلأَشْباح 

Word  : 'يَسْتَعِيد'
trans : 'yasotaEiyd'
Gloss : | recover | regain | reclaim | 
POS   : | IV3MS + VERB_IMPERFECT | 

Word  : 'الكاتِب'
trans : 'AlkAtib'
Gloss : | writer | author | clerk | writing | 
POS   : | DET + NOUN | 

Word  : 'فِي'
trans : 'fiy'
Gloss : | in | V. | 
POS   : | PREP | 

Word  : 'هٰذِهِ'
trans : 'h`*ihi'
Gloss : | this | these | 
POS   : | DEM_PRON_F | 

Word  : 'الرِوايَة'
trans : 'AlriwAyap'
Gloss : | story | novel | report | account | 
POS   : | DET + NOUN + NSUFF_FEM_SG | 

Word  : 'كَيْفَ'
trans : 'kayofa'
Gloss : | how | 
POS   : | REL_PRON | 

Word  : 'تَحَوَّلْتُ'
trans : 'taHaw~alotu'
Gloss : | be changed | be transformed | 
POS   : | VERB_PERFECT + PVSUFF_SUBJ:1S | 

Word  : 'مِن'
trans : 'min'
Gloss : | from | 
POS   : | PREP | 

Word  : 'مَدِينَة'
trans : 'madiynap'
Gloss : | owing | obligated | debtor | city | Medina | 
POS   : | ADJ + NSUFF_FEM_SG | 

Word  : 'لِلأَنْوار'
trans : 'lil>anowAr'
Gloss : | lights | 
POS   : | PREPAl + NOUN | 

Word  : 'إِلَيَّ'
trans : '<ilay~a'
Gloss : | to | towards | 
POS   : | PREP + PRON_1S | 

Word  : 'لِلأَشْباح'
trans : 'lil>a$obAH'
Gloss : | specters | shapes | 
POS   : | PREPAl + NOUN | 

```

##### Input
```

text = 'يستعيد الكاتب في هذه الرواية كيف تحولت من مدينة للانوار الي مدينة للاشباح'
ara = Arabycia(text)
ara.search('حول')

text = 'بسم الله الرحمن الرحيم'
ara = Arabycia(text)
ara.search('رحم')

```

##### Output
```

Result :  {'تحولت'}
Result :  {'الرحيم', 'الرحمن'}

```

## Notes
- Arabycia uses modified version of pyaramorph.
- **Add Dict & table files from [pyaramorph](https://bitbucket.org/alexlee/pyaramorph) (ex. dictPrefixes, dictStems, tableAB, etc) to pyaramorph Directory.**
- Arabycia uses [Tashkeela: Arabic diacritization corpus](https://sourceforge.net/projects/tashkeela/).

## Todo
- The code is messy, it needs a bit organization.
- Need Enhancement to obtain high accuracy.

## Requirement
- NTLK
- Tashkeela
