import time
import os
import tqdm
from pinecone import Pinecone, ServerlessSpec


class VectorDB:
    def __init__(self, embedding_model, book, arvix, batch_size=100):
        self.embedding_model = embedding_model
        self.book = book
        self.arvix = arvix
        self.index_name = "ai-chatbot"
        self.pc_index = None
        self.batch_size = batch_size

    def create_vectordb(self):
        pc = Pinecone(os.getenv('PINECONE_API'))
        index_list = [idx['name'] for idx in pc.list_indexes()]
        if self.index_name not in index_list:
            pc.create_index(name=self.index_name, spec=ServerlessSpec(
                cloud='aws', region='us-east-1'), dimension=384)
        timeout = 60
        start_time = time.time()
        while not pc.describe_index(self.index_name).status['ready']:
            if time.time() - start_time > timeout:
                raise TimeoutError("Timeout")
            time.sleep(1)
        self.pc_index = pc.Index(self.index_name)

    def insert_pdf(self):
        status = self.pc_index.describe_index_stats()
        if status['total_vector_count'] == 0:
            for i in tqdm(range(0, len(self.book), self.batch_size)):
                i_end = min(i+self.batch_size, len(self.book))
                batch = self.book[i:i_end]
                ids = batch['id'].astype(str).to_list()
                chunks = batch['chunk'].to_list()
                embed_chunk = self.embedding_model.encode(chunks)
                metadata = batch[['id', 'chunk']].to_dict(orient='records')
                self.pc_index.upsert(vectors=list(
                    zip(ids, embed_chunk, metadata)))
        else:
            print('Already Inserted data')

    def insert_arvix(self):
        status = self.pc_index.describe_index_stats()
        if status.get('total_vector_count', 0) <= 1054:
            for i in tqdm(range(0, len(self.arvix), self.batch_size)):
                i_end = min(len(self.arvix), i + self.batch_size)
                batch = self.arvix[i:i_end]
                ids = (batch['doi'].astype(str) + '-' +
                       batch['chunk-id'].astype(str)).to_list()
                chunk = batch['chunk'].to_list()
                embeds = self.embedding_model.encode(chunk)
                meta_data = batch[['chunk', 'source', 'title']
                                  ].to_dict(orient='records')
                self.pc_index.upsert(vectors=list(zip(ids, embeds, meta_data)))
        else:
            print("Alredy Created")
