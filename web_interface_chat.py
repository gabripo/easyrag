import streamlit as st
import llm_interface
from langchain_core.messages import HumanMessage


def load_user_options():
    user_options = {}
    user_options["data_folder"] = st.secrets["data_folder"]
    user_options["llm"] = st.secrets["llm"]
    user_options["rag_folder"] = st.secrets["rag_folder"]
    user_options["system_prompt"] = st.secrets["system_prompt"]
    return user_options


def chat_actions():
    user_input = st.session_state["chat_input"]
    st.session_state["chat_history"].append({"role": "user", "content": user_input})

    user_options = load_user_options()
    with st.spinner("Thinking about an answer..."):
        llm_output = llm_interface.get_llm_response(user_input, user_options)
    st.session_state["chat_history"].append(
        {
            "role": "assistant",
            "content": llm_output,
        }
    )


def chat_actions_chat():
    user_input = st.session_state["chat_input"]
    st.session_state["chat_history"].append({"role": "user", "content": user_input})

    user_options = load_user_options()
    llm_history = st.session_state["llm_history"]
    with st.spinner("Thinking about an answer..."):
        llm_output = llm_interface.get_llm_response_chat(
            user_input, user_options, llm_history
        )
    st.session_state["chat_history"].append(
        {
            "role": "assistant",
            "content": llm_output["answer"],
        }
    )
    st.session_state["llm_history"].extend(
        [HumanMessage(content=user_input), llm_output["answer"]]
    )


st.set_page_config(page_title="Local RAG", page_icon=":robot")
st.header("Analyze local documents")

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

if st.secrets["consider_history"]:
    if "llm_history" not in st.session_state:
        st.session_state["llm_history"] = []

    st.chat_input(
        "Enter your query to Easyrag...", on_submit=chat_actions_chat, key="chat_input"
    )
else:
    st.chat_input(
        "Enter your query to Easyrag...", on_submit=chat_actions, key="chat_input"
    )

for message in st.session_state["chat_history"]:
    with st.chat_message(name=message["role"]):
        st.write(message["content"])
