import easyrag_gui
import llm_interface
import streamlit as st
import process_handler
import streamlit_settings
from langchain_core.messages import HumanMessage
import os

if __name__ == "__main__":
    user_options = easyrag_gui.ui_get_options()

    if easyrag_gui.ui_check_options(user_options) and user_options["use_web_interface"]:
        streamlit_settings.write_streamlit_secrets(user_options)
        streamlit_script = "web_interface_chat.py"
        streamlit_cmd = f"streamlit run --server.port {os.getenv('STREAMLIT_PORT', '8501')} " + streamlit_script
        streamlit_pid = process_handler.execute_command_and_get_pid(streamlit_cmd)

        while True:
            kill_streamlit = easyrag_gui.ui_yes_no("Close the streamlit engine?")
            if kill_streamlit:
                process_handler.kill_process_by_pid(streamlit_pid)
                break
    else:
        while easyrag_gui.ui_check_options(user_options):
            user_query = easyrag_gui.ui_get_query()
            if user_options["consider_history"]:
                chat_history = []
                llm_output = llm_interface.get_llm_response_chat(
                    user_query, user_options, chat_history
                )
                answer = llm_output["answer"]

                chat_history.extend(
                    [HumanMessage(content=user_query), llm_output["answer"]]
                )
            else:
                answer = llm_interface.get_llm_response(user_query, user_options)
            easyrag_gui.ui_print(answer, "RAG response")
            if not easyrag_gui.ui_yes_no("Continue with the queries?"):
                break
