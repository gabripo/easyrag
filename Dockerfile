FROM python:3.10.12

ENV DockerHOME=/home/easyrag
RUN mkdir -p ${DockerHOME}
WORKDIR ${DockerHOME}

# copy the whole project into the docker directory
COPY . $DockerHOME
RUN ls -l

# install dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r dependencies/requirements.txt

# port where the Streamlit engine will be available
ENV STREAMLIT_PORT=8501
EXPOSE ${STREAMLIT_PORT}/udp
EXPOSE ${STREAMLIT_PORT}/tcp

# port where the Flask application will be available
EXPOSE 3000/udp
EXPOSE 3000/tcp

# environment variables to access ollama from the container
# host.docker.internal is the name of the host machine
ENV APP_IN_DOCKER=Yes
ENV OLLAMA_API_ENDPOINT_HOST=host.docker.internal

# patch the langchain framework with the correct api endpoint
COPY patch_langchain_api_endpoint.sh /usr/local/bin/patch_langchain_api_endpoint.sh
RUN chmod +x /usr/local/bin/patch_langchain_api_endpoint.sh
RUN sh /usr/local/bin/patch_langchain_api_endpoint.sh http://localhost:11434 http://${OLLAMA_API_ENDPOINT_HOST}:11434 /usr/local/lib/python3.10/site-packages/langchain_community/embeddings/ollama.py
RUN sh /usr/local/bin/patch_langchain_api_endpoint.sh http://localhost:11434 http://${OLLAMA_API_ENDPOINT_HOST}:11434 /usr/local/lib/python3.10/site-packages/langchain_community/llms/ollama.py


ENTRYPOINT [ "python" ]
CMD ["flask_app/easyrag_flask.py"]