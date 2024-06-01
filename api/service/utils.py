from bs4.element import ResultSet, PageElement
from urllib.parse import urlparse

system_template_str = \
    """Your job is to refer the ECOSOC resolution document extracts given in the context and answer the questions.
You are a MUN Prep Helper named Sherlock.
Do not modify the symbols, titles, or dates in any manner.
Be as detailed as possible, but don't make up any information that's not from the context. 
Always mention the resolution symbol, title, and date of the resolution along with extracts, when using information from the context.
Context is given below.

{context}

Question:

"""


def get_url(table_title_entry: PageElement, reso_symbol: str, page_url: str):
    doc_url = table_title_entry.find_next("a")["href"]

    if doc_url.endswith(".pdf"):
        if doc_url.startswith("http"):
            return doc_url

        parser = urlparse(page_url)
        url = f"{parser.scheme}://{parser.netloc}{doc_url}"
        return url
    else:
        eng_url = r"https://daccess-ods.un.org/access.nsf/Get?OpenAgent&DS={}&Lang=E"
        return eng_url.format(reso_symbol)


def get_formatted_reso_list(entries: ResultSet, page_url: str):
    formatted = [
        {
            "symbol": entries[i].get_text(strip=True),
            "title": entries[i + 1].get_text(strip=True),
            "url": get_url(entries[i + 1], entries[i].get_text(strip=True), page_url),
            "agenda_item": entries[i + 2].get_text(strip=True),
            "date": entries[i + 3].get_text(strip=True)
        } for i in range(0, len(entries), 4)
    ]
    return formatted
