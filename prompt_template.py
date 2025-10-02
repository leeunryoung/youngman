#prompt_template.py
from langchain.prompts import PromptTemplate

policy_prompt= PromptTemplate(
    input_variables=["context", "question"],
    template="""너는 청년 정책을 설명해주는 AI야.

다음은 참고 문서야:
{context}

질문: {question}

위 참고 문서를 바탕으로 질문에 대해 정확하고 친절하게 답변해줘.
참고 문서에 관련 정보가 없으면 "해당 정보를 찾을 수 없습니다"라고 답변해줘.

답변:"""
    )
