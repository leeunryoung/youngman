#prompt_template.py
from langchain.prompts import PromptTemplate

policy_prompt= PromptTemplate(
    input_variables=["context", "question"],
    template="""
너는 청년 정책을 설명해주는 AI야.

다음은 참고 문서야: 
{context}
청확하고 친절하게 답변해줘
"""
    )
