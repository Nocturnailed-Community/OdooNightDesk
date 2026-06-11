import re
from html.parser import HTMLParser

class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html or "")
    return s.get_data()

# Sentiment Keywords
POSITIVE_KEYWORDS = {
    'en': ['good', 'great', 'excellent', 'happy', 'satisfied', 'thanks', 'thank', 'awesome', 'perfect', 'solved', 'resolved', 'helpful'],
    'id': ['bagus', 'hebat', 'puas', 'terima kasih', 'makasih', 'keren', 'sempurna', 'selesai', 'teratasi', 'membantu', 'mantap']
}

NEGATIVE_KEYWORDS = {
    'en': ['bad', 'poor', 'unhappy', 'dissatisfied', 'terrible', 'worst', 'broken', 'not working', 'fail', 'failed', 'issue', 'problem', 'error', 'bug', 'delay', 'slow'],
    'id': ['buruk', 'jelek', 'kecewa', 'parah', 'rusak', 'tidak bekerja', 'gagal', 'masalah', 'error', 'bug', 'lambat', 'telat', 'lelet']
}

# Urgency Keywords
URGENCY_KEYWORDS = {
    'en': ['urgent', 'emergency', 'asap', 'broken', 'critical', 'immediately', 'stop', 'failed', 'down', 'dead', 'now'],
    'id': ['mendesak', 'darurat', 'segera', 'rusak', 'kritis', 'mati', 'gagal', 'down', 'sekarang', 'penting', 'cepat']
}

def analyze_sentiment(text):
    """
    Returns (sentiment_category, sentiment_score)
    Score is between -1.0 and 1.0
    """
    if not text:
        return 'neutral', 0.0

    text = text.lower()
    pos_count = 0
    neg_count = 0

    # English
    for word in POSITIVE_KEYWORDS['en']:
        pos_count += len(re.findall(r'\b' + re.escape(word) + r'\b', text))
    for word in NEGATIVE_KEYWORDS['en']:
        neg_count += len(re.findall(r'\b' + re.escape(word) + r'\b', text))

    # Indonesian
    for word in POSITIVE_KEYWORDS['id']:
        pos_count += len(re.findall(r'\b' + re.escape(word) + r'\b', text))
    for word in NEGATIVE_KEYWORDS['id']:
        neg_count += len(re.findall(r'\b' + re.escape(word) + r'\b', text))

    total = pos_count + neg_count
    if total == 0:
        return 'neutral', 0.0

    score = (pos_count - neg_count) / total
    
    if score > 0.2:
        return 'positive', score
    elif score < -0.2:
        return 'negative', score
    else:
        return 'neutral', score

def analyze_urgency(text):
    """
    Returns urgency_score (0.0 to 1.0)
    """
    if not text:
        return 0.0

    text = text.lower()
    urgency_count = 0
    words = text.split()
    if not words:
        return 0.0

    for lang in URGENCY_KEYWORDS:
        for word in URGENCY_KEYWORDS[lang]:
            urgency_count += len(re.findall(r'\b' + re.escape(word) + r'\b', text))

    # Normalize based on word count (rough estimate)
    score = min(urgency_count / 3.0, 1.0) # 3 urgent words = max urgency
    return score
