def load_as_text(path):
    with open(path, 'r') as f:
        text = f.read()
        return text