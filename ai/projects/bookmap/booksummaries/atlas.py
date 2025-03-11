from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import joblib
import os

class Atlas:
    def __init__(self):
        self.indices = None
        self.cosine_sim = None
        self.tfidf_vectorizer = None
        self.titles = None
    
    def train(self, df):
        self.indices = pd.Series(df.index, index=df['Title']).drop_duplicates()
        self.titles = df['Title'].values
        self.tfidf_vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_mat = self.tfidf_vectorizer.fit_transform(df['Description'])
        self.cosine_sim = cosine_similarity(tfidf_mat, tfidf_mat)
        return self
    
    def similars(self, title, n=10):
        try:
            idx = self.indices[title]
        except KeyError:
            return f"Book '{title}' not found in the database."
        sim_scores = list(enumerate(self.cosine_sim[idx]))
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)[1:n+1]
        return [(self.titles[i], score) for i, score in sim_scores]
    
    def save(self, filepath="book_similarity_model"):
        os.makedirs(os.path.dirname(filepath) if os.path.dirname(filepath) else '.', exist_ok=True)
        joblib.dump(self.indices, f"{filepath}_indices.pkl")
        joblib.dump(self.cosine_sim, f"{filepath}_cosine_sim.pkl")
        joblib.dump(self.tfidf_vectorizer, f"{filepath}_tfidf.pkl")
        joblib.dump(self.titles, f"{filepath}_titles.pkl")
        print(f"Model saved to {filepath}")
        
    @classmethod
    def load(cls, filepath="book_similarity_model"):
        model = cls()
        model.indices = joblib.load(f"{filepath}_indices.pkl")
        model.cosine_sim = joblib.load(f"{filepath}_cosine_sim.pkl")
        model.tfidf_vectorizer = joblib.load(f"{filepath}_tfidf.pkl")
        model.titles = joblib.load(f"{filepath}_titles.pkl")
        print(f"Model loaded from {filepath}")
        return model
    
    def search_titles(self, query, n=5):
        if self.titles is None:
            return "Model not trained. Call train() first."

        query = query.lower()
        matching_titles = [title for title in self.titles 
                          if query in title.lower()]
        return matching_titles[:n] 