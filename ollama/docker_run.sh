#! /bin/bash

docker run -d -v ollama:/root/.ollama -p 11434:11434 --name ollama_local docker-ollama