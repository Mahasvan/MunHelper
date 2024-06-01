import json
from bs4 import BeautifulSoup
import urllib.request

from . import utils, shell

import os
import json
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed


class EcosocUpdater:
    # todo: check if all this works
    def __init__(self, savepath: str, json_source: str = "documents/ecosoc_resolutions.json"):
        self.savepath = savepath
        self.json_source = json_source
        with open(json_source) as f:
            self.ecosoc_resolutions = json.load(f)

        self.page_url = r"https://ecosoc.un.org/en/documents/resolutions?page={}".format(page)

    def rename(self, string, replace_with: str = "-"):
        """Copy of function `rename` from utils.py"""
        illegal = [x[0] for x in r"""< (less than)
    > (greater than)
    : (colon)
    " (double quote)
    / (forward slash)
    \ (backslash)
    | (vertical bar or pipe)
    ? (question mark)
    * (asterisk)""".split("\n")]
        for char in illegal:
            string = string.replace(char, replace_with)
        return string

    def get_filename(self, reso):
        symbol = self.rename(reso["symbol"])
        title = self.rename(reso["title"])
        if len(title) > 100:
            title = title[:100] + " [shortened]"
        return f"{symbol} - {title}.pdf"

    def update_store(self):
        page = 0
        resolutions = []
        while True:
            html = urllib.request.urlopen(self.page_url.format(page))
            htmlparse = BeautifulSoup(html, 'html.parser')
            page_resos = htmlparse.find_all("tbody")
            print(f"{page}: {len(page_resos)}")

            if len(page_resos) == 0:
                # no more resolutions
                break
            page += 1

            page_resos = page_resos[0]
            entries = page_resos.find_all_next("td")
            formatted = utils.get_formatted_reso_list(entries, self.page_url)
            shell.print_green_message(f"Found {len(formatted)} resolutions")
            resolutions.extend(formatted)
            shell.print_cyan_message(f"Total: {shell.format_bold(len(resolutions))} resolutions in store")

        # update json source with new data
        shell.print_yellow_message(f"Updating {shell.format_bold(self.json_source)} with {shell.format_bold(len(resolutions))} resolutions")
        with open(self.json_source, "w") as f:
            json.dump(resolutions, f, indent=4)
        shell.print_green_message(f"Saved {shell.format_bold(len(resolutions))} to disk "
                                  f"in {shell.format_bold(self.json_source)}.")
        self.ecosoc_resolutions = resolutions
        shell.print_green_message("Store updated.")

    def _download_resolution(self, reso, savepath):
        url = reso["url"]

        filename = self.get_filename(reso)
        file_path = os.path.join(savepath, filename)

        if os.path.exists(file_path):
            shell.print_yellow_message(f"Already present. Skipping {reso['filename']}")
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
        print(f"Downloading {total} resolutions")

        with ThreadPoolExecutor() as executor:
            futures = []
            for i, reso in enumerate(self.ecosoc_resolutions):
                print(self.savepath, reso.get("filename", "DoesNotExist"))
                futures.append(executor.submit(self._download_resolution, reso, self.savepath))

            for i, future in enumerate(as_completed(futures)):
                filename = future.result()
                if filename:
                    downloaded += 1

        print(f"Downloaded {downloaded} of {total} resolutions")

