from langchain_text_splitters import RecursiveCharacterTextSplitter


"""
Splits a given document into smaller chunks using a recursive character-based text splitter.

Args:
    docs (str): The document to be split into smaller chunks.

Returns:
    list: A list of text chunks, each with a specified maximum size and overlap.
"""
def split_doc(docs: str):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, chunk_overlap=200, add_start_index=True
    )
    
    all_splits = text_splitter.split_documents(docs)
    return all_splits
