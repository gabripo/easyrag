import os
import chromadb
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings

def build_database(docs_path='', model_name='llama3', db_folder_path='', persistent_db=True) -> Chroma:
    if not docs_path:
        print("Unspecified documents path!")
        pass
    if model_name == 'llama3':
        embedding_model_function = OllamaEmbeddings(model=model_name)
    else:
        print("Unsupported model " + model_name)
        pass
    if not db_folder_path:
        db_folder_path = os.path.join(docs_path, 'chroma_data')

    data = []
    for file in os.listdir(docs_path):
        if file.endswith(".pdf"):
            single_pdf_path = os.path.join(docs_path, file)
            loader = PyPDFLoader(single_pdf_path)
            data.extend(loader.load())

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=0)
    split_documents = text_splitter.split_documents(data)

    client = chromadb.Client()
    if client.list_collections():
        print("Creating new collection")
        consent_collection = client.create_collection("consent_collection")
    else:
        print("Collection already exists")
    vector_db = Chroma.from_documents(
        documents=split_documents,
        embedding=embedding_model_function,
        persist_directory=db_folder_path,
    )

    if persistent_db:
        vector_db.persist()
    return vector_db

def load_database_from_folder(db_folder_path='', model_name='llama3') -> Chroma:
    if not db_folder_path:
        print("Unspecified database path!")
        pass
    elif not os.path.exists(db_folder_path):
        print("Folder " + db_folder_path + "does not exist!")
        pass
    if model_name == 'llama3':
        embedding_model_function = OllamaEmbeddings(model=model_name)
    else:
        print("Unsupported model " + model_name)
        pass

    vector_db = Chroma(
            persist_directory=db_folder_path,
            embedding_function=embedding_model_function,
        )
    return vector_db