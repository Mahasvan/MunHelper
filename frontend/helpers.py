import os

import requests
from urllib.parse import quote


base_url_context = os.environ.get("BASE_CONTEXT_URL")
if not base_url_context:
    base_url_context = "http://localhost:5000/search/ecosoc-resolutions?query="

base_url_llm = os.environ.get("BASE_LLM_URL")
if not base_url_llm:
    base_url_llm = "http://localhost:5000/chat/ecosoc-resolutions?query="


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
