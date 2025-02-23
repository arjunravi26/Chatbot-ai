import pandas as pd
import logging
from datasets import load_dataset
from langchain_community.document_loaders import PyPDFDirectoryLoader


class DataIngestion:
    def __init__(self):
        pass

    def load_arvix_data(self):
        dataset_name = "jamescalam/llama-2-arxiv-papers-chunked"
        try:
            data = load_dataset(path=dataset_name, split="train")
        except Exception as e:
            logging.info(f"Error in data loading from datasets {e}")
        return data.to_pandas()

    def load_book_pdf(self):
        pdf_folder = "../Data/"
        try:
            pdf_loader = PyPDFDirectoryLoader(pdf_folder)
            pdf_documents = pdf_loader.load()
        except FileNotFoundError as e:
            logging.info(f"Error from data loading from pdf {e}")
        return pd.DataFrame([{'source': doc.metadata['source'], 'page_label': doc.metadata['page_label'], 'text': doc.page_content}for doc in pdf_documents[19:1073]])
