from src.load_models import CreateModels


class CreateModelPipeline:
    def __init__(self):
        pass

    def start_embedding_model(self):
        create_models = CreateModels()
        embedding_model = create_models.create_embedding()
        return embedding_model

    def start_llm_model(self):
        create_models = CreateModels()
        gemini_model = create_models.create_gemini()
        deepseek_model = create_models.create_deepseek()
        return gemini_model, deepseek_model
