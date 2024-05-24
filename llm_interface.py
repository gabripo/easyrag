import os
import database_manager
import chat_model
from langchain.schema.runnable import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser


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
        | chat_model.load_chat_model()
        | StrOutputParser()
    )
    answer = chat_chain.invoke(query)
    return answer
