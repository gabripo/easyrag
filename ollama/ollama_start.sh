#! /bin/bash

echo "Starting Ollama server..."
ollama serve &

echo "Waiting for Ollama server to be active..."
while [ "$(ollama list | grep 'NAME')" == "" ]; do
  sleep 1
done
echo "Ollama server is now active!"

echo "Pulling nomic embedder ..."
ollama pull nomic-embed-text
echo "Pull of nomic embedder completed"

# pull llama3.2 - 3B parameters
echo "Pulling llama3.2 ..."
ollama pull llama3.2
echo "Pull of llama3.2 completed"

ollama list