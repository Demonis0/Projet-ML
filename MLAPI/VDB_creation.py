import os

from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceBgeEmbeddings

from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import PyPDFLoader

os.environ['TOKENIZERS_PARALLELISM'] = 'false'


documents = []
docs_path = "docs"
persist_directory = 'Loras_doc'  # this is the directory in which we'll store our vector database
embedding_f = HuggingFaceBgeEmbeddings(
    model_name="BAAI/bge-base-en-v1.5",
    model_kwargs={"device": "cpu"},
    encode_kwargs={"normalize_embeddings": True})

loader = TextLoader("LORAS.txt")
documents.extend(loader.load())


with open('temporaryF.txt', 'w') as file:
    co = ''
    file.write(co)

with open('temporary.txt', 'w') as file:
    content = ''
    for i in range(len(documents)):
        content += documents[i].page_content
        word_count = len(content.split())
    file.write(content)

k = 1
size = 4000
while size > 2500:
    k += 1
    size = word_count/k

# so now we have even sizes for the rough chunking, we can proceed to chunk.
t_docs = []
with open('temporary.txt', 'r') as file:
    content_T = ''
    for line in file:
        w_count = len(content_T.split())
        if w_count < size:
            # hope this simple condition will be good enough, but if most docs have hyper long lines...
            content_T += line
        else:
            t_docs.append(content_T)
            content_T = ''

    # After the loop, check if there is any remaining content to be added
    if content_T.strip():  # This ensures we don't add empty strings
        t_docs.append(content_T)

print(len(t_docs))


# Now that I have the dividers, I can write them in the second text file.
with open('temporaryF.txt', 'a') as file:
    content = ''
    for j in range(len(t_docs)):
        content += t_docs[j]
    file.write(content)

text_chunks = []
with open('temporaryF.txt', 'r') as file:
    content = file.read()
    # Split the content by '-o-' to separate into chunks
    text_chunks = content.split('-o-')

text_chunks = [chunk.strip() for chunk in text_chunks]


class Document:
    def __init__(self, page_content, metadata=None):
        self.page_content = page_content
        self.metadata = metadata


documents = [Document(page_content=chunk) for chunk in text_chunks]


vdb = Chroma.from_documents(
    documents=documents,
    embedding=embedding_f,
    persist_directory=persist_directory,
    collection_metadata={"hnsw:space": "cosine"}
    )

vdb.persist()
