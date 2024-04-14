import tiktoken


class OpenAITokenSize:
    def __init__(self):
        pass

    def calc_token_size(self, model_name, string):
        encoding = tiktoken.encoding_for_model(model_name)
        num_tokens = len(encoding.encode(string))
        return num_tokens