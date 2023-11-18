import requests
from bs4 import BeautifulSoup
import pdfkit
import os
from urllib.parse import urlparse, urljoin
from tqdm import tqdm  # For progress bar
import shutil

failed_urls = []
good_urls = []


def get_all_links(data_dict: dict):
    # Create a directory to store the PDFs
    if not os.path.exists("documents"):
        os.makedirs("documents")

    base_url = data_dict["base_url"]
    hrefs_to_skip = data_dict["hrefs_to_skip"]
    domain = urlparse(base_url).netloc

    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, "html.parser")
    links = soup.find_all("a")

    for link in tqdm(links, leave=False, ascii=True, desc=data_dict["name"]):
        url = link.get("href")
        if url:
            full_url = urljoin(base_url, url)
            url_domain = urlparse(full_url).netloc
            if (
                url_domain == domain
                and not any(href in full_url for href in hrefs_to_skip)
                and "#" not in full_url
                and not full_url.endswith(".com/")
                and not full_url.endswith(".zip")
            ):
                # print(full_url)
                try:
                    pdfkit.from_url(
                        full_url,
                        f'documents/{domain}_{urlparse(full_url).path.replace("/", "_")}.pdf',
                    )
                    good_urls.append(full_url)
                except Exception as e:
                    print(f"Failed to create PDF for {full_url}. Reason: {str(e)}")
                    failed_urls.append(full_url)


def merge_pdfs():
    from PyPDF2 import PdfMerger
    import glob

    pdfs = glob.glob("documents/*.pdf")
    merger = PdfMerger()

    for pdf in tqdm(pdfs, ascii=True, leave=True):
        # print(pdf)
        merger.append(pdf)

    merger.write("final/libraries.pdf")
    merger.close()
    print("PDFs merged successfully!")


def main():
    library_list: list = [
        {
            "name": "FastAPI",
            "base_url": "https://fastapi.tiangolo.com",
            "hrefs_to_skip": [
                "/sponsors/",
                "/de/",
                "/em/",
                "/es/",
                "/fa/",
                "/fr/",
                "/he/",
                "/id/",
                "/ja/",
                "/ko/",
                "/pl/",
                "/pt/",
                "/ru/",
                "/tr/",
                "/uk/",
                "/ur/",
                "/vi/",
                "/yo/",
                "/zh/",
                "/zh/",
            ],
            "pdf": False,
        },
        {
            "name": "SQLAlchemy",
            "base_url": "https://docs.sqlalchemy.org/en/20/",
            "hrefs_to_skip": [".zip"],
            "pdf": False,
        },
        {
            "name": "Loguru",
            "base_url": "https://loguru.readthedocs.io/en/stable/",
            "hrefs_to_skip": ["/downloads/", "/0."],
            "pdf": False,
        },
        {
            "name": "HTTPX",
            "base_url": "https://www.python-httpx.org/",
            "hrefs_to_skip": [],
            "pdf": False,
        },
        {
            "name": "TQDM",
            "base_url": "https://tqdm.github.io/",
            "hrefs_to_skip": ["/slides", "/presentation", "/merch", "..", "video"],
            "pdf": False,
        },
        {
            "name": "Pydantic",
            "base_url": "https://docs.pydantic.dev/latest/",
            "hrefs_to_skip": ["/dev/", "/1."],
            "pdf": False,
        },
        # {
        #     "name": "alembic",
        #     "base_url": "https://alembic.sqlalchemy.org/en/latest/",
        #     "hrefs_to_skip": [],
        #     "pdf": False,
        # },
        {
            "name": "Textblob",
            "base_url": "https://textblob.readthedocs.io/_/downloads/en/latest/pdf/",
            "hrefs_to_skip": [],
            "pdf": True,
        },
        # {
        #     "name": "MkDocs-Material",
        #     "base_url": "https://squidfunk.github.io/mkdocs-material/",
        #     "hrefs_to_skip": [],
        #     "pdf": False,
        # },
        {
            "name": "Pytest",
            "base_url": "https://docs.pytest.org/_/downloads/en/7.4.x/pdf/",
            "hrefs_to_skip": [],
            "pdf": True,
        },
        # {
        #     "name": "Passlib",
        #     "base_url": "https://passlib.readthedocs.io/_/downloads/en/stable/pdf/",
        #     "hrefs_to_skip": [],
        #     "pdf": True,
        # },
        # {
        #     "name": "Xyz",
        #     "base_url": "https://xyz.com",
        #     "hrefs_to_skip": [],
        #     "pdf": False,
        # },
    ]
    for library in tqdm(library_list, ascii=True, leave=True):
        if library["pdf"] is True:
            r = requests.get(library["base_url"], stream=True)
            if r.status_code == 200:
                with open(
                    f'documents/{str(library["name"]).lower()}.pdf',
                    "wb",
                ) as f:
                    r.raw.decode_content = True
                    shutil.copyfileobj(r.raw, f)
        else:
            get_all_links(data_dict=library)
            # pass

    merge_pdfs()


if __name__ == "__main__":
    main()

    for f in failed_urls:
        print(f)
