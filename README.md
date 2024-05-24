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
2. Download the Meta AI llama3 model: `ollama download llama3-8b`
3. Install Python - https://www.python.org/downloads/
4. Install conda - please refer to the official website https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html
5. By using a shell, create a conda environment by using the provided dependencies:
```
conda env create -f dependencies/environment.yml -n easyrag
```

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
- ![Screenshot 2024-05-23 at 21 20 09](https://github.com/gabripo/easyrag/assets/25492636/163be97f-529a-4685-b13a-c6818ebc4a32)
- Select the folder with documents by using the _Browse_ button.
- Edit the _System prompt_ as you wish: it will be the preamble for all your following queries - you can ask _Easyrag_ to behave as a scientist, as a teacher, as your cousin, ...
- Click on the _Submit_ button to proceed.
- ![Screenshot 2024-05-23 at 21 24 00](https://github.com/gabripo/easyrag/assets/25492636/7109ebd1-6817-484d-bd36-9b46d40e32ff)
- Edit the text to talk with _Easyrag_ .
- Confirm with the _Submit_ button to let _Easyrag_ process the documents.
- Be patient. Your response will come soon!
- ![Screenshot 2024-05-23 at 21 26 51](https://github.com/gabripo/easyrag/assets/25492636/16b149d9-83ef-4ae9-9005-f2a295c39825)
- After closing the window, it is possible to provide _Easyrag_ with other queries by clicking on the _Yes_ button. To abort, click on the _No_ button, instead.
- ![Screenshot 2024-05-23 at 21 29 29](https://github.com/gabripo/easyrag/assets/25492636/0f5a8000-cc73-4503-bf7a-47f385ecf614)

## Current status and limitations
1. Only the llama3 ( https://ollama.com/library/llama3 ) model is currently supported. It means everything can run offline on your machine! Other models may come in the future - if I will get more spare time.
2. As Ollama runs on Linux / MacOS only, Windows is not supported - no problem since you are a Geek, right?
3. Be patient at the first analysis of the documents: _Easyrag_ has to go through all the documents, let it read!
4. If the documents have been already analyzed, then the following queries after the first one are faster (TLDR: the Chroma database is loaded and not re-generated)
5. Only `.pdf` documents are supported. `.xls` and other spreadsheet files may come soon...
6. The GUI is not the best on earth, I know... I used `pysimplegui` to have more free time to develop the backend.
7. A web interface with `streamlit` may come. One day...

# Contacts
1. Do you want to contact me about collaborations? Write me to gabriele.giardino.ing@gmail.com
2. Do you want to contact me about bugs? Same e-mail adress as before.

