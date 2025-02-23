from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain_huggingface import HuggingFaceEndpoint
from langchain_google_genai import ChatGoogleGenerativeAI


class CreateModels:
    def __init__(self):
        pass

    def create_embedding(self):
        model_name = 'sentence-transformers/all-MiniLM-L6-v2'
        embedding_model = SentenceTransformerEmbeddings(model_name=model_name)
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

    def create_llama(self):
        repo_id = "meta-llama/Llama-3.3-70B-Instruct"
        llama_model = HuggingFaceEndpoint(
            repo_id=repo_id,
            top_k=10,
            top_p=0.95,
            temperature=0.6,
            task='text-generation',
            repetition_penalty=1.03
        )
        return llama_model

    def create_deepseek(self):
        deepseek_repo = "deepseek-ai/deepseek-llm-67b-base"
        deepseek_model = HuggingFaceEndpoint(
            repo_id=deepseek_repo, task='text-generation',
            temperature=0.7,
            top_p=0.9,
            top_k=50
        )
        return deepseek_model
