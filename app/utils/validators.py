import re

def is_valid_instruction(text: str) -> bool:
    if not text or not text.strip():
        return False
    
    words = re.findall(r"[a-zA-Z]+", text)
    return len(words) >= 3

def generate_title(text: str, max_words: int = 6) -> str:
    words = text.split()[:max_words]
    title = " ".join(words)
    return title.capitalize() if title else "Untitled"
