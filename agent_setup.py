#agent_setup.py
from langchain.agents import initialize_agent, AgentType
from langchain_openai import ChatOpenAI
from tools import create_policy_qa_tool, create_policy_field_tool


def create_agent(vectorstore):
    llm=ChatOpenAI(model="gpt-4o-mini")

    tools=[
        create_policy_qa_tool(vectorstore), 
        create_policy_field_tool()
        ]

    agent=initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        handle_parsing_errors=True, 
        agent_kwargs={
            "prefix":"당신은 청년 정책을 한국어로 친절하게 설명해주는 전문가입니다.",
            "format_instructions":
            """생각: 문제를 분석하고 논리적으로 추론해 보세요.
            행동: 사용할 도구를 선택하세요(예: 정책분야분류기 또는 정책QA도구)
            행동 입력: 도구에 보낼 한국어 입력
            관찰: 도구의 응답
            ...(반복)
            최종 답변: 질문에 대한 최종 답변을 한국어로 작성
            
            """    
        },
        system_message="당신은 청년 정책 정보를 제공하는 한국어 전문 챗봇입니다. 모든 응답은 한국어로 작성하세요."
      #   "prefix": "",
       # "format_instructions": ""
    )
    return agent