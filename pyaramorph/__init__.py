# pyaramorph, an Arabic morphological analyzer
# Copyright © 2005 Alexander Lee
# Ported to Python from Tim Buckwalter's aramorph.pl.

import sys
import re
from collections import namedtuple
from . import buckwalter
from . import util

Segment = namedtuple('Segment', 'prefix stem suffix')

# Data file paths
TABLE_AB = "tableAB"
TABLE_BC = "tableBC"
TABLE_AC = "tableAC"
DICT_PREFIXES = "dictPrefixes"
DICT_STEMS = "dictStems"
DICT_SUFFIXES = "dictSuffixes"

def _tokenize(text):
    """ Extract all Arabic words from input and ignore everything
    else """
    tokens = re.split('[^\u0621-\u0652\u0670-\u0671]+', text)
        # include all strictly Arabic consonants and diacritics --
        # perhaps include other letters at a later time.
    return tokens

def _clean_arabic(text):
    """ Remove any تَطوِيل and vowels/diacritics """
    return re.sub('[\u0640\u064b-\u0652\u0670]', '', text)
    # FIXME do something about \u0671, ALIF WASLA ?

class Analyzer:

    def __init__(self):
        self.tableAB = util.load_table(TABLE_AB)
        self.tableBC = util.load_table(TABLE_BC)
        self.tableAC = util.load_table(TABLE_AC)

        self.prefixes = util.load_dict(DICT_PREFIXES)
        self.stems = util.load_dict(DICT_STEMS)
        self.suffixes = util.load_dict(DICT_SUFFIXES)

    def analyze_text(self, text):
        """Generate analyses for each word in the given Arabic text."""

        all_results = []
        tokens = _tokenize(text.strip())

        for token in tokens:
            if token is not "":
                word_results = {}
                token = _clean_arabic(token)
                buckword = buckwalter.uni2buck(token)
                analyses, possible = self.analyze_word(buckword)
                if len(analyses) >= 0:
                    word_results.update(transl=buckword, arabic=token, solution=analyses)

                all_results.append(word_results)
        return all_results

    def analyze_word(self, word):
        """Return all possible analyses for the given word"""
        analyses = []
        segments = self._build_segments(word)
        possible = []

        for prefix, stem, suffix in segments:
            possible.append(stem)
            analyses.extend(self._check_segment(prefix, stem, suffix))
        return analyses, possible

    def _check_segment(self, prefix, stem, suffix):
        """ See if the prefix, stem, and suffix are compatible """
        analyses = []

        # Loop through the possible prefix entries
        for pre_entry in self.prefixes[prefix]:
            (voc_a, cat_a, gloss_a, pos_a) = pre_entry[1:5]

            # Loop through the possible stem entries
            for stem_entry in self.stems[stem]:
                (voc_b, cat_b, gloss_b, pos_b, lemmaID) = stem_entry[1:]

                # Check the prefix + stem pair
                pairAB = "%s %s" % (cat_a, cat_b)
                if not pairAB in self.tableAB: continue

                # Loop through the possible suffix entries
                for suf_entry in self.suffixes[suffix]:
                    (voc_c, cat_c, gloss_c, pos_c) = suf_entry[1:5]

                    # Check the prefix + suffix pair
                    pairAC = "%s %s" % (cat_a, cat_c)
                    if not pairAC in self.tableAC: continue

                    # Check the stem + suffix pair
                    pairBC = "%s %s" % (cat_b, cat_c)
                    if not pairBC in self.tableBC: continue

                    # Ok, it passed!
                    buckvoc = "%s%s%s" % (voc_a, voc_b, voc_c)
                    univoc = buckwalter.buck2uni(buckvoc)
                    # if gloss_a == '': gloss_a = '___'
                    # if gloss_c == '': gloss_c = '___'
                    '''analyses.append(
                        "    solution: (%s %s) [%s]\n"
                        "         pos: %s%s%s\n"
                        "       gloss: %s + %s + %s\n" % \
                        (univoc, buckvoc, lemmaID, \
                        pos_a, pos_b, pos_c, \
                        gloss_a, gloss_b, gloss_c))
					'''
                    analyses.append({
                        "word": [univoc, buckvoc, lemmaID], \
                        "pos": [pos_a, pos_b, pos_c], \
                        "gloss": [gloss_a, gloss_b,gloss_c]
                    })

        return analyses

    def _valid_segment(self, segment):
        """Determines whether the segment is possible."""
        return segment.prefix in self.prefixes \
                and segment.stem in self.stems \
                and segment.suffix in self.suffixes

    def _build_segments(self, word):
        """Returns all possible segmentations of the given word."""
        segments = []

        for stem_idx, suf_idx in util.segment_indexes(len(word)):
            prefix = word[0:stem_idx]
            stem = word[stem_idx:suf_idx]
            suffix = word[suf_idx:]

            segment = Segment(prefix, stem, suffix)
            if self._valid_segment(segment):
                segments.append(segment)

        return segments