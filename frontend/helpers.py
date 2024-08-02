import os
import threading

import requests
from urllib.parse import quote

base_url = os.environ.get("BASE_API_URL", "http://localhost:5000")
# remove trailing forward slash if present
base_url = base_url.rstrip("/")

base_url_context = f"{base_url}/search/ecosoc-resolutions?query="
base_url_llm = f"{base_url}/chat/ecosoc-resolutions?query="
base_url_update = f"{base_url}/manage/update-chromadb"


def get_context(query):
    url = base_url_context + quote(query)
    res = requests.get(url)
    return res.json()


def parse_results(res):
    final = ""
    for reso in res:
        sym = reso["symbol"]
        title = reso["title"]
        date = reso["date"]
        document = reso["document"]
        string = """#### {title}\n##### _{sym} - {date}_\n```\n{document}\n```\n\n""".format(sym=sym, title=title,
                                                                                             date=date,
                                                                                             document=document)
        final += string
        final += "\n\n<hr>\n\n"
    return final


def get_llm_response(query):
    url = base_url_llm + quote(query)
    s = requests.Session()
    with s.get(url, headers=None, stream=True) as resp:
        for line in resp.iter_lines():
            yield line.decode('utf-8')


def update_chromadb():
    res = requests.get(base_url_update)
    return res.status_code


def update_and_forget():
    thread = threading.Thread(target=update_chromadb)
    thread.start()
