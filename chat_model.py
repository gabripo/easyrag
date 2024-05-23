from langchain.prompts import (
    PromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    ChatPromptTemplate,
)
from langchain_community.llms import Ollama

def compose_llm_prompt(sys_prompt='') -> ChatPromptTemplate:
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

def load_chat_model(model_name='llama3'):
    if not model_name:
        print("Empty model to load!")
        pass
    elif model_name != 'llama3':
        print("Unsupported model " + model_name)
        pass
    # TODO: Support multiple models
    chat_model = Ollama(model=model_name)
    return chat_model