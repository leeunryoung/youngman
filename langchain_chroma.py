pip install langchain-chroma #Chroma 통합 라이브러리
pip install langchain-community # 다양한 통합을 위한 기본 라이브러리
pip install pydantic==1.10.13 # ChromaDB와  특정 Pydantic 버전 호환성 문제 해결을 위해 명시적으로 설치
pip install unstructured #문서 로딩에 사용될 수 있는 라이브러리(필요시) pdf, docx 등 다양한 형식의 문서를 로드하고 파싱하는데 유용한-
pip openai # 예제에서 임베딩 모델로 OpenAI를 사용한다면 필요 (예: text-embedding-ada-002)을 사용하여 텍스트를 벡터로 변환하려면 
#문서로드 및 분할(Text Loading & Splitting) 벡터db에 저장할 text data를 준비한다. 긴문서를 작은 청크(chunk)로 분할하여 벡터화하는것이 
                                                                #                                       효율적이다.
                                                                                                   # 이 라이브러리가 필요
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
# 텍스트 파일 로드(예시: "state_of_the_union.txt"파일이 있다고 가정)
# TextLoader는 간단한 텍스트 파일을 로드하는 데 사용됨.
loader= TextLoader("state_of_the_union.txt")
docs = loader.load()

# 문서 분할기 초기화
#RecursiveCharacterTextSplitter는 다양한 구분자(newline, space 등)를 사용하여 텍스트를 재귀적으로 분할합니다.
#chunk_size는 각 청크의 최대 문자 수, chunk_overlap은 인접한 청크 간의 겹치는 문자수 입니다.
text_splitter = RecursivecharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
# 문서 분할 실행
splits = text_splitter.split_documents(docs)
#주석:
# - 문서 분할은 임베딩 모델의 토큰 제한을 고려하고, 검색 관련성을 높이는 데 중요합니다.
# - chunk_size와 chunk_overlap은 애플리케이션의 특성에 따라 최적화될 수 있다.
# - 다른 로더(예: PyPDFLoader CSVLoader 등)을 사용하여 다양한 형식의 문서를 로드할 수 있습니다.
#임베딩모델 선택 및 초기화
#텍스트를 고차원 벡터(숫자배열)로 변환한느 임베딩 모델을 선택하고 초기화함. 이벡터는 텍스트의 의미론적 유사성을 나타냄.
from langchain_openai import OpenAIEmbeddings
import os
#OpenAI API 키 설정(환경 변수 사용 권장)
#os.environ["OPENAI_API_KEY"]= "YOUR_API_KEY"
#OpenAI 임베딩 모델 초기화
#text-embedding-ada-002는 OpenAI의 대표적인 임베딩 모델입니다.
embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
# 주석 :
# -  OpenAIEmbeddings 외에도 SentenceTransformers, CohereEmbeddings 등 다양한 임베딩 모델을 사용할 수 있다.
# - 로컬에서 실행 가능한 임베딩 모델(예: SentenceTransformers)을 사용하면  API 키 없어도 사용할 수 있다.
# - 임베딩 모델의 선택은 검색 정확도와 비용에 영향을 미칩니다.
#chroma 벡터 db생성 및 저장 
#준비된 문서 청크와 임베딩 모델을 사용하여chroma db를 생성하고  데이터를 저장.
from langchain_chroma import Chroma
#Chroma 벡터 DB 생성
#from_documents 메서드는 문서 청크와 임베딩 모델을 사용하여 벡터 DB를 구축합니다.
#persist_directory는 벡터 DB를  저장할 로컬 경로입니다.
#이 경로에 chromaDB의 데이터가 저장되므로, 애플리케이션을 다시 시작해도 데이터를 유지할 수 있다.
vectorstore=Chroma.from_documents(
    documents=splits,
    embedding=embeddings,
    persist_directory="./chroma_db"# 데이터를 저장할 디렉토리 지정
)
# 데이터베이스 영구 저장(명시적으로 호출하는 것이 좋습니다.)
# persist() 메서드를 호출해야 데이터가 지정된 persist_directory에 실제로 저장됩니다.
 vectorstore.persist()
 print("Chroma DB가 'chroma_db' 디렉토리에 성공적으로 저장되었습니다.")

 #주석:
 # - persist_directory를 지정하지 않으면 ChromaDB는 인메모리(in-memory)로 동작하며, 애플리케이션 종료시 데이터가 사람짐.
 # - `from_documents`외에도 `add_texts` 등을 사용하여 텍스트를 추가할 수 있습니다.
 #Chroma 벡터 테이터베이스 로드 및 질의
 #저장된 Chroma 데이터베이스를 로드하고, 질의(query)를 통해 유사한 문서를 검색합니다.
 from langchain_chroma import Chroma
 from langchain_openai import OpenAIEmbeddings
 import os
 #OpenAI API 키 설정(환경 변수 사용 권장)
 # os.environ["OPENAI_API_KEY"]="YOUR_API_KEY"
 # 임베딩 모델 초기화(DB 생성 시 사용했던 모델과 동일해야 함)
 