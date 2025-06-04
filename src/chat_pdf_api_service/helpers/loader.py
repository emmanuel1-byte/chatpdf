from langchain_community.document_loaders import PyPDFLoader
from fastapi import UploadFile
import os
import tempfile


"""
Load a PDF document from an uploaded file.

This function reads a PDF file from an UploadFile object, temporarily saves it
to disk, and uses the PyPDFLoader to load and parse the document. The temporary
file is removed after loading.

Args:
    file (UploadFile): The uploaded file object containing the PDF.

Returns:
    list: A list of documents parsed from the PDF.
"""
def load_document(file: UploadFile):
    file.file.seek(0)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tf:
        while chunk := file.file.read(1024 * 1024):  # 1MB chunks
            tf.write(chunk)
        tf_path = tf.name

    try:
        loader = PyPDFLoader(tf_path)
        docs = loader.load()
    finally:
        os.remove(tf_path)

    return docs
