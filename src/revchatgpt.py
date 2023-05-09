from revChatGPT.V3 import Chatbot
from tiktoken.core import Encoding
from tiktoken.registry import get_encoding


def encoding_for_model(model_name: str) -> Encoding:
    """Simplified Returns the encoding used by a model. (Only works for chatgpt and gpt4)"""
    encoding_name = "cl100k_base"
    return get_encoding(encoding_name)


# inherits from the Chatbot class
class CustomChatbot(Chatbot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # override the ask method
    def get_token_count(self, convo_id: str = "default") -> int:
        """
        Get token count
        """
        if self.engine not in ["gpt-3.5-turbo", "gpt-3.5-turbo-0301", "gpt-4", "gpt-4-0314"]:
            print()
            raise NotImplementedError(f"Unsupported engine {self.engine}")

        encoding = encoding_for_model(self.engine)

        num_tokens = 0
        for message in self.conversation[convo_id]:
            # every message follows <im_start>{role/name}\n{content}<im_end>\n
            num_tokens += 4
            for key, value in message.items():
                num_tokens += len(encoding.encode(value))
                if key == "name":  # if there's a name, the role is omitted
                    num_tokens += 1  # role is always required and always 1 token
        num_tokens += 2  # every reply is primed with <im_start>assistant
        return num_tokens