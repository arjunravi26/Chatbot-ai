from langchain_huggingface import HuggingFaceEmbeddings
from langchain_huggingface.llms import HuggingFaceEndpoint
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

import os


class CreateModels:
    def __init__(self):
        load_dotenv()  # This loads variables from .env into the environment

        self.hf_token = os.getenv('HF_TOKEN')
        if self.hf_token is None:
            raise ValueError("HF_TOKEN is not set in the environment.")

    def create_embedding(self):
        model_name = 'sentence-transformers/all-MiniLM-L6-v2'
        embedding_model = HuggingFaceEmbeddings(model_name=model_name)
        return embedding_model

    def create_gemini(self):
        gemini_model = ChatGoogleGenerativeAI(
            model="gemini-1.5-pro",
            temperature=0,
            max_tokens=None,
            timeout=None,
            max_retries=2,
        )
        return gemini_model


    def create_deepseek(self):
        deepseek_repo = "deepseek-ai/DeepSeek-R1-Distill-Qwen-32B"
        deepseek_model = HuggingFaceEndpoint(
            huggingfacehub_api_token = self.hf_token,
            repo_id=deepseek_repo, task='text-generation',
            temperature=0.7,
            top_p=0.9,
            top_k=50
        )
        return deepseek_model
