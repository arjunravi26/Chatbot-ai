import spacy
from transformers import AutoTokenizer

class Chunking:
    def __init__(self):
        self.nlp = spacy.load("en-core-web-sm")
        self.tokenizer = AutoTokenizer('bert-base-uncased')

    def dynamic_chunking(self,text, max_token=512, overlap=50):
        doc = self.nlp(text)
        chunks = []
        current_chunk = []
        token_length = 0
        # overlap_text = ""

        for sent in doc.sents:
            curr_length = len(self.tokenizer.tokenize(sent.text))

            if curr_length + token_length <= max_token:
                current_chunk.append(sent.text)
                token_length += curr_length
            else:
                if current_chunk:
                    chunks.append(' '.join(current_chunk))  # Save current chunk
                    # prev_tokens = tokenizer.tokenize(' '.join(current_chunk))
                    # overlap_tokens = prev_tokens[-overlap:]
                    # overlap_text = tokenizer.convert_tokens_to_string(overlap_tokens)

                # Start new chunk with overlap
                # current_chunk = [overlap_text, sent.text] if overlap_text else [sent.text]
                current_chunk = [sent.text]
                token_length = len(self.tokenizer.tokenize(' '.join(current_chunk)))  # Update length

        if current_chunk:
            chunks.append(' '.join(current_chunk))  # Append last chunk

        return chunks