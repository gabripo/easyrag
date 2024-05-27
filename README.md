# Easyrag - The one-click minimal solution to analyze documents

## What is it?
_Easyrag_ is a small tool to perform a RAG (Retrieval-Augmented Generation) over documents which are stored locally.

## Typical use case
1. I have big, boring, important documents stored on my PC.
2. I do not want to give these documents away.
3. ... yet I am not willing to waste hours reading the documents.
4. Then I give these documents to _Easyrag_ !
5. _Easyrag_ will process the documents, without being bored.
6. I ask _Easyrag_ questions to get an insight about the documents.
7. I am happy: I saved a lot of time!

## Installation
1. Install Ollama - https://ollama.com/
2. Download the Meta AI llama3 model (8b-parameter version used in this guide): `ollama download llama3-8b`
3. Install Python - https://www.python.org/downloads/
4. Install conda - please refer to the official website https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html
5. By using a shell, create a conda environment by using the provided dependencies:
```
conda env create -f dependencies/environment.yml -n easyrag
```
6. To use the web interface, install streamlit - https://docs.streamlit.io/get-started/installation

## Usage
1. Activate the just created conda environment:
```
conda activate easyrag
```
2. By using Python, run the `main.py` file:
```
python main.py
```
3. Follow the instructions in the GUI
  - ![Screenshot 2024-05-24 at 16 06 35](https://github.com/gabripo/easyrag/assets/25492636/bad5c7f7-4a01-4a4a-b906-1d48e9036d8f)
  - Select the folder with documents by using the _Browse_ button.
  - Edit the _System prompt_ as you wish: it will be the preamble for all your following queries - you can ask _Easyrag_ to behave as a scientist, as a teacher, as your cousin, ...
### Chatbot in the browser - requires streamlit
Tick the "Use web interface" and click on the "Submit" button to use the web interface (please note that this functionality requires streamlit to be installed!):
  - A web interface with your web browser will start: provide it with one query and press "Enter" to submit a question.
  - ![Screenshot 2024-05-25 at 10 45 45](https://github.com/gabripo/easyrag/assets/25492636/7928f505-3c5e-406f-8e94-8c181a296551)
  - To stop submitting queries, click "Yes" in the window that pops up.
  - ![Screenshot 2024-05-24 at 16 16 54](https://github.com/gabripo/easyrag/assets/25492636/c2c09abf-5376-4970-898f-c72a23d24e0c)
### Queries using the GUI
Click on the "Submit" button without ticking "Use web interface" to proceed using the GUI for queries and answers:
  - Edit the text to talk to _Easyrag_ .
  - ![Screenshot 2024-05-23 at 21 24 00](https://github.com/gabripo/easyrag/assets/25492636/7109ebd1-6817-484d-bd36-9b46d40e32ff)
  - Confirm with the "Submit" button to let _Easyrag_ process the documents.
  - Be patient. Your response will come soon!
  - ![Screenshot 2024-05-23 at 21 26 51](https://github.com/gabripo/easyrag/assets/25492636/16b149d9-83ef-4ae9-9005-f2a295c39825)
  - After closing the window, it is possible to provide _Easyrag_ with other queries by clicking on the "Yes" button. To abort, click on the "No" button, instead.
  - ![Screenshot 2024-05-23 at 21 29 29](https://github.com/gabripo/easyrag/assets/25492636/0f5a8000-cc73-4503-bf7a-47f385ecf614)



## Current status and limitations
1. Only the llama3 ( https://ollama.com/library/llama3 ) model is currently supported. Other models may come in the future - if I will get more spare time.
2. As Ollama runs on Linux / MacOS only, Windows is not supported - no problem since you are a Geek, right?
3. Be patient at the first analysis of the documents: _Easyrag_ has to go through all the documents, let it read them!
4. If the documents have been already analyzed, then the following queries after the first one are faster (TLDR: the Chroma database is loaded and not re-generated).
5. Only `.pdf` documents are supported. `.xls` and other spreadsheet files may come soon...
6. The GUI is not the best on earth, I know... I used `pysimplegui` to have more free time to develop the backend.
7. The prompts after the very first one consider the entire history of messages - the previous queries and answers.

# Contacts
1. Do you want to contact me about collaborations? Write me to gabriele.giardino.ing@gmail.com
2. Do you want to contact me about bugs? Same e-mail adress as before.
