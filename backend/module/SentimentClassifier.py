from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_selection import SelectKBest, chi2

class SentimentClassifier:
    def __init__(self, df, calon_name, k_percentage=0.6):
        self.df_calon = df[df["Pasangan Calon"] == calon_name]
        self.tfidf_vectorizer = TfidfVectorizer()
        self.X_tfidf = self.tfidf_vectorizer.fit_transform(self.df_calon["preprocessed"])

        self.k_value = int(k_percentage * self.X_tfidf.shape[1])
        self.chi2_selector = SelectKBest(chi2, k=self.k_value)
        self.X_new = self.chi2_selector.fit_transform(self.X_tfidf, self.df_calon['Sentiment'])
    
    def get_df_calon(self):
        return self.df_calon

    def get_tfidf_vectorizer(self):
        return self.tfidf_vectorizer

    def get_chi2_selector(self):
        return self.chi2_selector

    def get_X_tfidf(self):
        return self.X_tfidf

    def get_X_new(self):
        return self.X_new
