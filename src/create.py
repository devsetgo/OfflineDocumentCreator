# -*- coding: utf-8 -*-
# import requests
# import os
# import markdown
# from weasyprint import HTML

# from PyPDF2 import PdfReader, PdfMerger
# from tqdm import tqdm

# URL_LIST:list =[{"name":"fastapi","url":'https://api.github.com/repos/tiangolo/fastapi/git/trees/master?recursive=1'}]

# # GitHub API URL for the repository
# url = 'https://api.github.com/repos/tiangolo/fastapi/git/trees/master?recursive=1'

# # Set a user agent
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

# response = requests.get(url, headers=headers)

# if response.status_code == 200:
#     files = response.json()['tree']

#     # PDF merger
#     merger = PdfMerger()

#     for file in tqdm(files,ascii=True,desc="Downloading files"):
#         if file['path'].startswith('docs/en/docs/') and file['path'].endswith('.md'):
#             file_url = 'https://raw.githubusercontent.com/tiangolo/fastapi/master/' + file['path']
#             file_response = requests.get(file_url, headers=headers)
#             if file_response.status_code == 200:
#                 md = file_response.text
#                 html = markdown.markdown(md)
#                 HTML(string=html).write_pdf('temp.pdf')

#                 # Check if the PDF is valid before appending it
#                 try:
#                     PdfReader('temp.pdf')
#                     merger.append('temp.pdf')
#                 except Exception as ex:
#                     print(f"Failed to process file: {file['path']} full URL: {file_url} error: {ex}")

#     merger.write("output.pdf")
#     merger.close()
# else:
#     print(f"Failed to retrieve the webpage: Status Code {response.status_code}")
