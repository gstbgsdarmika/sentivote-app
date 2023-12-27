import re
import string
import nltk
import pandas as pd
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from nltk.corpus import stopwords

class TextProcessor:
    def __init__(self):
        # Inisialisasi stopwords
        factory = StopWordRemoverFactory()
        stopwords_sastrawi = factory.get_stop_words()
        stopwords_nltk = set(stopwords.words("indonesian"))

        txt_stopword = pd.read_csv('backend/database/stopword/stopword.csv', header=None, names=["stopwords"])
        additional_stopwords = list(txt_stopword["stopwords"])

        self.stop_words = stopwords_sastrawi + list(stopwords_nltk) + additional_stopwords + ["petrus", "sech", "bulakparen", "dcs", "mug","ahhhh","ah"
                "background2","nya", "klik", "nih", "wah", "bd","cie", "wahh", "gtgt", "wkwkw", "grgr", "thun",
                "twit", "iii", "08alian", "wkwkwkwk", "wkwk","wkwkwk", "ah", "ampnbsp", "bawaslu",
                "ltpgtampnbspltpgt", "dancukkk", "yach", "kepl", "wow","kretek", "woww", "smpn", "hmmmm", "hehe",
                "hahaha", "ppp", "nek", "rang", "tuh", "pls", "otw", "pas","haha", "ha", "hahahahaha", "hahahasenget",
                "xixixixi", "hehehehee", "nder", "aduuuhhh", "lah","lah", "deh", "si", "kan", "njirrrr", "huehehee",
                "hehehe", "yahh", "yah", "loh", "elo", "gw", "didkgkl","sih", "lu", "yeyeye", "dlllllllllll", "se",
                "pisss", "yo", "kok", "nge", "wkwkkw", "dah", "wahhh", "apa"]

        # Inisialisasi kamus normalisasi
        normalized_word = pd.read_csv('backend/database/normalisasi/normalisasi.csv', encoding='latin1')
        self.normalized_word_dict = {}
        for index, row in normalized_word.iterrows():  # Iterate over rows
            word = row.iloc[0]  # Access using iloc for position-based indexing
            normalized_word = row.iloc[1]
            if word not in self.normalized_word_dict:
                self.normalized_word_dict[word] = normalized_word

        # Inisialisasi stemmer
        factory = StemmerFactory()
        self.stemmer = factory.create_stemmer()

    def remove_punctuation(self, text):
        regex = re.compile('[%s]' % re.escape(string.punctuation))
        return regex.sub(' ', text)

    def clean_text(self, text):
        text = text.lower()
        text = re.sub(r'http\S+', '', text, flags=re.MULTILINE)
        text = text.encode('ascii', 'replace').decode('ascii')
        text = re.sub(r"@\S+", "", text)
        text = self.remove_punctuation(text)
        text = re.sub(r'\b[a-zA-Z]\b', '', text)
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        return ' '.join(text.split())

    def remove_stopwords(self, text):
        new_text = ""
        for word in text.split():
            if word not in self.stop_words:
                new_text += " " + word
        return new_text

    def normalize_term(self, text):
        new_text = ""
        for word in text.split():
            if word in self.normalized_word_dict:
                new_text += " " + self.normalized_word_dict[word]
            else:
                new_text += " " + word
        return new_text

    def stemming(self, text):
        return self.stemmer.stem(text)
    
    def preprocess_all(self, text):
        # Apply all preprocessing functions
        cleaned_text = self.clean_text(text)
        without_stopwords = self.remove_stopwords(cleaned_text)
        normalized_text = self.normalize_term(without_stopwords)
        stemmed_text = self.stemming(normalized_text)
        
        return stemmed_text
