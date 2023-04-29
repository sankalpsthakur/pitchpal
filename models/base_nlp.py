import spacy
import spacy_stanza
import textblob
from googletrans import Translator
from collections import Counter

# Load Spacy multilingual model using Stanza
nlp_multi = spacy_stanza.load_pipeline("multi")

def detect_language(text):
    translator = Translator()
    lang_code = translator.detect(text).lang
    return lang_code

def named_entity_recognition(text):
    doc = nlp_multi(text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    return entities

def sentiment_analysis(text, lang_code):
    if lang_code != "en":
        translator = Translator()
        text = translator.translate(text, dest="en").text
    blob = textblob.TextBlob(text)
    sentiment_polarity = blob.sentiment.polarity
    return sentiment_polarity

def speaker_analysis(text):
    doc = nlp_multi(text)
    speakers = [token.text for token in doc if token.pos_ == "PROPN"]
    speaker_count = Counter(speakers)
    return speaker_count

def keyword_usage(text):
    doc = nlp_multi(text)
    keywords = [token.text for token in doc if token.pos_ in ("NOUN", "VERB", "ADJ")]
    keyword_count = Counter(keywords)
    return keyword_count

def objection_handling(text):
    objections = ["price", "cost", "expensive", "cheap", "value", "budget", "afford"]
    keyword_count = keyword_usage(text)
    objection_count = sum([keyword_count[obj] for obj in objections])
    return objection_count


text = "John met María in Bangalore. El precio del producto es alto. அவர் நல்லவர்."

# Language Detection
lang_code = detect_language(text)
print(f"Detected Language: {lang_code}")

# Named Entity Recognition
entities = named_entity_recognition(text)
print(f"Entities: {entities}")

# Sentiment Analysis
sentiment_polarity = sentiment_analysis(text, lang_code)
print(f"Sentiment Polarity: {sentiment_polarity}")

# Speaker Analysis
speaker_count = speaker_analysis(text)
print(f"Speaker Count: {speaker_count}")

# Keyword Usage
keyword_count = keyword_usage(text)
print(f"Keyword Count: {keyword_count}")

# Objection Handling
objection_count = objection_handling(text)
print(f"Objection Count: {objection_count}")
