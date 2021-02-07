# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import nltk
import re
import pyaramorph
import SinaiCorpus.load as SinaiCorpusload

class Arabycia:

	def __init__(self):
		self.analyzer = pyaramorph.Analyzer()
		self.stemmer = nltk.ISRIStemmer()
		self.lemmatizer = nltk.WordNetLemmatizer()
		self.segmenter = nltk.data.load("tokenizers/punkt/english.pickle")

	def analyze(self):
		self.analyze_text()
		self.find_ambiguity()
		self.generate_candidates()
		self.load_corpus("SinaiCorpus/src/Sinai-corpus.zip", 60)
		self.select_candidate()
		self.print_result()

	def tokenization(self, txt):
		"""
			tokenization a certain arabic text
			:param txt: string : arabic text
			:return: tokens : array : array contain Tokens
		"""
		tokens = nltk.word_tokenize(txt)
		return tokens

	def stemming(self, txt):
		"""
			Apply Arabic Stemming without a root dictionary, using nltk's ISRIStemmer.
			:param txt: string : arabic text
			:return: stems : array : array contains a stem for each word in the text
		"""
		stems = [self.stemmer.stem(w) for w in self.tokenization(txt)]
		return stems

	def lemmatization(self, txt):
		"""
			Lemmatize using WordNet's morphy function.
			Returns the input word unchanged if it cannot be found in WordNet.
			:param txt: string : arabic text
			:return: lemmas : array : array contains a Lemma for each word in the text.
		"""
		lemmas = str([self.lemmatizer.lemmatize(w) for w in self.tokenization(txt)])
		return lemmas

	def set_raw_text(self, text):
		self.raw_text = text

	def segmentation(self, txt):
		"""
			Apply NLTK Sentence segmentation.
			:param txt: string : arabic text
			:return: sents : array : array contains Sentences.
		"""
		sents = self.segmenter.tokenize(txt)
		return sents

	@staticmethod
	def transliteration(str):
		"""
			Buckwalter Word transliteration.
			:param str: string : arabic word
			:return: trans : string : Word transliteration.
		"""
		trans = pyaramorph.buckwalter.uni2buck(str)
		return trans

	@staticmethod
	def reverse_transliteration(str):
		"""
			convert Word transliteration to the original word.
			:param str: string : Word transliteration.
			:return: trans : string : original word
		"""
		trans = pyaramorph.buckwalter.buck2uni(str)
		return trans

	def stem(self, word):
		"""
			Get word stem (NLTK ISRIStemmer)
			:param word: string : Word.
			:return: stem : string : stem
		"""
		stem = str(self.stemmer.stem(word))
		return stem

	def analyze_text(self):
		"""
			apply some analysis to a text ('raw_data') using pyaramorph lib
			:return: sents : array : the analysis data
		"""
		if len(self.raw_text):
			self.full_analyzed_data = self.analyzer.analyze_text(self.raw_text)
			return self.full_analyzed_data

	def text_search(self, key):
		"""
			Search for word that have the same root as 'key' (Text Search)
			:param key: string : Search keyword.
			:return: result: array : original words from the text with the same root.
		"""
		result = []
		text = self.raw_text.split()

		for word in text:
			if key == self.stem(word):
				result.append(word)

		return list(set(result))

	def load_corpus(self, path, filenum = 50):
		"""
			Load all Sinai-Corpus content
			:param filename: path to the file
			:return:
		"""
		self.corpus = SinaiCorpusload.load_corpus(path, filenum)
		self.corpus = self.corpus.split('\n')
		return self.corpus

	def find_ambiguity(self):
		"""
			Find all the ambiguous words.
			(After text_analysis the word with one solution is considered unambiguous, otherwise it's ambiguous)
			:return:
		"""
		self.ambiguous_words = []
		for index in range(len(self.full_analyzed_data)):
			if len(self.full_analyzed_data[index]['solution']) > 1:
				self.ambiguous_words.append(self.full_analyzed_data[index]['arabic'])

		self.ambiguous_words = list(set(self.ambiguous_words))
		self.solve_unambiguity()

		return self.ambiguous_words

	def solve_unambiguity(self):
		"""
			Solve any unambiguous word, and add its diacritics.
			Note: After text_analysis the word with one solution is considered unambiguous, otherwise it's ambiguous)
			add diacritics for unambiguous words
			:return:
		"""
		self.analyzed_text_result = []
		self.diacritized_text = self.raw_text
		self.diacritized_text_pos = ""
		raw = self.raw_text

		for word in raw.split():
			if word not in self.ambiguous_words:
				for possible_word in self.full_analyzed_data:
					if possible_word['arabic'] == word:
						diacritized_word = possible_word['solution'][0]['word'][0]
						diacritized_word_pos = possible_word['solution'][0]['pos'][1]
						self.diacritized_text_pos += diacritized_word_pos + " "
						self.diacritized_text = self.diacritized_text.replace(word, diacritized_word)
						self.analyzed_text_result.append({'transl': possible_word['transl'],
														  'arabic': possible_word['arabic'],
														  'word': possible_word['solution'][0]['word'],
														  'pos': possible_word['solution'][0]['pos'],
														  'gloss': possible_word['solution'][0]['gloss']
														  })
			else:
				self.diacritized_text_pos += "? "
		return self.diacritized_text

	def generate_candidates(self):
		"""
			foreach ambiguous word find all unambiguous candidates that can be solution.
			[one to be selected later]
			:return: all candidates
		"""
		candidates = []
		for word in self.ambiguous_words:
			temp = []
			for possible_word in self.full_analyzed_data:
				if possible_word['arabic'] == word:
					if possible_word not in temp: temp.append(possible_word)
			candidates.append(temp)
		self.candidates = candidates
		return self.candidates

	def find_index(self, word):
		text = self.raw_text.split()
		return text.index(word)

	def select_candidate(self):
		"""
			Select the best candidate.
			Replace the best candidate with the original ambiguous word.
			:return:
		"""
		candidates = self.candidates
		ambiguous = self.ambiguous_words
		words = self.raw_text.split()
		pos = self.diacritized_text_pos.split()

		for i in range(0,len(words)):
			if pos[i] == "?" and pos[i-1] != "?" and (i-1)>=0:
				NEXT = self.find_index(words[i])
				PERV = NEXT - 1
				cand_index = ambiguous.index(words[NEXT])
				prob = 0
				cand_best = -1
				ocurrence_count_best = -1
				transl = candidates[cand_index][0]['transl']
				arabic = candidates[cand_index][0]['arabic']
				for solution in candidates[cand_index][0]['solution']:
					cand_pos = solution['pos'][1]
					current_cand_prob, ocurrence_count = self.prob(pos[PERV], cand_pos)
					if current_cand_prob > prob or (current_cand_prob == prob and ocurrence_count > ocurrence_count_best):
						prob = current_cand_prob
						cand_best = solution
						ocurrence_count_best = ocurrence_count
				self.diacritized_text = self.diacritized_text.replace(words[NEXT], cand_best['word'][0])
				pos[i] = cand_best['pos'][1]
				self.diacritized_text_pos = " ".join(pos)

				self.analyzed_text_result.append({'transl': transl,
												  'arabic': arabic,
												  'word': cand_best['word'],
												  'pos': cand_best['pos'],
												  'gloss': cand_best['gloss'] })

		return self.analyzed_text_result

	def search(self, text, key):
		return [sent for sent in text if re.search(key, sent)]

	def get_subsentences(self, sents, key):
		subsentences = []
		for sent in sents:
			words = sent.split()
			for i in range(0, len(words)):
				if key in words[i] and i >= 0 and i < len(words) - 1:
					subsentences.append(words[i + 1])
		return subsentences

	def split(self, str, returnval="pos"):
		str = str.split('/')
		if returnval is "pos": return str[1]
		else: return str[0]

	def prob(self, word1, word2):
		"""
			compute the probability of the given two words.
			prob = count(w1 | w2) / count(w1)
			:param w1:
			:param w2:
			:return:
		"""
		w1 = self.split(word1, "pos")
		w2 = self.split(word2, "pos")
		count_word2 = len(self.search(self.corpus, self.split(word2, "word")))
		filter = self.search(self.corpus, w1)
		count_w1 = self.get_subsentences(filter, w1)
		count_w1_w2 = self.search(count_w1, w2)


		prob = len(count_w1_w2) / float(len(count_w1))
		if w1 == w2: prob /= 2

		return prob, count_word2

	def print_result(self):
		"""
			Reformat the output & print it.
			:return:
		"""
		print('Sentence :')
		print(self.raw_text)
		print('With Diacritics :')
		print(self.diacritized_text)
		print('POS :')
		print(self.diacritized_text_pos)

		for result in self.analyzed_text_result:
			word  = '\nWord  : \t' + '\t'.join(filter(None, result['word']))
			root  = '\nRoot  : \t' + self.stemming(result['word'][0])[0]
			gloss = '\nGloss : \t' + result['gloss'][1]
			pos   = '\nPOS   : \t' + '\t'.join(filter(None, result['pos']))
			print(word, root, pos, gloss)

		return self.analyzed_text_result


arabycia = Arabycia()

text = 'يستعيد الكاتب في هذه الرواية كيف تحولت من مدينة للانوار الي مدينة للاشباح'
arabycia.set_raw_text(text)
arabycia.analyze()

text = 'يستجمع المؤرخ أفكاره'
arabycia.set_raw_text(text)
arabycia.analyze()
search_result = arabycia.text_search("جمع")
print(search_result)

