from langchain.prompts import (
    PromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
    MessagesPlaceholder,
)
from langchain_community.llms import Ollama
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from ollama_manager import ollama_api_base_url


def compose_llm_prompt(sys_prompt="") -> ChatPromptTemplate:
    template_str_sys_prompt = sys_prompt + """\n{context}"""
    template_sys_prompt = SystemMessagePromptTemplate(
        prompt=PromptTemplate(
            input_variables=["context"],
            template=template_str_sys_prompt,
        )
    )
    template_human_prompt = HumanMessagePromptTemplate(
        prompt=PromptTemplate(
            input_variables=["query"],
            template="{query}",
        )
    )
    message_to_llm = [template_sys_prompt, template_human_prompt]
    llm_prompt = ChatPromptTemplate(
        input_variables=["context", "query"],
        messages=message_to_llm,
    )
    return llm_prompt


def load_chat_model(model_name="llama3"):
    if not model_name:
        print("Empty model to load!")
        pass
    # TODO: Support multiple models
    chat_model = Ollama(model=model_name)
    chat_model.base_url = ollama_api_base_url()
    print(f"Used Ollama model: {model_name} with endpoint {chat_model.base_url}")
    return chat_model


"""Additional functions to have model calls which consider chat history"""


def contextualize_system_prompt(llm, retriever):
    contextualize_q_system_prompt = """Given a chat history and the latest user question \
    which might reference context in the chat history, formulate a standalone question \
    which can be understood without the chat history. Do NOT answer the question, \
    just reformulate it if needed and otherwise return it as is."""
    contextualize_q_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", contextualize_q_system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )
    history_aware_retriever = create_history_aware_retriever(
        llm, retriever, contextualize_q_prompt
    )
    return history_aware_retriever


def create_question_answer_chain(llm, sys_prompt=""):
    qa_system_prompt = sys_prompt + """\n{context}"""
    qa_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", qa_system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )

    question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)
    return question_answer_chain


def create_rag_chain(history_aware_retriever, question_answer_chain):
    rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)
    return rag_chain
