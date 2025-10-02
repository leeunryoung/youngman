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
        max_iterations=3,
        agent_kwargs={
            "prefix":"You are an expert assistant for Korean youth policies. Answer all questions in Korean. Use the YouthPolicyQA tool once to get information and immediately provide the final answer.",
        }
    )
    return agent