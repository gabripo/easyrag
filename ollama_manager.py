import requests


def list_available_models() -> set[str]:
    url = "http://localhost:11434/api/tags"
    response = requests.get(url)
    if response.status_code == 200:
        models = response.json()
        model_names = {model["name"].split(":")[0] for model in models["models"]}
        return model_names
    else:
        return {}


def is_llm_available(llm_name: str) -> bool:
    return llm_name in list_available_models()
