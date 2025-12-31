# slugger.py
# ------------------------------------------------------------
# Convert a query or title into a safe, deterministic filename
# ------------------------------------------------------------

import re


MAX_SLUG_LENGTH = 60


def slugify(text: str, extension: str = ".txt") -> str:
    """
    Convert text into a filesystem-safe slug filename.
    """

    if not text or not text.strip():
        return f"output{extension}"

    # lowercase
    slug = text.lower()

    # remove apostrophes
    slug = slug.replace("'", "")

    # replace non-alphanumeric characters with hyphen
    slug = re.sub(r"[^a-z0-9]+", "-", slug)

    # remove leading/trailing hyphens
    slug = slug.strip("-")

    # collapse multiple hyphens
    slug = re.sub(r"-{2,}", "-", slug)

    # limit length
    slug = slug[:MAX_SLUG_LENGTH].rstrip("-")

    return f"{slug}{extension}"
