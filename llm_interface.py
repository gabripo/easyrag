import os
import database_manager
import chat_model
from langchain.schema.runnable import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from ollama_manager import is_llm_available


def get_llm_response(query, user_options={}):
    if os.path.exists(user_options["rag_folder"]):
        print("Using already available database at path " + user_options["rag_folder"])
        vector_db = database_manager.load_database_from_folder(
            db_folder_path=user_options["rag_folder"], model_name=user_options["llm"]
        )
    else:
        vector_db = database_manager.build_database(
            docs_path=user_options["data_folder"],
            model_name=user_options["llm"],
            db_folder_path=user_options["rag_folder"],
        )

    num_tokens_to_consider = 3
    retriever = vector_db.as_retriever(k=num_tokens_to_consider)

    chat_chain = (
        {"context": retriever, "query": RunnablePassthrough()}
        | chat_model.compose_llm_prompt(user_options["system_prompt"])
        | chat_model.load_chat_model(model_name=user_options["llm"])
        | StrOutputParser()
    )
    answer = chat_chain.invoke(query)
    return answer


def get_llm_response_chat(query, user_options={}, chat_history=[]):
    llm_name = user_options["llm"]
    if is_llm_available(llm_name):
        if os.path.exists(user_options["rag_folder"]):
            print(
                "Using already available database at path " + user_options["rag_folder"]
            )
            vector_db = database_manager.load_database_from_folder(
                db_folder_path=user_options["rag_folder"], model_name=llm_name
            )
        else:
            vector_db = database_manager.build_database(
                docs_path=user_options["data_folder"],
                model_name=llm_name,
                db_folder_path=user_options["rag_folder"],
            )

        num_tokens_to_consider = 3
        retriever = vector_db.as_retriever(k=num_tokens_to_consider)

        llm_model = chat_model.load_chat_model(model_name=llm_name)
        contextualizer = chat_model.contextualize_system_prompt(llm_model, retriever)
        qa_chain = chat_model.create_question_answer_chain(
            llm_model, user_options["system_prompt"]
        )
        chat_chain = chat_model.create_rag_chain(contextualizer, qa_chain)

        answer = chat_chain.invoke({"input": query, "chat_history": chat_history})
        return answer
    else:
        return {
            "answer": f"Model {llm_name} is not available! Install it with Ollama before running Easyrag.\n"
        }
