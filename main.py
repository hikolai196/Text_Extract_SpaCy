import streamlit as st
import os
from document_parser import DocumentParser
from text_extractor import TextExtractor

def main():
    st.title("📝 Text Extraction Pipeline")

    # File upload
    uploaded_file = st.file_uploader("Choose a document", 
                                     type=['pdf', 'docx', 'txt'])

    if uploaded_file is not None:
        # Initialize components
        parser = DocumentParser()
        extractor = TextExtractor()

        # Get the filename
        filename = uploaded_file.name
        file_extension = os.path.splitext(filename)[1].lower()

        # Parse document based on file type
        try:
            if file_extension == '.pdf':
                text = parser.parse_pdf(uploaded_file)
            elif file_extension == '.docx':
                text = parser.parse_docx(uploaded_file)
            elif file_extension == '.txt':
                text = parser.parse_txt(uploaded_file)
            else:
                return

            # Detect language
            language = parser.detect_language(text)

            # Extract entities
            entities = extractor.extract_entities(text, language)
            keywords = extractor.extract_keywords(text, language)

            # Display results
            st.subheader("Extracted Information")
            
            st.write(f"Detected Language: {language}")
            
            st.write("### Entities")
            for entity_type, values in entities.items():
                st.write(f"**{entity_type}**: {', '.join(values)}")
            
            st.write("### Top Keywords")
            st.write(', '.join(keywords))

            # Optional: Display text preview
            st.write("### Text Preview")
            st.text(text[:500] + "...")

        except Exception as e:
            st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()