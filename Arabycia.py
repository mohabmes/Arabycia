from __future__ import unicode_literals
import nltk
import pyaramorph


class Arabica:

	analyzer = None
	stemmer = None
	lemmatizer = None
	segmenter = None

	raw_data = None
	analyzed_data = []
	full_analyzed_data = []

	def __init__(self, raw_data=None):
		self.analyzer = pyaramorph.Analyzer()
		self.stemmer = nltk.ISRIStemmer()
		self.lemmatizer = nltk.WordNetLemmatizer()
		self.segmenter = nltk.data.load("tokenizers/punkt/english.pickle")

		if raw_data is not None:
			self.raw_data = raw_data


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
		return data


	def extract_data(self):
		"""
			Extract some useful data from analyze_text() result
			[ex. arabic word, transliteration, root, etc.] for each token from 'raw_data'

			Returns
			----------
			analyzed_data : array
		"""
		data, _ = self.analyze_text()
		for i in range(0, len(data)):
			tans = data[i][0]['transl']
			word = data[i][0]['arabic']
			root = self.stem(data[i][0]['arabic'])
			possible_root = self.pam_stem(word)
			rtrans = self.transliteration(root)
			self.analyzed_data.append({'arabic': word, 'transl': tans, 'root': root, 'root_transl': rtrans, 'candidates': possible_root})
		return self.analyzed_data


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

		key = self.transliteration(self.stem(key))
		data = self.extract_data()

		# print("Data   : ", data)
		# print("Search : ", [search, key])

		for i in range(0, len(data)):
			if data[i]['root_transl'] == key:
				result.append(data[i]['arabic'])

		print("Result : ", set(result))
		return set(result)


var = '''
الْحَمْدُ لِلَّهِ رَبِّ الْعَالَمِينَ
الرَّحْمَٰنِ الرَّحِيمِ
مَالِكِ يَوْمِ الدِّينِ
إِيَّاكَ نَعْبُدُ وَإِيَّاكَ نَسْتَعِينُ
اهْدِنَا الصِّرَاطَ الْمُسْتَقِيمَ
صِرَاطَ الَّذِينَ أَنْعَمْتَ عَلَيْهِمْ غَيْرِ الْمَغْضُوبِ عَلَيْهِمْ وَلَا الضَّالِّينَ
'''

arab = Arabica(var)
arab.search('رحم')