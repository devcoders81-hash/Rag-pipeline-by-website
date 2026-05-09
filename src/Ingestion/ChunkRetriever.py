from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
def ExtractWeb(url):
    loader = WebBaseLoader(url)

    docs = loader.load()
    #print(docs[0].page_content[:500])
    return docs
    
def ChunkContent(docs):
    text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=800,
    chunk_overlap=150
    )

    chunks = text_splitter.split_documents(docs)

    print(len(chunks))
    print(chunks[2].page_content)
    return chunks