import re
import pickle
import string
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from cleantext import clean

class TextProcessor:
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        self.factory = StemmerFactory()
        self.stemmer = self.factory.create_stemmer()

    def remove_numbers(self, text):
        return re.sub(r'\d+', '', text)

    def remove_punctuation(self, text):
        return re.sub('[' + string.punctuation + ']', ' ', text)

    def remove_emojis(self, text):
        return clean(text, no_emoji=True)  # Termasuk case folding

    def remove_stopwords(self, text):
        stop_words = set(stopwords.words("indonesian"))
        new_text = ""
        for word in text.split():
            if word not in stop_words:
                new_text += " " + word
        return new_text

    def lemmatize_word(self, text):
        new_text = ""
        word_tokens = text.split()
        # memberikan konteks, yaitu part-of-speech
        lemmas = [self.lemmatizer.lemmatize(word, pos='v') for word in word_tokens]
        for word in text.split():
            new_text += " " + self.lemmatizer.lemmatize(word, pos='v')
        return new_text

    def stemming(self, text):
        return self.stemmer.stem(text)

    def preprocess(self, text):
        text = self.remove_numbers(text)
        text = self.remove_punctuation(text)
        text = self.remove_emojis(text)
        text = self.remove_stopwords(text)
        # text = self.lemmatize_word(text)
        text = self.stemming(text)
        return text
    
# menggunakan instance
text_processor_instance = TextProcessor()

# menyimpan instance menggunakan pickle
with open('model/text_processor.sav', 'wb') as f:
    pickle.dump(text_processor_instance, f)