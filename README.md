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
arabycia = Arabycia()
arabycia.set_raw_text(text)
arabycia.analyze()

```
##### Output
```

Sentence :
يستعيد الكاتب في هذه الرواية كيف تحولت من مدينة للانوار الي مدينة للاشباح
With Diacritics :
يَسْتَعِيد الكاتِب فِي هٰذِهِ الرِوايَة كَيْفَ تَحَوَّلْتُ مِن مَدِينَة لِلأَنْوار إِلَى مَدِينَة لِلأَشْباح
POS :
sotaEiyd/VERB_IMPERFECT kAtib/NOUN fiy/PREP h`*ihi/DEM_PRON_F riwAy/NOUN kayofa/REL_PRON taHaw~al/VERB_PERFECT min/PREP madiyn/NOUN >anowAr/NOUN <ilaY/PREP madiyn/NOUN >a$obAH/NOUN

Word  : 	يَسْتَعِيد | yasotaEiyd | {isotaEAd_1 
POS   : 	ya/IV3MS+ sotaEiyd/VERB_IMPERFECT  
Gloss : 	he/it recover;regain;reclaim 

Word  : 	هٰذِهِ | h`*ihi | h`*A_1 
POS   : 	h`*ihi/DEM_PRON_F  
Gloss : 	this/these 

Word  : 	لِلأَنْوار | lil>anowAr | nuwr_2 
POS   : 	li/PREP+Al/DET+ >anowAr/NOUN  
Gloss : 	to/for + the lights 

Word  : 	لِلأَشْباح | lil>a$obAH | $abaH_1 
POS   : 	li/PREP+Al/DET+ >a$obAH/NOUN  
Gloss : 	to/for + the specters;shapes 

Word  : 	الكاتِب | AlkAtib | kAtib_1 
POS   : 	Al/DET+ kAtib/NOUN  
Gloss : 	the writer;author 

Word  : 	فِي | fiy | fiy_1 
POS   : 	fiy/PREP  
Gloss : 	in 

Word  : 	الرِوايَة | AlriwAyap | riwAyap_1 
POS   : 	Al/DET+ riwAy/NOUN +ap/NSUFF_FEM_SG 
Gloss : 	the story;novel [fem.sg.]

Word  : 	كَيْفَ | kayofa | kayofa_1 
POS   : 	kayofa/REL_PRON  
Gloss : 	how 

Word  : 	تَحَوَّلْتُ | taHaw~alotu | taHaw~al_1 
POS   : 	taHaw~al/VERB_PERFECT +tu/PVSUFF_SUBJ:1S 
Gloss : 	be changed;be transformed I <verb>

Word  : 	مِن | min | min_1 
POS   : 	min/PREP  
Gloss : 	from 

Word  : 	مَدِينَة | madiynap | madiynap_1 
POS   : 	madiyn/NOUN +ap/NSUFF_FEM_SG 
Gloss : 	city [fem.sg.]

Word  : 	إِلَى | <ilaY | <ilaY_1 
POS   : 	<ilaY/PREP  
Gloss : 	to;towards 

Word  : 	مَدِينَة | madiynap | madiynap_1 
POS   : 	madiyn/NOUN +ap/NSUFF_FEM_SG 
Gloss : 	city [fem.sg.]

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
- Arabycia uses modified version of pyaramorph (rewritten for better data manipulation).
- Arabycia uses [Sinai-corpus: Arabic tagged corpus](https://github.com/mohabmes/Sinai-corpus).


## Requirement
- NLTK
