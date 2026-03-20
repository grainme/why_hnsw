import json
import os

from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

"""



"""

embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-V2")
queries = [
    "best response to e4",
    "how to attack the king in the middlegame",
    "what is a fork in chess",
    "how do pawns affect the position",
    "endgame technique with rooks",
]


# load vector from embedding.json
def load_embeddings_from_json():
    with open("embeddings.json", "r") as f:
        data = json.load(f)
        return data


def main():
    loader = DirectoryLoader(path="knowledge_base", glob="*.md", loader_cls=TextLoader)
    splitter = RecursiveCharacterTextSplitter(chunk_size=200, chunk_overlap=30)

    documents = loader.load()
    chunks = splitter.split_documents(documents)

    if not os.path.exists("embedding.json"):
        vectors = embedding_model.embed_documents(
            [chunk.page_content for chunk in chunks]
        )

        with open("embeddings.json", "w") as f:
            data = []
            for i in range(len(chunks)):
                data.append(
                    {
                        "id": i,
                        "text": chunks[i].page_content,
                        "vector": vectors[i],
                        "source": chunks[i].metadata["source"].split("/")[-1],
                    }
                )
            # json.load() to read...
            json.dump(data, f, indent=4)


if __name__ == "__main__":
    main()
