import re
from unicodedata import normalize
from typing import Callable


def slugify(text:str):
    """Convert a string into a slug."""
    text = normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    text = re.sub(r"[^a-zA-Z0-9]+", "-", text).strip("-").lower()
    return text

def generate_unique_slug(text:str, is_slug_unique:Callable):
    """Generate a unique slug for a given text."""
    base_slug = slugify(text)
    slug = base_slug
    counter = 1

    while not is_slug_unique(slug):
        slug = f"{base_slug}-{counter}"
        counter += 1

    return slug