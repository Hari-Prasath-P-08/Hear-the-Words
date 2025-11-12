import re
from jiwer import wer


def clean_lyrics(text: str) -> str:
    """Clean and normalize lyrics for fair comparison.

    Steps:
    - remove any bracketed headers like [Verse 1], [Chorus], etc.
    - remove punctuation except apostrophes
    - convert to lowercase
    - collapse multiple whitespace into single spaces
    """
    # Remove section headers like [Verse 1], [Chorus], etc.
    text = re.sub(r"\[.*?\]", "", text)
    # Remove punctuation except apostrophes (keep contractions)
    text = re.sub(r"[^\w\s']", "", text)
    # Convert to lowercase
    text = text.lower()
    # Collapse whitespace
    text = re.sub(r"\s+", " ", text).strip()
    return text


# Read actual lyrics
with open("actual_lyrics/Believer_actual.txt", "r", encoding="utf-8") as f:
    actual = f.read()

# Read transcribed lyrics
with open("transcribed_lyrics/Believer_lyrics.txt", "r", encoding="utf-8") as f:
    transcribed = f.read()

# Clean both texts
actual_clean = clean_lyrics(actual)
transcribed_clean = clean_lyrics(transcribed)

# Calculate Word Error Rate (WER)
error = wer(actual_clean, transcribed_clean)
accuracy = (1 - error) * 100

print("--- Comparison summary ---")
print(f"Original actual (first 200 chars): {actual[:200]!r}")
print(f"Cleaned actual (first 200 chars): {actual_clean[:200]!r}\n")
print(f"Original transcribed (first 200 chars): {transcribed[:200]!r}")
print(f"Cleaned transcribed (first 200 chars): {transcribed_clean[:200]!r}\n")
print(f"Word Error Rate: {error:.3f}")
print(f"Accuracy Score: {accuracy:.2f}%")