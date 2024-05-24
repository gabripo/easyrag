import streamlit as st
import llm_interface
import easyrag_gui

user_options = {}
user_options["data_folder"] = st.secrets["data_folder"]
user_options["llm"] = st.secrets["llm"]
user_options["rag_folder"] = st.secrets["rag_folder"]
user_options["system_prompt"] = st.secrets["system_prompt"]

st.set_page_config(page_title="Local RAG", page_icon=":robot")
st.header("Analyze local documents")

user_input = st.text_input("Enter the query about the local documents")
submit_button = st.button("Submit query")

if submit_button:
    st.write(llm_interface.get_llm_response(user_input, user_options))
