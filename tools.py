#tools.py

from langchain.tools import Tool

from langchain.chains import RetrievalQA, LLMChain
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
#from langchain_chroma import Chroma
from langchain_community.vectorstores import Chroma
from prompt_template import policy_prompt

#1. RAG 기반 정책 질문 응답 RAG Tool
def create_policy_qa_tool(vectorstore:Chroma):
    llm=ChatOpenAI(model="gpt-4o-mini")

    qa_chain=RetrievalQA.from_chain_type(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        chain_type_kwargs={"prompt":policy_prompt}
    )
    print(f"policy_prompt: {policy_prompt}")
    return Tool(
        name="YouthPolicyQA",
        func=qa_chain.run,
        description="청년 정책(일자리, 주거, 교육 등)에 대한 질문에 답변합니다."
    )

#2. 질문에서 정책 분야 분류 Tool
def create_policy_field_tool():
    llm=ChatOpenAI(model="gpt-4o-mini")

    classify_prompt= PromptTemplate(
            input_variables=["question"],
                    template="""
 아래 질문은 청년 정책 관련 질문입니다.
 질문을 읽고 다음중 하나의 정책 분야를 저왁히 분류하세요:
 [일자리, 주거, 교육, 복지문화, 참여권리]
 
 질문: {question}
종책 분야:"""
            )
    chain= LLMChain(llm=llm, prompt=classify_prompt)
    return Tool(
            name="PolicyFieldClassifier",
            func=chain.run,
            description="질문을 읽고 청년 정책 분야(일자리, 주거, 교육 등)를 분류합니다. 예: '청년 임대주택 지원은 어떤 분야야?'"
    )
 