# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import nltk
import re
import pyaramorph


class Arabycia:

	analyzer = None
	stemmer = None
	lemmatizer = None
	segmenter = None

	raw_data = None
	org_data = None
	corpus = ''
	analyzed_data = []
	full_analyzed_data = []
	processed_data = []
	ambig_words = []


	def __init__(self, raw_data=None):
		self.analyzer = pyaramorph.Analyzer()
		self.stemmer = nltk.ISRIStemmer()
		self.lemmatizer = nltk.WordNetLemmatizer()
		self.segmenter = nltk.data.load("tokenizers/punkt/english.pickle")

		if raw_data is not None:
			self.raw_data = raw_data
			self.org_data = raw_data

		self.analyze_text()
		self.ambig()
		self.load_corpus('4.txt')
		self.select_cand()
		# self.print_result()


	def tokenization(self, txt):
		"""
			tokenization a certain arabic text

			Parameters
			----------
			txt : string
				arabic text

			Returns
			----------
			tokens : array
				array contain Tokens
		"""
		tokens = nltk.word_tokenize(txt)
		return tokens


	def stemming(self, txt):
		"""
			Apply Arabic Stemming without a root dictionary, using nltk's ISRIStemmer.

			Parameters
			----------
			txt : string
				arabic text

			Returns
			----------
			stems : array
				array contains a stem for each word in the text
		"""
		stems = str([self.stemmer.stem(w) for w in self.tokenization(txt)])
		return stems


	def lemmatization(self, txt):
		"""
			Lemmatize using WordNet's morphy function.
			Returns the input word unchanged if it cannot be found in WordNet.

			Parameters
			----------
			txt : string
				arabic text

			Returns
			----------
			lemmas : array
				array contains a Lemma for each word in the text.
		"""
		lemmas = str([self.lemmatizer.lemmatize(w) for w in self.tokenization(txt)])
		return lemmas


	def segmentation(self, txt):
		"""
			Apply NLTK Sentence segmentation.

			Parameters
			----------
			txt : string
				arabic text

			Returns
			----------
			sents : array
				array contains Sentences.
		"""
		sents = self.segmenter.tokenize(txt)
		return sents


	@staticmethod
	def transliteration(str):
		"""
			Buckwalter Word transliteration.

			Parameters
			----------
			txt : string
				arabic word

			Returns
			----------
			trans : string
				Word transliteration.
		"""
		trans = pyaramorph.buckwalter.uni2buck(str)
		return trans


	@staticmethod
	def reverse_transliteration(str):
		"""
			convert Word transliteration to the original word.

			Parameters
			----------
			txt : string
				Word transliteration.

			Returns
			----------
			trans : string
				original word
		"""
		trans = pyaramorph.buckwalter.buck2uni(str)
		return trans


	def analyze_text(self):
		"""
			apply some analysis to a text ('raw_data') using pyaramorph lib

			Returns
			----------
			sents : array
				the analysis data
		"""
		data = self.analyzer.analyze_text(self.raw_data)
		self.full_analyzed_data = data[0]
		self.data_process()
		return self.full_analyzed_data


	def extract_data(self):
		"""
			Extract some useful data from analyze_text() result
			[ex. arabic word, transliteration, root, etc.] for each token from 'raw_data'

			Returns
			----------
			analyzed_data : array
		"""
		data = self.analyze_text()
		for i in range(0, len(data)):
			tans = data[i][0]['transl']
			word = data[i][0]['arabic']
			root = self.stem(data[i][0]['arabic'])
			possible_root = self.pam_stem(word)
			rtrans = self.transliteration(root)
			self.analyzed_data.append({'arabic': word, 'transl': tans, 'root': root, 'root_transl': rtrans, 'candidates': possible_root})
		# return self.analyzed_data


	def stem(self, word):
		"""
			Get word stem (NLTK ISRIStemmer)

			Parameters
			----------
			str : string
				Word.

			Returns
			----------
			stem : string
				stem
		"""
		stem = str(self.stemmer.stem(word))
		return stem


	def pam_stem(self, str):
		"""
			Get all root candidates.
			[Before using compatibility Table to eliminate some]

			Parameters
			----------
			str : string
				Word.

			Returns
			----------
			stems : array
				all root candidates
		"""
		stems = []
		data = self.analyzer.analyze_text(str)[1]
		for i in data:
			stems.append(self.reverse_transliteration(i))
		return stems


	def search(self, key):
		"""
			Search for word that have the same root as 'key' (Text Search)

			Parameters
			----------
			key : string
				Search keyword.

			Returns
			----------
			result : array
				original words from the text with the same root.
		"""
		result = []
		self.extract_data()
		# key = key
		data = self.analyzed_data

		for i in range(0, len(data)):
			if data[i]['root'] == key or key in data[i]['candidates']:
				result.append(data[i]['arabic'])

		print("Result : ", set(result))
		return set(result)


	def data_process(self):
		"""
			process the result data from pyaramorph & put it in organized way
		"""
		data = self.full_analyzed_data
		all = []
		for ele in range(0, len(data)):
			solution = []
			pos = []
			gloss = []
			eg = ''
			ar = ''
			for i in range(0, len(data[ele])):
				for k, v in data[ele][i].items():
					if k == 'transl': eg = v
					if k == 'arabic': ar = v
					if k == 'solution': solution.append(v)
					if k == 'pos': pos.append(v)
					if k == 'gloss': gloss.append(v)
			temp = {'transl': eg, 'arabic': ar, 'solution': solution, 'pos': pos, 'gloss': gloss}
			all.append(temp)
		self.processed_data = all


	def load_corpus(self, filename):
		print('Reading ' + filename)
		f = open(filename, 'r', encoding='utf-8')
		content = f.read()
		# segm_sent = self.segmenter.tokenize(content)
		# self.corpus = segm_sent
		self.corpus = content


	def replace_sub(self, text, str, sub):
		nw = ''
		for w in text.split():
			if w == str:
				nw += sub + " "
			else:
				nw += w + " "
		return nw


	def ambig(self):
		for w in self.processed_data:
			temp = []
			# print(w)
			for sol in w['solution']:
				temp.append(sol[2])
				# print(sol)
			if len(set(temp))>1:
				self.ambig_words.append(w['arabic'])
				# print(w['arabic'])

		###### Tashkil ######
		raw = self.raw_data
		temp = raw
		# print(raw)
		for w in raw.split():
			if w not in self.ambig_words:
				for t in self.processed_data:
					if t['arabic'] == w:
						for sol in t['solution'][0]:
							self.raw_data = self.replace_sub(self.raw_data, w, sol)
							# print(sol, w)
							break


	def find_word(self, key):
		valid_sent = [w for w in self.corpus if re.search(key, w)]
		return valid_sent


	def generate_cand(self):
		cand = []

		for w in self.ambig_words:
			temp = []
			for itr in self.processed_data:
				if itr['arabic'] == w:
					# print(itr['solution'])
					for sw in itr['solution']:
						# print(sw[0])

						if sw[0] in temp:
							continue
						else:
							temp.append(sw[0])
			cand.append(temp)
		return cand


	def select_cand(self):
		cands = self.generate_cand()
		ambgs = self.ambig_words
		sent = self.raw_data
		spsent = sent.split()

		# Generate the subsent
		for i in range(0, len(self.ambig_words)):
			best_p = -1
			best_word = ''
			for ii in range(0, len(cands[i])):
				subsent = ''
				id = [spsent.index(w) for w in spsent if re.search(ambgs[i], w)][0]
				subsent = spsent[id-1] + " " + cands[i][ii]
				p = self.bigram(subsent)

				if p > best_p:
					best_p = p
					best_word = cands[i][ii]

			self.raw_data = self.replace_sub(self.raw_data, ambgs[i], best_word)


	def prob(self, w1, w2):
		# prob = count(w1 | w2) / count(w1)
		key = str(w1) + str(w2)
		count_w1_w2 = len([w for w in self.corpus.replace(' ', '').split() if re.search(key, w)])
		key = str(w1)
		count_w1 = len([w for w in self.corpus.replace(' ', '').split() if re.search(key, w)])
		p = count_w1_w2 / float(count_w1 + 1)
		if p == 0:
			return count_w1 /1000
		return p


	def bigram(self, sents):
		words = sents.split()
		p = 1
		for i in range(0, len(words) - 1):
			p *= self.prob(words[i], words[i + 1])
		return p


	def pos_split(self, pos):
		data = ''
		disc = ''
		for i in pos:
			if i == '':
				continue
			else:
				str = i.split('/')
				if data != '':
					data += ' + ' + self.reverse_transliteration(str[0]).replace('+', '')
					disc += ' + ' + str[1]
				else:
					data += self.reverse_transliteration(str[0]).replace('+', '')
					disc += str[1].replace('+', '')

		return data + '  ->  ('+disc+')'


	def final_result(self):
		result = []
		sent = self.raw_data
		sent = sent.split()

		for itr in range(0, len(self.processed_data)):
			# print(self.processed_data[itr]['transl'])
			for p in range(0, len(self.processed_data[itr]['solution'])):

				if self.processed_data[itr]['solution'][p][0] in sent:
					result.append([
						self.processed_data[itr]['solution'][p],
						self.processed_data[itr]['gloss'][p],
						self.processed_data[itr]['pos'][p]
					])
				break
		return result


	def print_result(self):
		print('Sentence :')
		print(self.org_data)
		print('With Diacritics :')
		print(self.raw_data)

		data = self.final_result()

		for i in data:
			print('\nWord : ' + i[0][0] + '  (\'' + i[0][1] + '\')')
			print('Gloss : ' + i[1][1].replace(';', '/'))
			print('POS   : ' + self.pos_split(i[2]))



text = 'يستعيد الكاتب في هذه الرواية كيف تحولت من مدينة للانوار الي مدينة للاشباح'

ara = Arabycia(text)
ara.print_result()