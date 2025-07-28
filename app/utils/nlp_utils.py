import spacy
nlp = spacy.load("en_core_web_sm")

def extract_entities(doc):
    return list(set(ent.text.lower() for ent in doc.ents))

def extract_keywords_from_transcript(text):
    doc = nlp(text)
    chunks = [chunk.text.lower() for chunk in doc.noun_chunks if len(chunk.text) > 2]
    entities = extract_entities(doc)
    return list(set(chunks + entities))

def extract_nlp_features(term):
    doc = nlp(term)
    lemmas = list(set(token.lemma_ for token in doc if not token.is_stop and token.is_alpha))
    entities = extract_entities(doc)
    return lemmas, entities
