from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)
from langchain.schema import SystemMessage
from langchain_pinecone.vectorstores import PineconeVectorStore
from pinecone import Pinecone
import os


class AugmentPrompt:
    def __init__(self, embedding_model, query, k=3):
        self.k = k
        self.query = query
        self.embedding_model = embedding_model
        self.pc_name = "ai-chatbot"

    def load_vector_db(self):
        self.pc_index = Pinecone(os.getenv('PINECONE_API')).Index(self.pc_name)

    def extract_contexts(self):
        vectorstore = PineconeVectorStore(
            self.pc_index, embedding=self.embedding_model, text_key='chunk')

        results = vectorstore.similarity_search_with_score(
            query=self.query)
        contexts,scores = map(list, zip(*results))
        return contexts,scores

    def augment_prompt(self, user_query, contexts):

        system_msg = SystemMessage(
            content=(
                "You are a highly knowledgeable AI expert specializing in Artificial Intelligence, "
                "machine learning, and Deep Learning. Answer questions with detailed, clear, and technically accurate explanations. "
                "Always provide examples or analogies when they help clarify complex topics."
            )
        )

        human_msg_template = HumanMessagePromptTemplate.from_template(
            "{user_query}")

        chat_history_placeholder = MessagesPlaceholder(
            variable_name="chat_history")

        user_msg_template = HumanMessagePromptTemplate.from_template(
            "{contexts}")

        chat_prompt = ChatPromptTemplate.from_messages([
            system_msg,
            chat_history_placeholder,
            human_msg_template,
            user_msg_template,
        ])

        formatted_prompt = chat_prompt.format(
            user_query=user_query,
            chat_history=[],
            contexts=contexts
        )

        return formatted_prompt
