import re
from datetime import datetime
import pytz
from flask import session
from slugify import slugify

def get_uzbek_timezone():
    """Get Tashkent timezone"""
    return pytz.timezone('Asia/Tashkent')

def format_uzbek_date(date_obj):
    """Format date for Uzbek locale"""
    if not date_obj:
        return ""
    
    tz = get_uzbek_timezone()
    if date_obj.tzinfo is None:
        date_obj = tz.localize(date_obj)
    else:
        date_obj = date_obj.astimezone(tz)
    
    # Uzbek month names
    uzbek_months = {
        1: "yanvar", 2: "fevral", 3: "mart", 4: "aprel",
        5: "may", 6: "iyun", 7: "iyul", 8: "avgust",
        9: "sentabr", 10: "oktabr", 11: "noyabr", 12: "dekabr"
    }
    
    day = date_obj.day
    month = uzbek_months[date_obj.month]
    year = date_obj.year
    time = date_obj.strftime("%H:%M")
    
    return f"{day}-{month}, {year}-yil, {time}"

def get_current_language():
    """Get current language from session"""
    return session.get('language', 'uz')

def translate_text(text_uz, text_ru=None):
    """Return text based on current language"""
    lang = get_current_language()
    if lang == 'ru' and text_ru:
        return text_ru
    return text_uz

def create_excerpt(content, length=150):
    """Create excerpt from content"""
    if not content:
        return ""
    
    # Remove HTML tags
    clean_content = re.sub(r'<[^>]+>', '', content)
    
    # Truncate and add ellipsis
    if len(clean_content) <= length:
        return clean_content
    
    return clean_content[:length].rsplit(' ', 1)[0] + "..."

def generate_slug(title):
    """Generate URL-friendly slug"""
    return slugify(title)

def clean_uzbek_text(text):
    """Clean and normalize Uzbek text"""
    if not text:
        return ""
    
    # Replace common characters
    replacements = {
        "'": "'",
        """: '"',
        """: '"',
        "–": "-",
        "—": "-",
        "…": "...",
    }
    
    for old, new in replacements.items():
        text = text.replace(old, new)
    
    return text.strip()

def format_uzbek_number(number):
    """Format number in Uzbek style"""
    if not number:
        return "0"
    
    return f"{number:,}".replace(",", " ")

def format_uzbek_currency(amount):
    """Format currency in UZS"""
    if not amount:
        return "0 so'm"
    
    formatted = format_uzbek_number(int(amount))
    return f"{formatted} so'm"

def validate_uzbek_phone(phone):
    """Validate Uzbek phone number"""
    # Remove all non-digits
    cleaned = re.sub(r'\D', '', phone)
    
    # Check if it matches Uzbek phone patterns
    patterns = [
        r'^998[0-9]{9}$',  # +998xxxxxxxxx
        r'^[0-9]{9}$',     # xxxxxxxxx
    ]
    
    for pattern in patterns:
        if re.match(pattern, cleaned):
            return True
    
    return False

def format_uzbek_phone(phone):
    """Format Uzbek phone number"""
    cleaned = re.sub(r'\D', '', phone)
    
    if len(cleaned) == 9:
        return f"+998 {cleaned[:2]} {cleaned[2:5]} {cleaned[5:7]} {cleaned[7:9]}"
    elif len(cleaned) == 12 and cleaned.startswith('998'):
        return f"+{cleaned[:3]} {cleaned[3:5]} {cleaned[5:8]} {cleaned[8:10]} {cleaned[10:12]}"
    
    return phone

def get_uzbek_regions():
    """Get list of Uzbek regions"""
    return [
        'Toshkent shahri',
        'Toshkent viloyati',
        'Samarqand',
        'Buxoro',
        'Andijon',
        'Farg\'ona',
        'Namangan',
        'Qashqadaryo',
        'Surxondaryo',
        'Xorazm',
        'Navoiy',
        'Jizzax',
        'Sirdaryo',
        'Qoraqalpog\'iston'
    ]

def get_popular_uzbek_keywords():
    """Get popular Uzbek keywords for SEO"""
    return [
        "o'zbekiston yangiliklar",
        "toshkent shahar yangiliklar",
        "uzbekistan news",
        "markaziy osiy",
        "iqtisodiyot uzbekistan",
        "sport yangiliklar uzbekistan",
        "texnologiya uzbekistan",
        "madaniyat uzbekistan",
        "ta'lim uzbekistan",
        "siyosat uzbekistan"
    ]

def calculate_reading_time(content):
    """Calculate estimated reading time"""
    if not content:
        return 0
    
    # Average reading speed: 200 words per minute for Uzbek
    word_count = len(content.split())
    reading_time = max(1, round(word_count / 200))
    
    return reading_time

def sanitize_html(content):
    """Basic HTML sanitization"""
    if not content:
        return ""
    
    # Allow only safe HTML tags
    allowed_tags = ['p', 'br', 'strong', 'em', 'u', 'a', 'ul', 'ol', 'li', 'h2', 'h3', 'h4']
    
    # This is a basic implementation - in production, use bleach or similar
    return content

def generate_meta_description(content, max_length=155):
    """Generate meta description from content"""
    if not content:
        return ""
    
    # Remove HTML tags
    clean_content = re.sub(r'<[^>]+>', '', content)
    
    # Get first sentences up to max_length
    sentences = clean_content.split('. ')
    description = ""
    
    for sentence in sentences:
        if len(description + sentence + '. ') <= max_length:
            description += sentence + '. '
        else:
            break
    
    return description.strip()

def is_uzbek_text(text):
    """Check if text is in Uzbek language"""
    if not text:
        return False
    
    # Check for common Uzbek characters and patterns
    uzbek_chars = set("o'gʻx'GQQO'Ğ'Ч")
    uzbek_words = ['va', 'bilan', 'uchun', 'ning', 'dan', 'ga', 'ni']
    
    # Check for Uzbek-specific characters
    has_uzbek_chars = any(char in uzbek_chars for char in text)
    
    # Check for common Uzbek words
    words = text.lower().split()
    has_uzbek_words = any(word in uzbek_words for word in words)
    
    return has_uzbek_chars or has_uzbek_words

def format_file_size(size_bytes):
    """Format file size in human readable format"""
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB"]
    import math
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    
    return f"{s} {size_names[i]}"

class UzbekTextProcessor:
    """Class for processing Uzbek text"""
    
    def __init__(self):
        self.stop_words = [
            'va', 'yoki', 'lekin', 'ammo', 'shuning', 'uchun', 'bilan',
            'ning', 'dan', 'ga', 'ni', 'bu', 'shu', 'o\'sha', 'har',
            'hech', 'ba\'zi', 'boshqa', 'ko\'p', 'oz', 'juda', 'ancha'
        ]
    
    def remove_stop_words(self, text):
        """Remove stop words from text"""
        words = text.lower().split()
        filtered_words = [word for word in words if word not in self.stop_words]
        return ' '.join(filtered_words)
    
    def extract_keywords(self, text, max_keywords=10):
        """Extract keywords from text"""
        # Remove stop words
        filtered_text = self.remove_stop_words(text)
        
        # Get word frequency
        words = filtered_text.split()
        word_freq = {}
        
        for word in words:
            if len(word) > 3:  # Only consider words longer than 3 characters
                word_freq[word] = word_freq.get(word, 0) + 1
        
        # Sort by frequency and return top keywords
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        return [word for word, freq in sorted_words[:max_keywords]]
