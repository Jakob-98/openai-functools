class Conversation:
    def __init__(self):
        self.conversation_history = []

    def add_message(self, role, content, function_name=None):
        # conditionally build message:
        if function_name is None:
            message = {"role": role, "content": content}
        else:
            message = {
                "role": role,
                "content": content,
                "name": function_name,
            }
        self.conversation_history.append(message)

    def display_conversation(self):
        for message in self.conversation_history:
            print(f"{message['role']}: {message['content']}\n\n")

    def display_last_message(self):
        last_message = self.conversation_history[-1]
        print(f"{last_message['role']}: {last_message['content']}\n\n")
