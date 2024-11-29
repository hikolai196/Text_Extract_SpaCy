import spacy
from typing import List, Dict

class TextExtractor:
    def __init__(self):
        # Load multilingual NER models *need adjust
        try:
            self.nlp_en = spacy.load("en_core_web_sm")
            self.nlp_zh = spacy.load("zh_core_web_sm")
            self.nlp_ja = spacy.load("ja_core_news_sm")
        except OSError:
            print("Language models not found. Please download them.")
            raise

    def extract_entities(self, text: str, language: str) -> Dict[str, List[str]]:
        # Select appropriate language model
        nlp_model = {
            'en': self.nlp_en,
            'zh': self.nlp_zh,
            'ja': self.nlp_ja
        }.get(language, self.nlp_en)

        # Process text
        doc = nlp_model(text)

        # Extract entities
        entities = {
            'PERSON': [],
            'ORG': [],
            'GPE': [],  # Geopolitical entities
            'DATE': []
        }

        for ent in doc.ents:
            if ent.label_ in entities:
                entities[ent.label_].append(ent.text)

        return entities

    def extract_keywords(self, text: str, language: str, top_n: int = 10) -> List[str]:
        # Select appropriate language model
        nlp_model = {
            'en': self.nlp_en,
            'zh': self.nlp_zh,
            'ja': self.nlp_ja
        }.get(language, self.nlp_en)

        # Process text
        doc = nlp_model(text)

        # Extract keywords (nouns and proper nouns)
        keywords = [token.text for token in doc if token.pos_ in ['PROPN', 'NOUN']]
        
        # Remove duplicates and return top N
        return list(dict.fromkeys(keywords))[:top_n]