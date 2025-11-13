import spacy

nlp = spacy.load("en_core_web_sm")  # Small model
def generate_embedding(text):
    print(text)
    return nlp(text).vector
