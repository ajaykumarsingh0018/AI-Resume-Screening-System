import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

stop_words = set(stopwords.words("english"))

def clean_text(text):
    # Tokenize the text
    text = text.lower()
    text  = re.sub(r'[^\w\s]', ' ', text)  # Remove punctuation
    words = text.split()
    filtered_words = []
    for word in words:
        if word not in stop_words:
            filtered_words.append(word)
    return " ".join(filtered_words)
