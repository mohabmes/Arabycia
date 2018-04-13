# buckwalter.py
# Provides functions for translation between the Buckwalter
# transliteration and Unicode Arabic.

import re

BUCK_UNI = {
    "'" : "ء",
    "|" : "آ",
    ">" : "أ",
    "O" : "أ",
    "&" : "ؤ",
    "W" : "ؤ",
    "<" : "إ",
    "I" : "إ",
    "}" : "ئ",
    "A" : "ا",
    "b" : "ب",
    "p" : "ة",
    "t" : "ت",
    "v" : "ث",
    "j" : "ج",
    "H" : "ح",
    "x" : "خ",
    "d" : "د",
    "*" : "ذ",
    "r" : "ر",
    "z" : "ز",
    "s" : "س",
    "$" : "ش",
    "S" : "ص",
    "D" : "ض",
    "T" : "ط",
    "Z" : "ظ",
    "E" : "ع",
    "g" : "غ",
    "_" : "ـ",
    "f" : "ف",
    "q" : "ق",
    "k" : "ك",
    "l" : "ل",
    "m" : "م",
    "n" : "ن",
    "h" : "ه",
    "w" : "و",
    "Y" : "ى",
    "y" : "ي",
    "F" : u"\u064b",
    "N" : u"\u064c",
    "K" : u"\u064d",
    "a" : u"\u064e",
    "u" : u"\u064f",
    "i" : u"\u0650",
    "~" : u"\u0651",
    "o" : u"\u0652",
    "`" : u"\u0670",
}
""" Maps ascii characters to the unicode characters """

# Now we create a reverse mapping.
# Note that the extra characters:
#   I (hamza-under-alif) → duplicates <
#   O (hamza-over-alif) → duplicates >
#   W (hamza-on-waw) → duplicates &
# must be removed, since these are duplicates that Buckwalter has
# proposed for XML compatibility. I'll just remove them for now.

##del BUCK_UNI['I']
##del BUCK_UNI['O']
##del BUCK_UNI['W']

UNI_BUCK = {value: key for key, value in BUCK_UNI.items()
        if key not in 'IOW'}
""" Maps unicode characters to ascii characters """

BUCK_UNI_TABLE = str.maketrans(BUCK_UNI)

def buck2uni(text):
    """ Convert string from Buckwalter transliteration to Unicode """
    return text.translate(BUCK_UNI_TABLE)

UNI_BUCK_TABLE = str.maketrans(UNI_BUCK)

def uni2buck(text):
    """ Convert string from Buckwalter transliteration to Unicode """
    return text.translate(UNI_BUCK_TABLE)
