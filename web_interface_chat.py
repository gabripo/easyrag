import streamlit as st
import llm_interface


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


st.set_page_config(page_title="Local RAG", page_icon=":robot")
st.header("Analyze local documents")

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

st.chat_input(
    "Enter your query to Easyrag...", on_submit=chat_actions, key="chat_input"
)

for message in st.session_state["chat_history"]:
    with st.chat_message(name=message["role"]):
        st.write(message["content"])
