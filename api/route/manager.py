import os

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from api.service import shell

from api.service.chromadb_updater import ChromaDBUpdater
from api.service.ecosoc_updater import EcosocUpdater

router = APIRouter()
prefix = "/manage"

chroma_collection = os.environ.get("CHROMA_COLLECTION", "ecosoc")
chroma_host = os.environ.get("CHROMA_HOST", "localhost")
chroma_port = os.environ.get("CHROMA_PORT", 8000)

current_file_path = os.path.split(os.path.abspath(__file__))
api_folder_path = os.path.split(current_file_path[0])[0]

PROCESSED_DOCUMENTS_SOURCE = os.path.join(
    api_folder_path,
    "service",
    "documents",
    "ecosoc_processed_documents.json"
)

JSON_SOURCE = os.path.join(
    api_folder_path,
    "service",
    "documents",
    "ecosoc_resolutions.json"
)


@router.get("/update-chromadb")
def update_chromadb():
    result = {
        "cwd": os.getcwd(),
        "processed_documents_source": PROCESSED_DOCUMENTS_SOURCE,
        "chroma_collection": chroma_collection,
        "chroma_host": chroma_host,
        "chroma_port": chroma_port
    }

    updater = ChromaDBUpdater(
        chroma_collection=chroma_collection,
        chroma_host=chroma_host,
        chroma_port=chroma_port
    )
    try:
        updater.update_database(PROCESSED_DOCUMENTS_SOURCE)
    except Exception as e:
        result["error"] = str(e)
        result["success"] = False
        return JSONResponse(content=result, status_code=500)

    result["success"] = True
    return JSONResponse(content=result)


@router.get("/update-ecosoc")
def update_ecosoc(delete_downloaded_pdfs: bool = False):
    SAVEPATH = os.path.join(current_file_path[0], "ecosoc_resolutions")
    result = {
        "cwd": os.getcwd(),
        "resolution_savepath": os.path.abspath(SAVEPATH)
    }

    os.makedirs(SAVEPATH, exist_ok=True)
    try:
        updater = EcosocUpdater(
            savepath=SAVEPATH,
            json_source=JSON_SOURCE,
            processed_documents_source=PROCESSED_DOCUMENTS_SOURCE
        )
    except Exception as e:
        result["error"] = str(e)
        result["success"] = False
        return JSONResponse(content=result, status_code=500)

    try:
        status = updater.update_store()
    except Exception as e:
        result["error"] = str(e)
        result["success"] = False
        return JSONResponse(content=result, status_code=500)

    if status == 1:
        result["up_to_date"] = True
        shell.print_yellow_message("Exiting.")
        return JSONResponse(content=result)

    try:
        updater.download_resolutions()
    except Exception as e:
        result["error"] = str(e)
        result["success"] = False
        return JSONResponse(content=result, status_code=500)

    result["download_resolutions"] = True

    try:
        updater.process_resolutions()
    except Exception as e:
        result["error"] = str(e)
        result["success"] = False
        return JSONResponse(content=result, status_code=500)

    result["process_resolutions"] = True

    result["delete_downloaded_pdfs"] = delete_downloaded_pdfs

    if delete_downloaded_pdfs:
        try:
            updater.delete_resolutions()
        except Exception as e:
            result["error"] = str(e)
            result["success"] = False
            return JSONResponse(content=result, status_code=500)

    return JSONResponse(content=result)


def setup(app):
    app.include_router(router, prefix=prefix)
