import streamlit as st
from src.data_ingestion import handle_file_upload
from src.data_preprocessing import predict_category
from src.skill_extraction import extract_skills

st.set_page_config(page_title="Resume Category Prediction", page_icon="📄", layout="wide")

def main():
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

            # Predict the resume category
            st.subheader("Predicted Category")
            category = predict_category(resume_text)
            st.write(f"The predicted category of the uploaded resume is: **{category}**")

            # Extract skills
            st.subheader("Extracted Skills")
            skills = extract_skills(resume_text)
            if skills:
                st.write("Top 5 relevant skills identified in the resume:")
                for skill in skills:
                    st.write(f"- {skill}")
            else:
                st.write("No skills found in the uploaded resume.")

        except Exception as e:
            st.error(f"Error processing the file: {str(e)}")


if __name__ == "__main__":
    main()
