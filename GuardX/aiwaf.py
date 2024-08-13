import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split, StratifiedKFold, GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report
import joblib

log_data = []

class AIWAF:
    def __init__(self):
        self.model = None
        self.label_encoder = None
    
    def train_logistic_regression(self, xss_path, sql_path, normal_path, shell_path):
        # Load datasets
        xss_data = pd.read_csv(xss_path)
        sql_data = pd.read_csv(sql_path)
        normal_data = pd.read_csv(normal_path)
        shell_code_data = pd.read_csv(shell_path)

        # Add labels
        xss_data['label'] = 'xss'
        sql_data['label'] = 'sql_injection'
        normal_data['label'] = 'normal'
        shell_code_data['label'] = 'shell_code'

        # Combine datasets
        data = pd.concat([xss_data, sql_data, normal_data, shell_code_data], ignore_index=True)

        # Save combined dataset for reference
        data.to_csv('combined_dataset.csv', index=False)

        # Encode labels
        label_encoder = LabelEncoder()
        data['label'] = label_encoder.fit_transform(data['label'])

        # Split data
        X_train, X_test, y_train, y_test = train_test_split(data['input'], data['label'], test_size=0.2, random_state=42)

        # Create a pipeline with TF-IDF and Logistic Regression
        pipeline = make_pipeline(TfidfVectorizer(), LogisticRegression())
        pipeline.fit(X_train, y_train)

        # Evaluate the model
        print("Logistic Regression Model Accuracy: ", pipeline.score(X_test, y_test))
        log_data.append(f"Logistic Regression Model Accuracy: {str(round(pipeline.score(X_test, y_test), 5))}")

        # Save the model and label encoder
        self.model = pipeline
        self.label_encoder = label_encoder

        joblib.dump(self.model, 'logistic_regression_model.pkl')
        joblib.dump(self.label_encoder, 'logistic_regression_label_encoder.pkl')

    def train_random_forest_imbalanced(self, xss_path, sql_path, normal_path, shell_path):
        # Load datasets
        xss_data = pd.read_csv(xss_path)
        sql_data = pd.read_csv(sql_path)
        normal_data = pd.read_csv(normal_path)
        shell_code_data = pd.read_csv(shell_path)

        # Add labels
        xss_data['label'] = 'xss'
        sql_data['label'] = 'sql_injection'
        normal_data['label'] = 'normal'
        shell_code_data['label'] = 'shell_code'

        # Combine datasets
        data = pd.concat([xss_data, sql_data, normal_data, shell_code_data], ignore_index=True)

        # Encode labels
        label_encoder = LabelEncoder()
        data['label'] = label_encoder.fit_transform(data['label'])

        # Split data
        X_train, X_test, y_train, y_test = train_test_split(data['input'], data['label'], test_size=0.2, random_state=42)

        # Create a pipeline with TF-IDF and a Random Forest Classifier
        pipeline = make_pipeline(
            TfidfVectorizer(ngram_range=(1, 2), analyzer='char_wb'),  # Use character-level n-grams
            RandomForestClassifier(n_estimators=100, random_state=42)
        )

        # Define hyperparameter grid for tuning
        param_grid = {
            'randomforestclassifier__n_estimators': [100, 200],
            'randomforestclassifier__max_depth': [None, 10, 20],
            'randomforestclassifier__min_samples_split': [2, 5, 10]
        }

        # Perform grid search
        grid_search = GridSearchCV(pipeline, param_grid, cv=5, scoring='accuracy')
        grid_search.fit(X_train, y_train)

        # Evaluate the model
        best_model = grid_search.best_estimator_
        print("Random Forest Model Class-imbalanced Best Parameters: ", grid_search.best_params_)
        print("Random Forest Model Class-imbalanced Accuracy: ", best_model.score(X_test, y_test))
        log_data.append(f"Random Forest Model Class-imbalanced Best Parameters: {grid_search.best_params_}")
        log_data.append(f"Random Forest Model Class-imbalanced Accuracy: {str(round(best_model.score(X_test, y_test), 5))}")

        # Get detailed classification report
        y_pred = best_model.predict(X_test)
        print(classification_report(y_test, y_pred, target_names=label_encoder.classes_))
        log_data.append(classification_report(y_test, y_pred, target_names=label_encoder.classes_))

        # Save the best model and label encoder
        self.model = best_model
        self.label_encoder = label_encoder

        joblib.dump(self.model, 'random_forest_model_imbalanced.pkl')
        joblib.dump(self.label_encoder, 'random_forest_label_encoder_imbalanced.pkl')

    def train_random_forest_balanced(self, xss_path, sql_path, normal_path, shell_path):
        # Load datasets
        xss_data = pd.read_csv(xss_path)
        sql_data = pd.read_csv(sql_path)
        normal_data = pd.read_csv(normal_path)
        shell_code_data = pd.read_csv(shell_path)

        # Add labels
        xss_data['label'] = 'xss'
        sql_data['label'] = 'sql_injection'
        normal_data['label'] = 'normal'
        shell_code_data['label'] = 'shell_code'

        # Combine datasets
        data = pd.concat([xss_data, sql_data, normal_data, shell_code_data], ignore_index=True)

        # Encode labels
        label_encoder = LabelEncoder()
        data['label'] = label_encoder.fit_transform(data['label'])

        # Split data
        X_train, X_test, y_train, y_test = train_test_split(data['input'], data['label'], test_size=0.2, random_state=42, stratify=data['label'])

        # Create a pipeline with TF-IDF and a Random Forest Classifier
        pipeline = make_pipeline(
            TfidfVectorizer(ngram_range=(1, 2), analyzer='char_wb'),  # Use character-level n-grams
            RandomForestClassifier(class_weight='balanced', random_state=42)
        )

        # Define hyperparameter grid for tuning
        param_grid = {
            'randomforestclassifier__n_estimators': [100, 200],
            'randomforestclassifier__max_depth': [None, 10, 20],
            'randomforestclassifier__min_samples_split': [2, 5, 10]
        }

        # Perform grid search with stratified k-fold
        strat_k_fold = StratifiedKFold(n_splits=3, shuffle=True, random_state=42)
        grid_search = GridSearchCV(pipeline, param_grid, cv=strat_k_fold, scoring='accuracy')
        grid_search.fit(X_train, y_train)

        # Evaluate the model
        best_model = grid_search.best_estimator_
        print("Random Forest Model Class-Balanced Best Parameters: ", grid_search.best_params_)
        print("Random Forest Model Class-Balanced Accuracy: ", best_model.score(X_test, y_test))
        log_data.append(f"Random Forest Model Class-Balanced Best Parameters: {grid_search.best_params_,}")
        log_data.append(f"Random Forest Model Class-Balanced Accuracy: {str(round(best_model.score(X_test, y_test), 5))}")

        # Get detailed classification report
        y_pred = best_model.predict(X_test)
        print(classification_report(y_test, y_pred, target_names=label_encoder.classes_))
        log_data.append(classification_report(y_test, y_pred, target_names=label_encoder.classes_))

        # Save the best model and label encoder
        self.model = best_model
        self.label_encoder = label_encoder

        joblib.dump(self.model, 'random_forest_model_balanced.pkl')
        joblib.dump(self.label_encoder, 'random_forest_label_encoder_balanced.pkl')
    
    def load_model(self, model_path, label_encoder_path):
        self.model = joblib.load(model_path)
        self.label_encoder = joblib.load(label_encoder_path)
    
    def detect_payload(self, input_text):
        if self.model is None or self.label_encoder is None:
            raise RuntimeError("Model and label encoder have not been loaded. Please load the model using load_model method.")
        
        prediction = self.model.predict([input_text])
        label = self.label_encoder.inverse_transform(prediction)
        return label[0]

if __name__ == '__main__':
    aiwaf = AIWAF()

    xss_file = "xss_payloads.csv"
    sql_file = "sql_injection_payloads.csv"
    normal_file = "normal_inputs.csv"
    shell_file = "shell_code_payloads.csv"
    
    aiwaf.train_logistic_regression(xss_file, sql_file, normal_file, shell_file)  # Simple Logistic Regression model
    aiwaf.train_random_forest_imbalanced(xss_file, sql_file, normal_file, shell_file)  # Class Imbalanced model
    aiwaf.train_random_forest_balanced(xss_file, sql_file, normal_file, shell_file)  # Class Balanced model

    text_data = '\n'.join(log_data)

    with open('train_data_log.txt', 'w') as log_file:
        log_file.write(text_data)
    
    print("Log file written successful of it.")
