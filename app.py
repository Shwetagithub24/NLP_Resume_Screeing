import streamlit as st
import pickle
import docx
import PyPDF2
import re
import nltk
import spacy
from spacy.matcher import PhraseMatcher
from skillNer.general_params import SKILL_DB
from skillNer.skill_extractor_class import SkillExtractor

# Download necessary NLTK resources
nltk.download('punkt')
nltk.download('stopwords')

# Load pre-trained models
svc_model = pickle.load(open('clf.pkl', 'rb'))
tfidf = pickle.load(open('tfidf.pkl', 'rb'))
le = pickle.load(open('encoder.pkl', 'rb'))

# Initialize spaCy NLP model
# load default skills data base
from skillNer.general_params import SKILL_DB
# import skill extractor
from skillNer.skill_extractor_class import SkillExtractor
nlp = spacy.load("en_core_web_lg")
# init skill extractor
phrase_matcher = PhraseMatcher(nlp.vocab)

skill_extractor = SkillExtractor(nlp, SKILL_DB, PhraseMatcher)
# Initialize spaCy and PhraseMatcher



# Function to clean resume text
def cleanResume(txt):
    cleanText = re.sub('http\S+\s', ' ', txt)
    cleanText = re.sub('RT|cc', ' ', cleanText)
    cleanText = re.sub('#\S+\s', ' ', cleanText)
    cleanText = re.sub('@\S+', '  ', cleanText)
    cleanText = re.sub('[%s]' % re.escape("""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""), ' ', cleanText)
    cleanText = re.sub(r'[^\x00-\x7f]', ' ', cleanText)
    cleanText = re.sub('\s+', ' ', cleanText)
    return cleanText


# Function to extract text from PDF
def extract_text_from_pdf(file):
    pdf_reader = PyPDF2.PdfReader(file)
    text = ''
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text


# Function to extract text from DOCX
def extract_text_from_docx(file):
    doc = docx.Document(file)
    text = ''
    for paragraph in doc.paragraphs:
        text += paragraph.text + '\n'
    return text


# Function to extract text from TXT
def extract_text_from_txt(file):
    try:
        text = file.read().decode('utf-8')
    except UnicodeDecodeError:
        text = file.read().decode('latin-1')
    return text


# Function to handle file upload and extraction
def handle_file_upload(uploaded_file):
    file_extension = uploaded_file.name.split('.')[-1].lower()
    if file_extension == 'pdf':
        text = extract_text_from_pdf(uploaded_file)
    elif file_extension == 'docx':
        text = extract_text_from_docx(uploaded_file)
    elif file_extension == 'txt':
        text = extract_text_from_txt(uploaded_file)
    else:
        raise ValueError("Unsupported file type. Please upload a PDF, DOCX, or TXT file.")
    return text


# Function to predict the category of a resume
def pred(input_resume):
    cleaned_text = cleanResume(input_resume)
    vectorized_text = tfidf.transform([cleaned_text])
    vectorized_text = vectorized_text.toarray()
    predicted_category = svc_model.predict(vectorized_text)
    predicted_category_name = le.inverse_transform(predicted_category)
    return predicted_category_name[0]  # Return the category name


# Function to extract skills from resume text
def extract_skills(resume_text):
    annotations = skill_extractor.annotate(resume_text)
    return [result['doc_node_value'] for result in annotations['results']['full_matches']]


# Streamlit app layout
def main():
    st.set_page_config(page_title="Resume Category Prediction", page_icon="📄", layout="wide")

    st.title("Resume Category Prediction App")
    st.markdown("Upload a resume in PDF, TXT, or DOCX format and get the predicted job category.")

    uploaded_file = st.file_uploader("Upload a Resume", type=["pdf", "docx", "txt"])

    if uploaded_file is not None:
        try:
            # Extract text from the uploaded file
            resume_text = handle_file_upload(uploaded_file)
            st.write("Successfully extracted the text from the uploaded resume.")

            if st.checkbox("Show extracted text", False):
                st.text_area("Extracted Resume Text", resume_text, height=300)

            # Make prediction
            st.subheader("Predicted Category")
            category = pred(resume_text)
            st.write(f"The predicted category of the uploaded resume is: **{category}**")

            
            # Extract skills using SkillNER
            st.subheader("Extracted Skills")
            skills = extract_skills(resume_text)
            if skills:
                st.write("Top 10 relevant skills identified in the resume:")
                for skill in skills:
                    st.write(f"- {skill}")
            else:
                st.write("No skills found in the uploaded resume.")

        except Exception as e:
            st.error(f"Error processing the file: {str(e)}")


if __name__ == "__main__":
    main()
