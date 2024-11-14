import requests
import json
import os


def ollama_api_endpoint() -> str:
    if os.getenv("APP_IN_DOCKER") == "Yes":
        if os.getenv("APP_IN_DOCKER_COMPOSE") == "Yes":
            return os.getenv("OLLAMA_API_ENDPOINT_CONTAINER", "")
        else:
            return os.getenv("OLLAMA_API_ENDPOINT_HOST", "")
    else:
        # execution on host
        return "localhost"


def ollama_api_base_url(port: str = "11434") -> str:
    api_endpoint = ollama_api_endpoint()
    return f"http://{api_endpoint}:{port}"


def list_available_models() -> set[str]:
    url = f"{ollama_api_base_url()}/api/tags"
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
    url = f"{ollama_api_base_url()}/api/pull"
    headers = {"Content-Type": "application/json"}
    data = {"name": llm_name}
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        return True
    return False
