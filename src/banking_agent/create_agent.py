from banking_agent.services.agent import create_banking_agent


def main():
    agent = create_banking_agent()

    print("Agent created successfully")
    print(f"Name: {agent.name}")
    print(f"Version: {agent.version}")


if __name__ == "__main__":
    main()