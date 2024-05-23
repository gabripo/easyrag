import streamlit as st
import llm_interface
import easyrag_gui
import sys

# TODO: pass the LLM user options to streamlit
# user_options = easyrag_gui.ui_get_options()
user_options = {}

if not easyrag_gui.ui_check_options(user_options):
    print("Invalid user options!")
    pass

st.set_page_config(page_title="Local RAG", page_icon=":robot")
st.header("Analyze local documents")

user_input = st.text_input("Enter the query about the local documents")
submit_button = st.button("Submit query")

if submit_button:
    st.write(llm_interface.get_llm_response(user_input, user_options))
