from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import accuracy_score, classification_report

class TextClassifier:
    def __init__(self):
        self.tfidf_vectorizer = TfidfVectorizer()
        self.chi2_selector = None
        self.rf_classifier = None

    def preprocess_text(self, text_data):
        # You can add your text preprocessing logic here
        # For now, assuming 'text_data' is already preprocessed
        return text_data

    def train_tfidf(self, text_data):
        preprocessed_text = self.preprocess_text(text_data)
        tfidf = self.tfidf_vectorizer.fit_transform(preprocessed_text)
        return tfidf

    def select_features_chi2(self, tfidf, labels):
        kbest = int(0.4 * tfidf.shape[1])
        self.chi2_selector = SelectKBest(chi2, k=kbest)
        X_new_aspek = self.chi2_selector.fit_transform(tfidf, labels)
        return X_new_aspek

    def train_rf(self, x, y):
        # splitting
        X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

        # Define the Random Forest classifier
        self.rf_classifier = RandomForestClassifier()

        # Define the hyperparameter grid for tuning
        param_grid = {
            'n_estimators': [50, 100, 200],
            'max_depth': [None, 10, 20, 30],
            'min_samples_split': [2, 5, 10],
            'min_samples_leaf': [1, 2, 4]
        }

        # Use GridSearchCV for hyperparameter tuning and cross-validation
        grid_search = GridSearchCV(estimator=self.rf_classifier, param_grid=param_grid, cv=5, scoring='accuracy')
        grid_search.fit(X_train, y_train)

        # Access Accuracy Scores for Each Combination
        results = grid_search.cv_results_

        # Print accuracy scores for each combination
        for mean_score, params in zip(results['mean_test_score'], results['params']):
            print(f"Accuracy: {mean_score:.4f}, Parameters: {params}")

        # Get the best parameters and the best model
        best_params = grid_search.best_params_
        best_rf_model = grid_search.best_estimator_

        # Evaluate the model on the test set
        y_pred = best_rf_model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)

        return best_rf_model

        # # Display results
        # print("\nJumlah fitur:", x.shape[1])
        # print("Best Hyperparameters:", best_params)
        # print("Test Accuracy:", accuracy)
        # print("\nClassification Report:\n", classification_report(y_test, y_pred))
        # return best_rf_model
