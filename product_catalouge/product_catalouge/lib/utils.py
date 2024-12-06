import re
from unicodedata import normalize


def slugify(text):
    """Convert a string into a slug."""
    text = normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    text = re.sub(r"[^a-zA-Z0-9]+", "-", text).strip("-").lower()
    return text

def generate_unique_slug(text, is_slug_unique):
    """
    Generate a unique slug for a given text.

    Args:
        text (str): The original text to convert to a slug.
        is_slug_unique (callable): A function that takes a slug and returns True if it is unique.

    Returns:
        str: A unique slug.
    """
    base_slug = slugify(text)
    slug = base_slug
    counter = 1

    while not is_slug_unique(slug):
        slug = f"{base_slug}-{counter}"
        counter += 1

    return slug