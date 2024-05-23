import easyrag_gui
import llm_interface

if __name__ == "__main__":
    user_options = easyrag_gui.ui_get_options()
    while easyrag_gui.ui_check_options(user_options):
        user_query = easyrag_gui.ui_get_query()
        answer = llm_interface.get_llm_response(user_query, user_options)
        easyrag_gui.ui_print(answer, "RAG response")
        if not easyrag_gui.ui_yes_no("Continue with the queries?"):
            break
