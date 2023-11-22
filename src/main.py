import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from tqdm import tqdm
from unsync import unsync
from PyPDF2 import PdfMerger
import pdfkit
import glob


failed_urls =[]
good_urls = []

def create_directory(directory_name):
    if not os.path.exists(directory_name):
        os.makedirs(directory_name)

def get_links_from_url(base_url, hrefs_to_skip):
    domain = urlparse(base_url).netloc
    response = requests.get(base_url)
    soup = BeautifulSoup(response.text, "html.parser")
    links = soup.find_all("a")

    valid_links = []
    for link in tqdm(links, leave=False, ascii=True, unit="pages"):
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
                valid_links.append(full_url)
    return valid_links

@unsync
def download_pdf(library):
    r = requests.get(library["base_url"], stream=True)
    if r.status_code == 200:
        total_size_in_bytes = int(r.headers.get('content-length', 0))
        block_size = 1024  # 1 Kibibyte
        progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True,
                            leave=False, ascii=True, desc=library["name"])
        with open(f'documents/{library["name"]}/{str(library["name"]).lower()}.pdf', 'wb') as f:
            for data in r.iter_content(block_size):
                progress_bar.update(len(data))
                f.write(data)
        progress_bar.close()
        if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
            print("ERROR, something went wrong")
    return "done"


def merge_pdfs(library_name):
    pdfs = glob.glob(f"documents/{library_name}/*.pdf")
    merger = PdfMerger()

    for pdf in tqdm(pdfs, ascii=False, leave=True):
        merger.append(pdf)

    merger.write(f"final/{library_name}.pdf")
    merger.close()
    print(f"PDFs for {library_name} merged successfully!")



@unsync
def process_library(library):
    if library["pdf"]:
        create_directory(f"documents/{library['name']}")
        download_pdf(library)
        return library["name"]
    else:
        links = get_links_from_url(library["base_url"], library["hrefs_to_skip"])
        create_directory("documents")
        for link in tqdm(links,leave=False, ascii=True, unit="pages",desc=library["name"]):
            try:
                create_directory(f"documents/{library['name']}")
                pdfkit.from_url(
                    link,
                    f'documents/{library["name"]}/{library["name"]}_{urlparse(link).path.replace("/", "_")}.pdf',
                )
                good_urls.append(link)
            except Exception as e:
                print(f"Failed to create PDF for {link}. Reason: {str(e)}")
                failed_urls.append(link)
        return library["name"]



def main():
    library_list = [
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
        {
            "name": "Pytest",
            "base_url": "https://docs.pytest.org/_/downloads/en/7.4.x/pdf/",
            "hrefs_to_skip": [],
            "pdf": True,
        },
        {
            "name": "Passlib",
            "base_url": "https://passlib.readthedocs.io/_/downloads/en/stable/pdf/",
            "hrefs_to_skip": [],
            "pdf": True,
        },
        # Add more libraries as needed
    ]

    create_directory("final")
    import time
    t0 = time.time()

    tasks = [process_library(library) for library in tqdm(library_list, ascii=False, leave=True, desc="Libraries Processing")]
    
    t0_merge = time.time()
    for task in tqdm(tasks, ascii=False, leave=True, desc="Libraries Processed"):
        library_name = task.result()
        merge_pdfs(library_name)

    t1 = time.time() - t0
    minutes, seconds = divmod(t1, 60)
    print(f"Time taken to download PDFs: {int(minutes)} minutes and {int(seconds)} seconds")

    # merge_pdfs()

    t2 = time.time() - t0_merge
    minutes, seconds = divmod(t2, 60)
    print(f"Time taken to merge the documents: {int(minutes)} minutes and {int(seconds)} seconds")
    
    t3 = time.time() - t0
    minutes, seconds = divmod(t3, 60)
    print(f"Total time taken: {int(minutes)} minutes and {int(seconds)} seconds")

if __name__ == "__main__":
    main()

    for f in failed_urls:
        print(f)
