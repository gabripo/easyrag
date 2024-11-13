import requests
import json


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


def download_model(llm_name: str) -> bool:
    url = "http://localhost:11434/api/pull"
    headers = {"Content-Type": "application/json"}
    data = {"name": llm_name}
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        return True
    return False
