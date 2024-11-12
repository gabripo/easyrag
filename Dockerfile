FROM python:3.10.12

ENV DockerHOME=/home/easyrag
RUN mkdir -p ${DockerHOME}
WORKDIR ${DockerHOME}

# copy the whole project into the docker directory
COPY . $DockerHOME

# install dependencies
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r dependencies/requirements.txt

# port where the Streamlit engine will be available
EXPOSE 8501

CMD python main.py