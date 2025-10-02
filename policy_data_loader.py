# policy_data_loader.py
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_community.document_loaders import TextLoader


from langchain.text_splitter import CharacterTextSplitter

import os
from dotenv import load_dotenv

# .env 파일에서 환경 변수 로드
load_dotenv()

def load_policy_documents():
    # 정책 문서 폴더
    folder_path = "./policy_docs"

    # 문서 로드 및 분할
    docs = []
    splitter = CharacterTextSplitter(chunk_size=600, chunk_overlap=100)
    for filename in os.listdir(folder_path):
        path = os.path.join(folder_path, filename)
        loader = TextLoader(path, encoding="utf-8")
        raw_docs = loader.load()
        docs.extend(splitter.split_documents(raw_docs))

    # Chroma 벡터 DB 저장
    vectorstore = Chroma.from_documents(
        documents=docs,
        embedding=OpenAIEmbeddings(model="text-embedding-3-small"),
        persist_directory="./chroma_db"

        
    )
    vectorstore.persist()
    return vectorstore
