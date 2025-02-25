import spacy
from transformers import AutoTokenizer

class Chunking:
    def __init__(self):
        self.nlp = spacy.load("en-core-web-sm")
        self.tokenizer = AutoTokenizer('bert-base-uncased')
    def chunking(self,text,chunk_size=256,overlap=50):
        chunks = []
        current_length = 0
        doc = self.nlp(text)
        current_chunk = []
        for sent in doc.sents:
            sent_length = len(self.tokenizer.tokenize(sent))
            if current_length + sent_length <=chunk_size:
                current_chunk.append(sent.text)
                current_length += sent_length
            else:
                if self.chunks:
                    prev_tokens = self.tokenizer.tokenize(chunks[-1])
                    prev_tokens =  prev_tokens[-overlap]
                    print(prev_tokens)
                    overlap_text = ' '.join(prev_tokens)
                    chunks.append(current_chunk)
                    current_length = sent_length
                    current_chunk = [sent.text]
            return chunks