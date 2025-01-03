import chardet
from sentence_transformers import SentenceTransformer, util
from langchain.text_splitter import RecursiveCharacterTextSplitter
import pickle

def detect_encoding(filename):
    with open(filename, 'rb') as file:
        raw_data = file.read()
        result = chardet.detect(raw_data)
        return result['encoding']

def load_text(filename):
    encoding = detect_encoding(filename)
    with open(filename, 'r', encoding=encoding) as file:
        return file.read()

def split_text(text, chunk_size=1000, chunk_overlap=100):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    chunks = text_splitter.split_text(text)
    return chunks
    # return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]


# Load the books and split them into chunks
book1 = load_text("./Knowledge_base_books/01 - The Fellowship Of The Ring.txt")
book2 = load_text("./Knowledge_base_books/02 - The Two Towers.txt")
book3 = load_text("./Knowledge_base_books/03 - The Return Of The King.txt")

book1_chunks = split_text(book1)
book2_chunks = split_text(book2)
book3_chunks = split_text(book3)

# combine all book chunks
context = book1_chunks + book2_chunks + book3_chunks

## Creating vector embeddings
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

knowledge_embeddings = [
    # (" ".join(chunk), embedding_model.encode(" ".join(chunk)))  # Join chunks of paragraphs and encode
    (chunk, embedding_model.encode(chunk))
    for chunk in context
]
with open('knowledge_embeddings.pkl', 'wb') as f:
    pickle.dump(knowledge_embeddings, f)
