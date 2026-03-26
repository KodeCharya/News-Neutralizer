import requests
from bs4 import BeautifulSoup
from typing import Optional, Tuple
import re


def extract_article_from_url(url: str) -> Optional[Tuple[str, str]]:
    """Extract article text and title from URL"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        title = soup.title.string if soup.title else url

        for script in soup(['script', 'style']):
            script.decompose()

        paragraphs = soup.find_all('p')
        text = '\n\n'.join([p.get_text() for p in paragraphs])

        text = re.sub(r'\n\s*\n', '\n\n', text)
        text = text.strip()

        if len(text) < 100:
            return None, None

        return text, title
    except Exception as e:
        print(f"Error extracting article: {e}")
        return None, None


def validate_article_text(text: str) -> Tuple[bool, str]:
    """Validate article text"""
    if not text or not text.strip():
        return False, "Article text cannot be empty"

    text = text.strip()

    if len(text) < 100:
        return False, "Article must be at least 100 characters long"

    if len(text) > 50000:
        return False, "Article is too long (max 50,000 characters)"

    return True, ""


def calculate_bias_score(biases: list) -> float:
    """Calculate overall bias score from individual biases"""
    if not biases:
        return 0.0

    total_confidence = sum(bias.get("confidence", 0.5) for bias in biases)
    avg_confidence = total_confidence / len(biases)

    base_score = avg_confidence * 100
    frequency_multiplier = min(len(biases) / 10, 1.0)

    final_score = base_score * (0.7 + 0.3 * frequency_multiplier)
    return min(max(final_score, 0), 100)


def categorize_biases(biases: list) -> dict:
    """Categorize biases by type"""
    categories = {
        "emotional": [],
        "political": [],
        "cultural": [],
        "economic": [],
        "other": []
    }

    for bias in biases:
        category = bias.get("category", "other").lower()
        if category not in categories:
            category = "other"
        categories[category].append(bias)

    return {k: v for k, v in categories.items() if v}


def format_bias_display(bias: dict) -> str:
    """Format bias for display"""
    return f"'{bias.get('term', '')}' → '{bias.get('replacement', '')}'"


def highlight_terms_in_text(text: str, terms: list) -> str:
    """Highlight terms in text with HTML markers"""
    highlighted = text
    for term in terms:
        pattern = re.compile(re.escape(term), re.IGNORECASE)
        highlighted = pattern.sub(f"<mark>{term}</mark>", highlighted)
    return highlighted


def truncate_text(text: str, max_length: int = 500) -> str:
    """Truncate text for preview"""
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."
