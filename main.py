# main.py

from policy_data_loader import load_policy_documents
from agent_setup import create_agent

def main():
    print("청년 정책 챗봇을 시작합니다...")
    vectorstore = load_policy_documents()
    agent = create_agent(vectorstore)
    

    while True:
        user_input = input("질문을 입력하세요 (종료하려면 'exit'): ")
        if user_input.lower() == "exit":
            break
        response = agent.run(user_input)
        print("🤖 답변:", response)

if __name__ == "__main__":
    main()
