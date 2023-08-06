from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains import ConversationalRetrievalChain
from langchain.llms import OpenAI
import pinecone
import os
from ..configuration import config

PINECONE_INDEX = os.getenv("PINECONE_INDEX")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_API_ENV = os.getenv("PINECONE_API_ENV")

class Store:
    def __init__(self) -> None:
        self.chat_history_file = {}
        self.text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        self.embeddings = OpenAIEmbeddings(openai_api_key=config._api_keys.get("OPENAI_API_KEY", None))
        pinecone.init(
          api_key=PINECONE_API_KEY,
          environment=PINECONE_API_ENV
        )

    def save(self, file_name, file_url) -> None:
        loader = PyPDFLoader(file_url)    
        document = loader.load()
        texts = self.text_splitter.split_documents(document)
        
        print(f"⏳ Saving file {file_name}")
        Pinecone.from_texts([chunk.page_content for chunk in texts], self.embeddings, index_name=PINECONE_INDEX, namespace=file_name)            


    def query(self, file_name, query, model=None) -> None:
        vectorstore = Pinecone.from_existing_index(index_name=PINECONE_INDEX, embedding=self.embeddings, namespace=file_name)
        qa = ConversationalRetrievalChain.from_llm(
            llm=OpenAI(temperature=0.7, openai_api_key=config._api_keys.get("OPENAI_API_KEY", None)), 
            retriever=vectorstore.as_retriever(),
            return_source_documents=True,
        )
        
        history = self.chat_history_file.get(file_name, None)
        if history is None:            
            history = ""
            self.chat_history_file[file_name] = []

        result =  qa({"question": query, "chat_history": history})
        self.chat_history_file[file_name].append((query, result["answer"]))
        
        return { "answer": result["answer"], "history": history }