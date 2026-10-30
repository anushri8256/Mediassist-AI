from chat_engine import ChatEngine

chatbot = ChatEngine()

print("\nMediAssist is ready!")
print("Type 'exit' to stop.\n")

while True:
    user_message = input("You: ")

    if user_message.lower() == "exit":
        break

    response = chatbot.chat(user_message)

    print(response)