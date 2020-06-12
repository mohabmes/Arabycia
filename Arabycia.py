# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import nltk
import re
import pyaramorph
import SinaiCorpus.load as SinaiCorpusload

class Arabycia:

	# analyzer = None
	# stemmer = None
	# lemmatizer = None
	# segmenter = None
	#
	# raw_data = None
	# org_data = None
	# corpus = None
	# analyzed_data = []
	# full_analyzed_data = []
	# processed_data = []
	# ambig_words = []


	def __init__(self):
		self.raw_text = text
		self.analyzer = pyaramorph.Analyzer()
		self.stemmer = nltk.ISRIStemmer()
		self.lemmatizer = nltk.WordNetLemmatizer()

		self.analyze_text()
		self.find_ambiguity()
		self.generate_candidates()

		print(self.raw_text)
		print(self.diacritized_text)
		print(self.diacritized_text_pos)

		# for x in range(0, len(self.ambiguous_words)):
		# 	print(self.ambiguous_words[x])
		# 	for solution in self.candidates[x][0]['solution']:
		# 		print(solution)
		self.load_corpus("SinaiCorpus/src/Sinai-corpus.zip", 60)
		self.select_candidate()

		# self.print_result()


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
		stems = str([self.stemmer.stem(w) for w in self.tokenization(txt)])
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

	def pam_stem(self, str):
		"""
			Get all root candidates.
			[Before using compatibility Table to eliminate some]
			:param str: string : Word.
			:return: stems : array : all root candidates
		"""
		stems = []
		data = self.analyzer.analyze_text(str)[1]
		for i in data:
			stems.append(self.reverse_transliteration(i))
		return stems

	def analyze_text(self):
		"""
			apply some analysis to a text ('raw_data') using pyaramorph lib
			:return: sents : array : the analysis data
		"""
		if len(self.raw_text):
			self.full_analyzed_data = self.analyzer.analyze_text(self.raw_text)
			return self.full_analyzed_data

	# def extract_data(self):
	# 	"""
	# 		Extract some useful data from analyze_text() result
	# 		[ex. arabic word, transliteration, root, etc.] for each token from 'raw_data'
	# 		:return: analyzed_data : array
	# 	"""
	# 	data = self.analyze_text()
	# 	for i in range(0, len(data)):
	# 		tans = data[i][0]['transl']
	# 		word = data[i][0]['arabic']
	# 		root = self.stem(data[i][0]['arabic'])
	# 		possible_root = self.pam_stem(word)
	# 		rtrans = self.transliteration(root)
	# 		self.analyzed_data.append({'arabic': word, 'transl': tans, 'root': root, 'root_transl': rtrans, 'candidates': possible_root})


	# def search(self, key):
	# 	"""
	# 		Search for word that have the same root as 'key' (Text Search)
	# 		:param key: string : Search keyword.
	# 		:return: result: array : original words from the text with the same root.
	# 	"""
	# 	result = []
	# 	self.extract_data()
	# 	data = self.analyzed_data
	#
	# 	for i in range(0, len(data)):
	# 		if data[i]['root'] == key or key in data[i]['candidates']:
	# 			result.append(data[i]['arabic'])
	#
	# 	print("Result : ", set(result))
	# 	return set(result)

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
		for word in self.full_analyzed_data:
			if len(word['solution']) > 1:
				self.ambiguous_words.append(word['arabic'])

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
				print("-> ", words[PERV], words[NEXT])
				cand_index = ambiguous.index(words[NEXT])

				prob = 0
				cand_best = -1
				ocurrence_count_best = -1
				for solution in candidates[cand_index][0]['solution']:
					cand_pos = solution['pos'][1]
					current_cand_prob, ocurrence_count = self.prob(pos[PERV], cand_pos)
					print(current_cand_prob, " ", ocurrence_count)
					if current_cand_prob > prob or (current_cand_prob == prob and ocurrence_count > ocurrence_count_best):
						prob = current_cand_prob
						cand_best = solution
						ocurrence_count_best = ocurrence_count

				print("-->> ", cand_best )
				self.diacritized_text = self.diacritized_text.replace(words[NEXT], cand_best['word'][0])
				pos[i] = cand_best['pos'][1]
				self.diacritized_text_pos = " ".join(pos)
				print(self.diacritized_text)
				print(self.diacritized_text_pos)

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



	# def pos_split(self, pos):
	# 	"""
	# 		Used to split (preprocess) POS before printing it.
	# 		:param pos: string
	# 		:return:
	# 	"""
	# 	data = ''
	# 	disc = ''
	# 	for i in pos:
	# 		if i == '':
	# 			continue
	# 		else:
	# 			str = i.split('/')
	# 			if data != '':
	# 				data += ' + ' + self.reverse_transliteration(str[0]).replace('+', '')
	# 				disc += ' + ' + str[1]
	# 			else:
	# 				data += self.reverse_transliteration(str[0]).replace('+', '')
	# 				disc += str[1].replace('+', '')
	# 	return data, disc


	# def final_result(self):
	# 	"""
	# 		Prepare the final result
	# 		:return: list contain the final result
	# 	"""
	# 	result = []
	# 	sent = self.raw_data
	# 	sent = sent.split()
	# 	for itr in range(0, len(self.processed_data)):
	# 		for p in range(0, len(self.processed_data[itr]['solution'])):
	# 			if self.processed_data[itr]['solution'][p][0] in sent:
	# 				result.append([
	# 					self.processed_data[itr]['solution'][p],
	# 					self.processed_data[itr]['gloss'][p],
	# 					self.processed_data[itr]['pos'][p]
	# 				])
	# 	return result


	# def print_result(self):
	# 	"""
	# 		Reformat the output & print it.
	# 		:return:
	# 	"""
	# 	print('Sentence :')
	# 	print(self.org_data)
	# 	print('With Diacritics :')
	# 	print(self.raw_data)
	#
	# 	data = self.final_result()
	# 	unique_wd =[]
	# 	res = ''
	#
	# 	for i in data:
	# 		if i[0][0] not in unique_wd:
	# 			unique_wd.append(i[0][0])
	# 			Gloss = '| '
	# 			POS = '| '
	# 			trans = '\'' + i[0][1] + '\''
	#
	# 			gloss = []
	# 			pos = []
	#
	# 			for dup in data:
	# 				if dup[0][0] == i[0][0]:
	# 					if dup[1][1] not in gloss:
	# 						gloss.append(dup[1][1])
	# 						pos.append(i[2])
	#
	# 			for ii in range(0, len(gloss)):
	# 				Gloss += gloss[ii].replace(';', ' | ').replace('/', ' | ') + ' | '
	# 				POS = '| ' + self.pos_split(pos[ii])[1] + ' | '
	#
	# 			word = '\nWord  : \t\t' + '\'' + i[0][0] + '\''
	# 			word2 = '\nWord  : \t\t' + '\'' + self.pos_split(i[2])[0] + '\''
	# 			trans = '\ntrans : \t\t' + trans
	# 			Gloss = '\nGloss : \t\t' + Gloss
	# 			POS = '\nPOS   : \t\t' + POS
	# 			print(word, word2, trans, Gloss, POS)
	#
	# 			res += word + word2 + trans + Gloss + POS + "\n"
	# 	return self.raw_data, res


text = 'يستعيد الكاتب في هذه الرواية كيف تحولت من مدينة للانوار الي مدينة للاشباح'
# text_ = 'بسم الله الرحمن الرحيم'
arabycia = Arabycia()
arabycia.set_raw_text(text)
# arabycia.test()
# ara.search('رحم')
# ara.print_result()
