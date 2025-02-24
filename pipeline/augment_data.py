from src.augument_prompt import AugmentPrompt

class AugmentPromptPipeline:
    def __init__(self,embedding_model, query,chat_history, k=3):
        self.k = k
        self.query = query
        self.chat_history = chat_history
        self.embedding_model = embedding_model
        self.pc_name = "ai-chatbot"

    def start_augment_prompt(self):
        augmentprompt_obj = AugmentPrompt(query=self.query,embedding_model=self.embedding_model)
        augmentprompt_obj.load_vector_db()
        contexts,scores = augmentprompt_obj.extract_contexts()
        augment_prompt = augmentprompt_obj.augment_prompt(self.query,contexts,chat_history=self.chat_history)
        return augment_prompt,scores