import json
import os

import chromadb

from . import shell

settings = chromadb.config.Settings(anonymized_telemetry=False)

bare_metal = False
"""
Change this to True if not running on Docker. 
"""
if bare_metal:
    # loads environment variables from `.env` file
    from dotenv import load_dotenv
    load_dotenv()

class ChromaDBUpdater:
    def __init__(self, chroma_collection: str, chroma_host: str = "localhost", chroma_port: int = 8000):
        self.chroma_server_ip = chroma_host
        self.chroma_port = chroma_port
        try:
            self.client = chromadb.HttpClient(host=chroma_host, port=chroma_port, settings=settings)
        except Exception as e:
            shell.print_red_message(f"Error occurred while connecting to ChromaDB\n{e}")
            return
        shell.print_green_message(f"ChromaDB client connected to {chroma_host}")
        try:
            self.chroma_collection = self.client.get_or_create_collection(chroma_collection)
        except Exception as e:
            shell.print_red_message(f"Error occurred while loading ChromaDB collection\n{e}")
            return

        shell.print_green_message(f"ChromaDB collection loaded: {chroma_collection}")

    def update_database(self, processed_documents_path: str):
        with open(processed_documents_path) as f:
            processed_documents = json.load(f)
        total = len(processed_documents)
        shell.print_cyan_message(f"Updating ChromaDB with {total} documents")
        for i, reso in enumerate(processed_documents):
            shell.print_yellow_message(f"Adding document {i + 1}/{total}")
            try:
                self.chroma_collection.add(
                    documents=reso["documents"],
                    ids=reso["ids"],
                    metadatas=reso["metadatas"])
                shell.print_green_message("Added document successfully.")
            except Exception as e:
                shell.print_red_message(f"Error occurred while adding document to ChromaDB\n{e}")
                continue
        shell.print_green_message("ChromaDB updated.")


# DRIVER CODE
if __name__ == "__main__":
    chroma_collection = os.environ.get("CHROMA_COLLECTION", "ecosoc")
    chroma_host = os.environ.get("CHROMA_HOST", "localhost")
    chroma_port = os.environ.get("CHROMA_PORT", 8000)

    # get the path of this file
    current_file_path = os.path.split(os.path.abspath(__file__))

    PROCESSED_DOCUMENTS_SOURCE = os.path.join(
        current_file_path[0],
        "documents",
        "ecosoc_processed_documents.json"
    )
    shell.print_cyan_message(f"Current Working Directory: {os.getcwd()}")
    shell.print_cyan_message(f"Processed Documents Source: {PROCESSED_DOCUMENTS_SOURCE}")

    updater = ChromaDBUpdater(
        chroma_collection=chroma_collection,
        chroma_host=chroma_host,
        chroma_port=chroma_port
    )

    shell.print_yellow_message("Updating ChromaDB...")
    updater.update_database(PROCESSED_DOCUMENTS_SOURCE)
    shell.print_green_message("Done. Your database is now up to date!")
