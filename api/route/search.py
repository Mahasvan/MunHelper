import json
import os

from fastapi import APIRouter
import chromadb

from api.service import shell

router = APIRouter()
prefix = "/search"

chroma_host = os.environ.get("CHROMA_HOST", "localhost")
chroma_port = os.environ.get("CHROMA_PORT", 8000)

client = chromadb.HttpClient(host=chroma_host, port=chroma_port)

ecosoc = client.get_collection("ecosoc")

all_resolutions = []


def populate_resolutions():
    shell.print_yellow_message("Populating ECOSOC resolutions...")
    global all_resolutions
    try:
        with open("api/service/documents/ecosoc_resolutions.json", "r") as f:
            all_resolutions = json.load(f)
        shell.print_green_message("Populated ECOSOC resolutions successfully.")
    except Exception as e:
        shell.print_red_message(f"Failed: {str(e)}")


@router.get("/ecosoc-resolutions")
def ecosoc_resolutions(query: str, n_results: int = 5):
    results = ecosoc.query(query_texts=[query], n_results=n_results)
    ids = results["ids"][0]
    metadatas = results["metadatas"][0]
    dates = [x["date"] for x in metadatas]
    symbols = [x["symbol"] for x in metadatas]
    titles = [x["title"] for x in metadatas]
    documents = results["documents"][0]
    distances = results["distances"][0]

    results = []
    for i in range(len(ids)):
        # print(f"{i + 1}.")
        #
        # print("Symbol:", symbols[i])
        # print("Title:", titles[i])
        # print("Date:", dates[i])
        # print("Distance:", distances[i])
        # print("====")
        # print("Document:", documents[i])
        # print("\n----\n")
        results.append({
            "symbol": symbols[i],
            "title": titles[i],
            "date": dates[i],
            "distance": distances[i],
            "document": documents[i]
        })
    return results


@router.get("/all-resolutions")
def get_all_resolutions():
    return all_resolutions

def setup(app):
    populate_resolutions()
    app.include_router(router, prefix=prefix)
