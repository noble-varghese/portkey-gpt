import streamlit as st
from llama_index import VectorStoreIndex, ServiceContext, Document
from llama_index.llms import OpenAI
from llama_index import SimpleDirectoryReader, load_index_from_storage


def load_data():
    reader = SimpleDirectoryReader(input_dir="./data", recursive=True)
    docs = reader.load_data()
    service_context = ServiceContext.from_defaults(
        llm=OpenAI(
            model="gpt-3.5-turbo", temperature=0.5,
            system_prompt="You are an expert on the Portkey - An LLM gateway application and your job is to answer technical questions. Assume that all questions are related to the Portkey. Keep your answers technical and based on facts – do not hallucinate features. If you think you don't know the answer then reply with 'Iam not sure about the answer. Please give more details.'"))
    index = VectorStoreIndex.from_documents(docs, service_context=service_context)
    return index


index = load_data()
index.storage_context.persist("./.portkey_index")
