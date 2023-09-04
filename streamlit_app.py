import streamlit as st
from llama_index import VectorStoreIndex, ServiceContext, Document
from llama_index.llms import OpenAI
import openai
import os
from llama_index import SimpleDirectoryReader, StorageContext, load_index_from_storage

st.set_page_config(page_title="Chat with the Portkey docs, powered by LlamaIndex",
                   page_icon="🦙", layout="centered", initial_sidebar_state="auto", menu_items=None)
openai.api_key = os.environ.get('OPENAI_API_KEY')
st.title("Chat with the Portkey docs, powered by LlamaIndex 💬🦙")

if "messages" not in st.session_state.keys():  # Initialize the chat messages history
    st.session_state.messages = [
        {"role": "assistant",
         "content": "Ask me a question about Portkey's "}]


# Rebuild storage context
storage_context = StorageContext.from_defaults(persist_dir="./.portkey_index")

# Load index from the storage context
index = load_index_from_storage(storage_context)

# system_prompt="You are an expert on the Portkey LLM gateway and your job is to answer technical questions. Assume that all questions are related to the Portkey. Keep your answers technical and based on facts – do not hallucinate features."
chat_engine = index.as_chat_engine(chat_mode="condense_question", verbose=True)

if prompt := st.chat_input("Your question"):  # Prompt for user input and save to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

for message in st.session_state.messages:  # Display the prior chat messages
    with st.chat_message(message["role"]):
        st.write(message["content"])

# If last message is not from assistant, generate a new response
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = chat_engine.chat(prompt)
            st.write(response.response)
            message = {"role": "assistant", "content": response.response}
            st.session_state.messages.append(message)  # Add response to message history
