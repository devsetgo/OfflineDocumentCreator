import httpx
from bs4 import BeautifulSoup
import pdfkit
import os
from urllib.parse import urlparse, urljoin
from tqdm import tqdm  # For progress bar
import asyncio

failed_urls = []
good_urls = []


async def get_all_links(data_dict: dict):
    # Create a directory to store the PDFs
    if not os.path.exists("documents"):
        os.makedirs("documents")

    base_url = data_dict["base_url"]
    hrefs_to_skip = data_dict["hrefs_to_skip"]
    domain = urlparse(base_url).netloc

    async with httpx.AsyncClient() as client:
        response = await client.get(base_url)
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
            ):
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
        merger.append(pdf)

    merger.write("documents/merged.pdf")
    merger.close()


async def main():
    library_list: list = [
        {
            "name": "fastapi",
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
        },
        {
            "name": "sqlalchemy",
            "base_url": "https://docs.sqlalchemy.org/en/20/",
            "hrefs_to_skip": [".zip"],
        },
        {
            "base_url": "https://loguru.readthedocs.io/en/stable/",
            "hrefs_to_skip": ["/downloads/", "/0."],
        },
        {
            "name": "httpx",
            "base_url": "https://www.python-httpx.org/",
            "hrefs_to_skip": [],
        },
        {"name": "tqdm", "base_url": "https://tqdm.github.io/", "hrefs_to_skip": []},
        {
            "name": "pydantic",
            "base_url": "https://docs.pydantic.dev/latest/",
            "hrefs_to_skip": ["/dev/", "/1."],
        },
        # {'name':'x',"base_url": "https://xyz.com", "hrefs_to_skip": []},
        # {'name':'x',"base_url": "https://xyz.com", "hrefs_to_skip": []},
        # {'name':'x',"base_url": "https://xyz.com", "hrefs_to_skip": []},
    ]
    for library in tqdm(library_list, ascii=True, leave=True):
        # print(library)
        await get_all_links(data_dict=library)


if __name__ == "__main__":
    # asyncio.run(get_all_links())
    asyncio.run(main())

    # merge_pdfs()

    for f in failed_urls:
        print(f)
