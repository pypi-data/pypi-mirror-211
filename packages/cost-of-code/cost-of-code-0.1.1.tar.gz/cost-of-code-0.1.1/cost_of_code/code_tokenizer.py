from tiktoken import encoding_for_model

enc = encoding_for_model("gpt-4")


def tokenize_code(code):
    return len(enc.encode(code))
