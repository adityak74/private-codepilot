"""Embeddings Client"""

import time
import threading
from langchain_community.document_loaders import GitLoader
from langchain_community.embeddings import OllamaEmbeddings
from langchain.chains import RetrievalQA
from langchain_chroma import Chroma
from langchain_text_splitters import CharacterTextSplitter
from private_codepilot.core.config import Config
from private_codepilot.util.hashing_helpers import md5_of_list


class EmbeddingsClient:
    """Embeddings Client"""

    def __init__(self):
        """Initialize the client and connect to the embeddings service"""
        self.app_config = Config().app_config
        self.vector_store = None
        self.embedding_function = OllamaEmbeddings(
            base_url=self.app_config.OLLAMA_URL,
            model=self.app_config.OLLAMA_EMBEDDING_MODEL,
        )
        self.text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
        self.git_loader = GitLoader(
            repo_path=self.app_config.REPO_DIR, branch=self.app_config.REPO_GIT_BRANCH
        )
        self.current_document_hash = None
        self.stop_background_thread = False
        self.background_thread = threading.Thread(target=self._hash_computation_loop)
        self.background_thread.daemon = True
        self.background_thread.start()

    def generate_embeddings(self):
        """Generate Embeddings"""
        if self.vector_store is None:
            documents = self.git_loader.load()
            docs = self.text_splitter.split_documents(documents)
            self.current_document_hash = md5_of_list(docs)
            self.vector_store = Chroma(
                embedding_function=self.embedding_function,
                persist_directory=self.app_config.PERSIST_DIR,
            ).from_documents(documents=docs, embedding=self.embedding_function)
        else:
            self.vector_store = Chroma(
                embedding_function=self.embedding_function,
                persist_directory=self.app_config.PERSIST_DIR,
            )

    def get_qa_chain_interface(self, llm_interface):
        """Get QA Chain Interface"""
        self.generate_embeddings()
        return RetrievalQA.from_chain_type(
            llm_interface, retriever=self.vector_store.as_retriever()
        )

    def should_update_embeddings(self):
        """Should update embeddings"""
        if self.current_document_hash is None:
            return True
        documents = self.git_loader.load()
        docs = self.text_splitter.split_documents(documents)
        new_hash = md5_of_list(docs)
        if new_hash != self.current_document_hash:
            return True
        return False

    def _hash_computation_loop(self):
        """Continuously compute the hash every 10 seconds wait for 10 seconds to start"""
        time.sleep(10)  # sleep 10 seconds and then start the thread to avoid race condition
        while not self.stop_background_thread:
            self.update_document_hash()
            time.sleep(10)

    def update_document_hash(self):
        """Update the document hash"""
        documents = self.git_loader.load()
        docs = self.text_splitter.split_documents(documents)
        new_hash = md5_of_list(docs)
        if new_hash != self.current_document_hash:
            self.current_document_hash = new_hash
            self.vector_store = Chroma(
                embedding_function=self.embedding_function,
                persist_directory=self.app_config.PERSIST_DIR,
            ).from_documents(documents=docs, embedding=self.embedding_function)

    def stop_hash_computation(self):
        """Stop the background hash computation thread"""
        self.stop_background_thread = True
        self.background_thread.join()
