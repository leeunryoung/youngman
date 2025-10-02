# main.py
from fastapi import FastAPI, Query
from pydantic import BaseModel
from policy_data_loader import load_policy_documents
from agent_setup import create_agent
import uvicorn

#서버 초기화
app=FastAPI()
vectorstore=load_policy_documents()
agent=create_agent(vectorstore)

# 입력 데이터 스키마 정의
class QueryRequest(BaseModel):
    question: str
#메인 질의 API
# @app.post("/ask")
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
     uvicorn.run("main:app", host="0.0.0.0", port=8022, reload=True)