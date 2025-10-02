# main.py
from fastapi import FastAPI, Query
from pydantic import BaseModel
from policy_data_loader import load_policy_documents
from agent_setup import create_agent
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
#서버 초기화
app=FastAPI()

origins = [
    "null",  # 파일을 직접 열 때의 Origin
    "file://",  # 일부 브라우저에서 사용
    "http://localhost:8000",  # 기존 설정 유지
    "http://127.0.0.1:8000",  # 기존 설정 유지
]
# CORS 허용 (필요 시)
app.add_middleware(
    CORSMiddleware,
    # allow_origins=["*"],  # 배포 시엔 도메인 제한 권장
    allow_origins=origins,  # 쿠키 전달 때문에 명시
    allow_credentials=True,  # 없으면 쿠키가 무시됨
    allow_methods=["*"],
    allow_headers=["*"],
)


vectorstore=load_policy_documents()
agent=create_agent(vectorstore)

# 입력 데이터 스키마 정의
class QueryRequest(BaseModel):
    question: str
#메인 질의 API
@app.post("/ask")
def ask_question(query: QueryRequest):
    try:
        response= agent.run(query.question)     
        return{"answer": response}
    except Exception as e:
        return {"error": str(e)}

#루트 페이지
@app.get("/")
def root():
    return {"message":"정년정책 챗봇 API입니다. POST /ask 로 질문하세요."}

if __name__=="main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)


