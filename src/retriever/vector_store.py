import faiss
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_community.vectorstores import FAISS
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings



class vectorStoreRetriever:

    def __init__(self, structured_data):
        self.embedding_model = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2")
        self.structured_data = structured_data
        self.embeddings = self.embedding_generation(structured_data)
        self.vector_store, self.ids = self.vector_store_interaction(
            self.embeddings)

    def embedding_generation(self, structured_data):
        embeddings = self.embedding_model.embed_documents(
            [row['content'] for row in structured_data])
        return embeddings

    def vector_store_interaction(self, embeddings):
        embedding_dim = len(embeddings[0])
        print("embedding_dim:", embedding_dim)

        index = faiss.IndexFlatL2(embedding_dim)
        vector_store = FAISS(
            embedding_function=self.embedding_model,
            index=index,
            docstore=InMemoryDocstore(),
            index_to_docstore_id={},
        )
        ids = vector_store.add_texts([row['content']
                                     for row in self.structured_data])
        return vector_store, ids
