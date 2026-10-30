"""
Conversation memory manager for MediAssist AI.
Keeps an in-memory rolling buffer of recent chat turns.
"""

from typing import List, Dict


class ConversationMemory:
    def __init__(self, max_history: int = 8):
        """
        Initialize an in-memory message history.
        :param max_history: Maximum number of individual messages (user + assistant turns)
                            to keep in context to prevent memory bloat on 8 GB RAM.
        """
        self.max_history = max_history
        self.messages: List[Dict[str, str]] = []

    def add_message(self, role: str, content: str) -> None:
        """Add a single message turn ('user' or 'assistant')."""
        self.messages.append({"role": role, "content": content.strip()})
        # Keep only the most recent messages
        if len(self.messages) > self.max_history:
            self.messages = self.messages[-self.max_history:]

    def get_messages(self) -> List[Dict[str, str]]:
        """Return the list of recorded messages."""
        return list(self.messages)

    def clear(self) -> None:
        """Reset conversation memory."""
        self.messages = []