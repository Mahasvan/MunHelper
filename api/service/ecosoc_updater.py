import sys
import urllib.request

import os
import json
import requests
import re
import shutil
from concurrent.futures import ThreadPoolExecutor, as_completed

from . import utils, shell

from bs4 import BeautifulSoup
import pymupdf4llm
from langchain_text_splitters import RecursiveCharacterTextSplitter


class EcosocUpdater:
    # todo: check if all this works
    def __init__(
            self, savepath: str, json_source: str = "api/service/documents/ecosoc_resolutions.json",
            processed_documents_source: str = "api/service/documents/ecosoc_processed_documents.json"
    ):
        self.savepath = savepath
        self.json_source = json_source
        self.processed_documents_source = processed_documents_source

        with open(json_source) as f:
            self.ecosoc_resolutions = json.load(f)
        with open(processed_documents_source) as f:
            self.processed_documents = json.load(f)

        self.processed_symbols = [x["metadatas"][0]["symbol"] for x in self.processed_documents]
        self.page_url = r"https://ecosoc.un.org/en/documents/resolutions?page={}"

        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=50,
            separators=["\n", "\n\n", " ", "", ",", ";", ";\n"]
        )

        self.regex_images = re.compile(r"!\[.*\]\(.*\)")
        self.regex_line_breaks = re.compile(r"(\*+)?([_-]{2,})(\*+)?")
        self.regex_extra_lines_2 = re.compile(r"\n{3,}")
        self.regex_extra_lines = re.compile(r"(-{3,}\n{3,})+-{5}")

        self.illegal = r"""<>:"/\|?*"""

    def rename(self, string, replace_with: str = "-"):
        """Copy of function `rename` from utils.py"""
        for char in self.illegal:
            string = string.replace(char, replace_with)
        return string

    def get_filename(self, reso):
        symbol = self.rename(reso["symbol"])
        title = self.rename(reso["title"])
        title = self.rename(f"{symbol} - {title}")

        if len(title) > 100:
            title = title[:100] + " [shortened]"

        title = title + ".pdf"

        return title

    def update_store(self):
        shell.print_cyan_message(f"Currently {len(self.ecosoc_resolutions)} resolutions in store")
        page = 0
        resolutions = []
        while True:
            shell.print_yellow_message(f"Scraping page: {page}")
            try:
                html = urllib.request.urlopen(self.page_url.format(page))
                htmlparse = BeautifulSoup(html, 'html.parser')
                page_resos = htmlparse.find_all("tbody")
            except Exception as e:
                shell.print_red_message(f"Error occurred while scraping page {page}\n{e}")
                continue

            if len(page_resos) == 0:
                # no more resolutions
                break
            page += 1

            page_resos = page_resos[0]
            # all entries are as table entries
            entries = page_resos.find_all_next("td")
            formatted = utils.get_formatted_reso_list(entries, self.page_url)
            shell.print_green_message(f"Found {len(formatted)} resolutions")
            resolutions.extend(formatted)
            shell.print_cyan_message(f"Total: {shell.format_bold(str(len(resolutions)))} resolutions in store")

        if len(self.ecosoc_resolutions) == len(resolutions):
            shell.print_yellow_message("No new resolutions found. Exiting.")
            return 1

        # update json source with new data
        shell.print_yellow_message(f"Updating {shell.format_bold(self.json_source)} "
                                   f"with {shell.format_bold(str(len(resolutions)))} resolutions")

        with open(self.json_source, "w") as f:
            json.dump(resolutions, f, indent=4)

        shell.print_green_message(f"Saved {shell.format_bold(str(len(resolutions)))} to disk "
                                  f"in {shell.format_bold(self.json_source)}.")

        self.ecosoc_resolutions = resolutions
        shell.print_green_message("Store updated.")

    def _download_resolution(self, reso, savepath):
        url = reso["url"]

        filename = self.get_filename(reso)
        file_path = os.path.join(savepath, filename)

        if os.path.exists(file_path):
            shell.print_yellow_message(f"Already present. Skipping {filename}")
            return filename

        try:
            file_content = requests.get(url).content
            with open(file_path, "wb") as f:
                f.write(file_content)
            shell.print_green_message(f"Saved {file_path}")
            return filename
        except Exception as e:
            shell.print_red_message(f"Error occurred while saving {file_path}\n{e}")
            return None

    def download_resolutions(self):
        downloaded = 0
        total = len(self.ecosoc_resolutions)
        shell.print_cyan_message(f"Downloading {total} resolutions")

        with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
            futures = []
            for i, reso in enumerate(self.ecosoc_resolutions):
                futures.append(executor.submit(self._download_resolution, reso, self.savepath))

            downloaded = len([x for x in as_completed(futures) if x.result() is not None])

        print(f"Downloaded {downloaded} of {total} resolutions")

    def preprocess_text(self, md_text: str):
        for image in self.regex_images.findall(md_text):
            md_text = md_text.replace(image, "")
        for line_break in self.regex_line_breaks.findall(md_text):
            md_text = md_text.replace("".join(line_break), "")
        for extra_line in self.regex_extra_lines.findall(md_text):
            md_text = md_text.replace(extra_line, "")
        for extra_line in self.regex_extra_lines_2.findall(md_text):
            md_text = md_text.replace(extra_line, "")
        return md_text

    def _create_document(self, reso):
        try:
            # convert pdf to markdown
            filename = self.get_filename(reso)
            md_text = pymupdf4llm.to_markdown(str(os.path.join(self.savepath, filename)))
            md_text = self.preprocess_text(md_text)
        except Exception as e:
            shell.print_red_message(f"Error on resolution {reso["symbol"]}")
            print(e)
            return None

        documents = [x.page_content for x in self.splitter.create_documents([md_text])]
        metadata = {
            "title": reso["title"],
            "symbol": reso["symbol"],
            "date": reso["date"]
        }
        ids = [f"{reso['symbol']}_part_{i}" for i in range(len(documents))]

        # remove documents that have no content
        to_remove = []
        for i in range(len(ids)):
            # remove documents which dont have alphabets (theyre useless)
            if not re.findall("[a-zA-z]+", documents[i]):
                shell.print_yellow_message(f"Count not find alphanumeric characters in document {i}")
                print(documents[i])
                to_remove.append(i)
        if to_remove:
            shell.print_yellow_message(f"Removing indices: {to_remove}")

        for index in to_remove[::-1]:
            ids.pop(index)
            documents.pop(index)

        if not ids:
            # we may have removed every document
            return {}

        return {
            "metadatas": [metadata for _ in range(len(documents))],
            "ids": ids,
            "documents": documents
        }

    def process_resolutions(self):
        for reso in self.ecosoc_resolutions:
            # if the symbol does not exist in the processed documents, then make the document
            symbol = reso["symbol"]

            if symbol in self.processed_symbols:
                continue

            doc = self._create_document(reso)
            if doc:
                self.processed_documents.append(doc)
                self.processed_symbols.append(symbol)
                shell.print_green_message(f"Processed {reso['symbol']}")

        shell.print_yellow_message(
            f"Saving {len(self.processed_documents)} processed documents "
            f"to {self.processed_documents_source}")

        with open(self.processed_documents_source, "w") as f:
            json.dump(self.processed_documents, f, indent=4)

        shell.print_green_message("Saved processed documents to disk.")

    def delete_resolutions(self):
        shell.print_yellow_message("Removing downloaded resolutions...")
        shell.print_yellow_message(f"Path: {shell.format_bold(self.savepath)}")
        folder = self.savepath

        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    # if the file_path leads to a file, delete it.
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    # if it is a directory, delete the directory.
                    shutil.rmtree(file_path)
            except Exception as e:
                shell.print_red_message(f"Failed to delete {file_path}.")
                print(e)
        shell.print_cyan_message("Deleted all downloaded resolutions.")


if __name__ == "__main__":
    # get the path of this file
    current_file_path = os.path.split(os.path.abspath(__file__))
    SAVEPATH = os.path.join(current_file_path[0], "ecosoc_resolutions")
    JSON_SOURCE = os.path.join(current_file_path[0], "documents", "ecosoc_resolutions.json")
    PROCESSED_DOCUMENTS_SOURCE = os.path.join(current_file_path[0], "documents", "ecosoc_processed_documents.json")

    shell.print_cyan_message(f"Current Working Directory: {os.getcwd()}")
    shell.print_cyan_message(f"Resolution Save Path: {os.path.abspath(SAVEPATH)}")

    shell.print_yellow_message("Ensuring save path exists...")
    os.makedirs(SAVEPATH, exist_ok=True)
    shell.print_green_message("Done.")

    updater = EcosocUpdater(
        savepath=SAVEPATH,
        json_source=JSON_SOURCE,
        processed_documents_source=PROCESSED_DOCUMENTS_SOURCE
    )

    shell.print_yellow_message("Updating Store...")
    status = updater.update_store()
    if status == 1:
        shell.print_yellow_message("Exiting.")
        exit(0)

    shell.print_yellow_message("Downloading resolutions...")
    updater.download_resolutions()

    shell.print_yellow_message("Processing resolutions...")
    updater.process_resolutions()
    shell.print_green_message("Done.")

    shell.print_blue_message(
        shell.format_bold("Would you like to delete the downloaded resolution PDFs? (y/n): "),
        end="")
    delete = input().strip().lower()
    if delete == "y":
        # todo: remove directory
        updater.delete_resolutions()
    else:
        shell.print_yellow_message("Skipping deletion.")

    python = "python" if os.name == "nt" else "python3"
    shell.print_pink_message("Now run: " + shell.format_bold(f"{python} chromadb_updater.py"))
