"""
this is an offline script for chunking, embedding and writing to `embeddings.json`

> this runs once to write embeddings.json
"""

import json
import os

from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter


def main():
    # loading docs from "knowledge_base" dir
    loader = DirectoryLoader(
        path="./knowledge_base", glob="*.md", loader_cls=TextLoader
    )
    docs = loader.load()

    # chunking the docs (either for limited context window purposes, or inject only relevant chunks into the prompt...)
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(docs)

    if not os.path.exists("./embeddings.json"):
        with open("./embeddings.json", "w") as f:
            # the next step is to embed those chunks, therefor we need an embedding model.
            # TODO (research): how does an embedding model, convert an object to a vector of numbers that hold semantic traits of the objects.
            embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-V2")
            embeddings = embedding_model.embed_documents(
                [chunk.page_content for chunk in chunks]
            )

            # write to the json file "embeddings.json"
            nodes = []
            for i in range(len(embeddings)):
                nodes.append(
                    {
                        "id": i,
                        "text": chunks[i].page_content[:50],
                        "vector": embeddings[i],
                        "source": chunks[i].metadata["source"].split("/")[-1],
                    }
                )
            json.dump(nodes, f, indent=4)


if __name__ == "__main__":
    main()
