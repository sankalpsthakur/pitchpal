import spacy as spacy
import textblob
from googletrans import Translator
from collections import Counter
from transformers import pipeline


# Load Spacy multilingual model
nlp_multi = spacy.load("en_core_web_sm")


# Text Classification
text_classification_model = pipeline("text-classification", model="distilbert-base-uncased")
# Named Entity Recognition (Semantic Role Labeling)
semantic_role_labeling_model = pipeline("ner", model="dbmdz/bert-large-cased-finetuned-conll03-english")
# Zero-Shot Classification (Topic Modeling)
topic_modeling_model = pipeline("zero-shot-classification", model="typeform/distilbert-base-uncased-mnli")
# Question Answering (Discourse Analysis)
discourse_analysis_model = pipeline("question-answering", model="distilbert-base-uncased-distilled-squad")
# Text Generation (Dialogue Systems)
dialogue_systems_model = pipeline("text-generation", model="microsoft/DialoGPT-small")
# Summarization
summarization_model = pipeline("summarization", model="sshleifer/distilbart-xsum-12-6")


def detect_language(text):
    """
    Detects the language of a text.

    Args:
        text: The text to be detected.

    Returns:
        The language code of the text.
    """

    translator = Translator()
    lang_code = translator.detect(text).lang
    return lang_code


def named_entity_recognition(text):
    """
    Perform named entity recognition on a text.

    Args:
        text: The text to be processed.

    Returns:
        A list of named entities.
    """

    doc = nlp_multi(text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    return entities


def sentiment_analysis(text, lang_code):
    """
    Perform sentiment analysis on a text.

    Args:
        text: The text to be processed.
        lang_code: The language code of the text.

    Returns:
        The sentiment polarity of the text.
    """

    if lang_code != "en":
        translator = Translator()
        text = translator.translate(text, dest="en").text
    blob = textblob.TextBlob(text)
    sentiment_polarity = blob.sentiment.polarity
    return sentiment_polarity


def speaker_analysis(text):
    """
    Perform speaker analysis on a text.

    Args:
        text: The text to be processed.

    Returns:
        A dictionary of speakers and their counts.
    """

    doc = nlp_multi(text)
    speakers = [token.text for token in doc if token.pos_ == "PROPN"]
    speaker_count = Counter(speakers)
    return speaker_count


def keyword_usage(text):
    """
    Perform keyword usage analysis on a text.

    Args:
        text: The text to be processed.

    Returns:
        A dictionary of keywords and their counts.
    """

    doc = nlp_multi(text)
    keywords = [token.text for token in doc if token.pos_ in ("NOUN", "VERB", "ADJ")]
    keyword_count = Counter(keywords)
    return keyword_count


def objection_handling(text):
    """
    Perform objection handling on a text.

    Args:
        text: The text to be processed.

    Returns:
        The number of objections found in the text.
    """

    objections = ["price", "cost", "expensive", "cheap", "value", "budget", "afford"]
    keyword_count = keyword_usage(text)
    objection_count = sum([keyword_count[obj] for obj in objections])
    return objection_count

def annotate_text(text):
    # Language Detection
    lang_code = detect_language(text)
    
    # Named Entity Recognition
    entities = named_entity_recognition(text)
    
    # Sentiment Analysis
    sentiment_polarity = sentiment_analysis(text, lang_code)
    
    # Speaker Analysis
    speaker_count = speaker_analysis(text)
    
    # Keyword Usage
    keyword_count = keyword_usage(text)
    
    # Objection Handling
    objection_count = objection_handling(text)

    # Dependency Parsing
    doc = nlp_multi(text)
    dependency_parsing = [(token.text, token.dep_, token.head.text) for token in doc]
    
    # Text Classification
    text_classification = text_classification_model(text)

    # Semantic Role Labeling
    semantic_role_labeling = semantic_role_labeling_model(text)

    # Topic Modeling
    topic_modeling = topic_modeling_model(text)

    # Discourse Analysis
    discourse_analysis = discourse_analysis_model(text)

    # Dialogue Systems
    dialogue_systems = dialogue_systems_model(text)

    # Summarization of Conversations
    summarization = summarization_model(text)

    annotated_text = {
        "language_code": lang_code,
        "entities": entities,
        "sentiment_polarity": sentiment_polarity,
        "speaker_count": speaker_count,
        "keyword_count": keyword_count,
        "objection_count": objection_count,
        "dependency_parsing": dependency_parsing,
        "text_classification": text_classification,
        "semantic_role_labeling": semantic_role_labeling,
        "topic_modeling": topic_modeling,
        "discourse_analysis": discourse_analysis,
        "dialogue_systems": dialogue_systems,
        "summarization": summarization,
    }

    return annotated_text

text = "John met María in Bangalore. El precio del producto es alto. அவர் நல்லவர்."
annotated_text = annotate_text(text)
print(annotated_text)
