import re
import nltk

# stopwords
try:
    from nltk.corpus import stopwords
    stopwords.words("english")
except LookupError:
    nltk.download("stopwords")
    from nltk.corpus import stopwords

stop_words = set(stopwords.words("english"))

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^\w\s]', ' ', text)  # Remove punctuation
    words = text.split()

    filtered_words = []
    for word in words:
        if word not in stop_words:
            filtered_words.append(word)

    return " ".join(filtered_words)
