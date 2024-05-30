import chromadb

from . import shell

class Retriever:
    def __init__(self, chroma_collection: str, chroma_host: str = "localhost", chroma_port: int = 8000):
        self.chroma_server_ip = chroma_host
        self.chroma_port = chroma_port
        self.client = chromadb.HttpClient(host=chroma_host, port=chroma_port)
        shell.print_green_message(f"ChromaDB client connected to {chroma_host}")
        self.chroma_collection = self.client.get_collection(chroma_collection)
        shell.print_green_message(f"ChromaDB collection loaded: {chroma_collection}")

    def retrieve(self, query, n_results=5):
        response = self.chroma_collection.query(query_texts=[query], n_results=n_results)
        ids = response["ids"][0]
        metadatas = response["metadatas"][0]
        dates = [x["date"] for x in metadatas]
        symbols = [x["symbol"] for x in metadatas]
        titles = [x["title"] for x in metadatas]

        documents = response["documents"][0]
        return {
            "ids": ids,
            "symbols": symbols,
            "dates": dates,
            "titles": titles,
            "documents": documents
        }


if __name__ == "__main__":
    r = Retriever("test")
    print(r.retrieve("whats the situation in yemen"))
