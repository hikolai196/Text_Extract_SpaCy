import spacy
import PyPDF2
import docx
from langdetect import detect

class DocumentParser:
    def __init__(self):
        try:
            # Load spaCy language models
            self.nlp_en = spacy.load("en_core_web_sm")
            self.nlp_zh = spacy.load("zh_core_web_sm")
            self.nlp_ja = spacy.load("ja_core_news_sm")
        except OSError:
            print("Please download relevant language models with:\n")
            print("python -m spacy download xx_core_web_sm")
            raise

    def parse_pdf(self, file):
        # Read pdf files .pdf
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text

    def parse_docx(self, file):
        # Read microsoft word .docx file
        doc = docx.Document(file)
        return "\n".join([para.text for para in doc.paragraphs])

    def parse_txt(self, file):
        # Read/Decode bytes to string for text files
        return file.read().decode('utf-8')

    def detect_language(self, text: str) -> str:
        return detect(text)