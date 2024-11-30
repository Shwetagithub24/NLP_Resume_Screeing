# Resume Classification and Skills Extraction Project
This project is a machine learning-based application to classify resumes into predefined categories and extract relevant skills using text processing and supervised learning. 
It employs techniques like TF-IDF vectorization, machine learning classifiers, and modular programming for better scalability.
```
Resume-Classification-Skills-Extraction/
│
├── data/                   
│   └── UpdatedResumeDataSet.csv  # Dataset
│
├── modules/
│   ├── data_ingestion.py         # Handles data loading
│   ├── data_preprocessing.py     # Handles text cleaning
│   ├── model_training.py         # Machine learning model training
│   ├── skills_extraction.py      # Skills extraction logic
│   ├── prediction.py             # Prediction logic
│   └── utils.py                  # Common utilities
│
├── models/               
│   ├── tfidf.pkl                 # Saved TF-IDF model
│   ├── clf.pkl                   # Saved classifier
│   └── encoder.pkl               # Label encoder
│
├── notebooks/                   
│   └── Resume_Classification.ipynb  # Original code notebook
```

## Model Training and Evaluation
The model is trained using One-vs-Rest Classifier with support for:
- SVM
- KNN
- Random Forest
TF-IDF vectorization converts resumes into numerical features.
The model achieves high accuracy on the test dataset, showcasing its effectiveness in resume classification.
Model Accuracy: 98.45% (The accuracy score is computed using sklearn.metrics.accuracy_score)

## Modules
1. data_ingestion.py:
- Loads the dataset.
- Handles missing values and ensures data integrity.
  
2. data_preprocessing.py:
- Cleans text (removes URLs, hashtags, special characters).
- Prepares data for TF-IDF vectorization.

3. model_training.py:
- Trains machine learning models using scikit-learn.
- Supports multiple classifiers (SVM, Random Forest, etc.).
- Handles oversampling for imbalanced datasets.

4. skills_extraction.py:
- Extracts skills and qualifications from resumes.


## User Interface
![UI](https://github.com/user-attachments/assets/19c7555e-f9b0-4384-9f5d-c153f2018407)

