FROM ollama/ollama:latest

WORKDIR /root/.ollama

COPY . /root/.ollama/

# expose port for communication
EXPOSE 11434

# make the ollama preparation scrip accessible within the shell
COPY ollama_start.sh /usr/local/bin/ollama_start.sh

# provide the ollama preparation script with run privileges
RUN chmod +x /usr/local/bin/ollama_start.sh

# ENTRYPOINT ["/usr/local/bin/ollama_start.sh"]