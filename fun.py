import tiktoken
def count_tokens(messages):
    encoding = tiktoken.get_encoding("cl100k_base")  # Llama 3 માટે આ સારું approximation
    total = 0
    for msg in messages:
        total += len(encoding.encode(msg["content"]))
    return total + len(messages) * 4