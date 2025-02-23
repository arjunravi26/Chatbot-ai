import re


class DataPreprocessing:
    def __init__(self):
        pass

    def clean_arvix(self, X):
        chunk = X.apply(lambda x: re.sub(r'[^a-zA-Z0-9.\s]', '', x))
        chunk = chunk.apply(lambda x: re.sub(r'[\x00-\x1F\x7F]', ' ', x))
        chunk = chunk.apply(lambda x: re.sub(r'\s+', ' ', x))
        chunk = chunk.apply(lambda x: re.sub(r'\s+([,.!?;:])', r'\1', x))
        chunk = chunk.apply(lambda x: re.sub(r'([,.!?;:])(?=\S)', r'\1 ', x))
        chunk = chunk.apply(lambda x: re.sub(r'\{', '-', x))
        chunk = chunk.apply(lambda x: re.sub(r'\}', '', x))
        chunk = chunk.apply(lambda x: x.strip())
        return chunk

    def clean_book_data(self, X):
        X = re.sub(r'[^A-Za-z0-9.]', ' ', X)
        pattern_chapter = r'^\d+\s+Chapter\s+\d+\s+.*?'
        X = re.sub(pattern_chapter, '', X, count=1)
        pattern_section = r'^\s+Section\s+\d+\s+.*?'
        pattern_section = r'^Section\s+\d+(?:\.\d+)?\s+.*?'
        X = re.sub(pattern_section, '', X, count=1)
        return X
