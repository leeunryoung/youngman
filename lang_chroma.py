from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
import os
os.environ["OPENAI_API_KEY"] = "YOUR_OPENAI_API_KEY" # 실제 API키로 대체
#문서불러오기->쪼개기->임베딩생성-> Chroma에 저장
#문서 로딩
loader=TextLoader("sample.txt", encoding="usf-8")
documents=loader.load()
#문서쪼개기
text_splitter= CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
docs = text_splitter.split_documents(documents)
#임베딩 생성기  준비
embedding = OpenAIEmbeddings()
#Chroma에 저장
vectordb=Chroma.from_documents(docs, embedding, persist_directory="./chroma_db")
vectordb.persist()
#질문-응답 시스템 구성(Retrieval+GPT)
#저장된 DB 불러오기
vectordb=Chroma(persist_directory="./chroma_db", embedding_function=embedding)
#LLM 준비
llm= OpenAI(temperature=0)
#Retrieval + QA 체인 구성
qa_chain= RetrievalQA.from_chain_type(
    llm=llm,
    retriever=vectordb.as_retriever(),
    chain_type="stuff"
)
#질문 실행
query="이 문서에서 핵심 내용이 뭐야?"
result= qa_chain.run(query)
print(result)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    
#전체 구조 요약
#graph TD; A[문서]--> B[Text Splitter]; ,l00p
# B --> C[OpenAI Embeddings]; 
# C --> D[Chroma DB]; 
# E[사용자 질문]--> F[Retriever]; 
# F-->D; D-->G[관련 문서 반환];
# G-->H[OpenAI LLM]; 
# H-->I[최종 응답]


