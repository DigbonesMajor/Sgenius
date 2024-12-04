from dotenv import load_dotenv
import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
import config as cf


def main():
    load_dotenv()
    st.set_page_config(page_title="Ask your pdf", layout="centered",initial_sidebar_state="auto")

    is_clicked = st.button("Go To Chatbot")
    if is_clicked:
        st.switch_page("🤖_Sgenius.py")

    
    st.header("Upload your pdf")
    
    # Uploading the file
    pdf = st.file_uploader("Upload your pdf", type="pdf")
    
    # Extracting the text
    if pdf is not None:
        pdf_reader = PdfReader(pdf)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()

        # Split into chunks 
        text_splitter = CharacterTextSplitter(
            separator="\n", # Defines a new line 
            chunk_size = 1000,
            chunk_overlap = 200,
            length_function = len
        )
        chunks = text_splitter.split_text(text)

        # Create embeddings
        embeddings = OpenAIEmbeddings(openai_api_key=st.secrets["api_key"])

        # Creating an object on which we will be able to search FAISS
        cf.knowledge_base = FAISS.from_texts(chunks, embeddings)

        # show user input
        user_question = st.text_input("Ask a question about the PDF: ")

        if st.button("Refresh Page"):
            st.caching.clear_cache()
            
        if user_question:
            docs = cf.knowledge_base.similarity_search(user_question)

            llm = OpenAI(openai_api_key=st.secrets["api_key"])
            chain = load_qa_chain(llm, chain_type="stuff")
            response = chain.run(input_documents=docs, question = user_question)

            st.write(response)

if __name__ == '__main__':
    main()
