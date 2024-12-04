from dotenv import load_dotenv
from PIL import Image
from langchain_core.messages import AIMessage, HumanMessage
import streamlit as st
from streamlit_extras.switch_page_button import switch_page
import config as cf
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain


im = Image.open("Societe-Generale-Emblem.png")


st.set_page_config(page_title="Chat With SGenius",page_icon=im)

# Custom HTML/CSS for the banner
custom_html = """
<div>
    <img src="chatbot-logo.png" style='height: 100%; width: 100%; object-fit: contain'>
</div>
<style>
    .banner {
        border-style: solid;
        border-width: thin;
        border-color: #FFFFFF;
    }
</style>

"""
# Display the custom HTML
#st.components.v1.html(custom_html)
st.image("chatbot-logo.png")




if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
      AIMessage(content="Hello! I'm your SGenius assistant. Ask me any query about the Company policy"),
    ]

load_dotenv()

with st.sidebar:
    st.subheader("Settings")
    st.write("LogIn as Admin to upload documents")
    adm = st.text_input("Host",value="")
    st.text_input("Password",value="******")
    is_clicked = st.button("connect")

if is_clicked:
    if(adm=="Admin"):
        switch_page("Upload")

for message in st.session_state.chat_history:
    if isinstance(message, AIMessage):
        with st.chat_message("AI", avatar=im):
            st.markdown(message.content)
    elif isinstance(message, HumanMessage):
        with st.chat_message("Human"):
            st.markdown(message.content)

user_query = st.chat_input("Type your Message:")

if user_query is not None and user_query.strip() != "":
    st.session_state.chat_history.append(HumanMessage(content=user_query))
    
    with st.chat_message("Human", avatar="🤔"):
        st.markdown(user_query)
        
    with st.chat_message("AI", avatar=im):

        if " hi " in user_query or " Hi " in user_query:
            response = "Hello! How are you doing"
            st.markdown(response)
        else:
            docs = cf.knowledge_base.similarity_search(user_query)

            llm = OpenAI(openai_api_key=st.secrets["api_key"])
            chain = load_qa_chain(llm, chain_type="stuff")
            response = chain.run(input_documents=docs, question = user_query)

            st.markdown(response)
        
    st.session_state.chat_history.append(AIMessage(content=response))
