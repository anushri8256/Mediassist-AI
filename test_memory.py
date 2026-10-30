from memory import ConversationMemory

memory = ConversationMemory()

memory.add_message("user", "Hello")
memory.add_message("assistant", "Hello! How can I help you?")
memory.add_message("user", "I have a headache.")

print(memory.get_messages())