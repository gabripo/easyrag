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
EXPOSE 8501/udp
EXPOSE 8501/tcp

# port where the Flask application will be available
EXPOSE 3000/udp
EXPOSE 3000/tcp

# environment variables for Ollama
ENV OLLAMA_HOST=0.0.0.0:11434
ENV OLLAMA_ORIGINS=http://0.0.0.0:11434

ENTRYPOINT [ "python" ]
CMD ["flask_app/easyrag_flask.py"]