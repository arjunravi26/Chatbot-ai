import logging
from .load_data import DataIngestionPipeline
from .clean_data import DataPreProcessingPipeline
from .load_model import CreateModelPipeline
from .vector_db import CreateVectorDBPipeline
from .augment_data import AugmentPromptPipeline
class Pipeline:
    def __init__(self):
        model_pipeline = CreateModelPipeline()
        self.embedding_model = model_pipeline.start_embedding_model()


    def train(self):
        logging.info("Data Ingestion Started")
        data_ingestion_pipeline = DataIngestionPipeline()
        book,arvix = data_ingestion_pipeline.start_ingestion()
        logging.info("Data Ingestion Completed")
        logging.info("Data Preprocessing Started")
        data_cleaning_pipeline = DataPreProcessingPipeline()
        clean_book,clean_arvix = data_cleaning_pipeline.start_cleaning(book,arvix)
        logging.info("Data Preprocessing Completed")
        logging.info("Model Creation Started")

        logging.info("Data Preprocessing Completed")
        logging.info("Vector Database Creation..")
        vector_db_pipeline = CreateVectorDBPipeline(embedding_model=self.embedding_model,book=clean_book,arvix=clean_arvix)
        vector_db_pipeline.start_vectordb()
        logging.info("Vector Database Creation Completed")


    def predict(self,query,selected_model_idx,chat_history):
        augmnet_query_pipeline = AugmentPromptPipeline(embedding_model=self.embedding_model,k=3,query=query,chat_history=chat_history)
        augmnet_query,scores = augmnet_query_pipeline.start_augment_prompt()
        print(scores)
        if scores[0] < 0.4:
            return f"Sorry. I don't know about this topic."
        else:
            model_pipeline = CreateModelPipeline()
            models = model_pipeline.start_llm_model() # gemini_model, llama_model, deepseek_model
            response = models[selected_model_idx].invoke(augmnet_query)
            print(response)
            if selected_model_idx == 0:
                return response.text()
            else:
                return response
