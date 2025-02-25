import re


class DataPreprocessing:
    def __init__(self):
        pass


def clean_data(X):
    # 1. Remove Chapter/Section Headings (All Occurrences)
    X = re.sub(r'^\d+\s+Chapter\s+\d+\s+.*?\n', '', X, flags=re.MULTILINE)
    X = re.sub(r'^Section\s+\d+(?:\.\d+)?\s+.*?\n', '', X, flags=re.MULTILINE)

    # 2. Be More Selective with Special Character Removal
    X = re.sub(r'[^A-Za-z0-9.,;:\(\)\{\}\[\]\+\-\*/=<>%&\|\^\$#@~\n]', ' ', X)  # Keep newlines!

    # 3. Handle Code Blocks (Example - Keep them as separate chunks)
    code_blocks = re.findall(r"```.*?```", X, re.DOTALL)  # Extract code blocks
    X = re.sub(r"```.*?```", "", X, re.DOTALL)      # Remove code blocks from main text

    # 4. Remove extra whitespace (optional)
    X = re.sub(r'\s+', ' ', X).strip()
    return X
