import os
import fitz
from google.cloud import storage
import re

def download(arxiv_id) -> str:
    file_name = f"dataset/tmp/{arxiv_id}.pdf"
    os.makedirs(os.path.dirname(file_name), exist_ok=True)

    bucket = "arxiv-dataset"
    blob = ''
    if re.match(r'[\w\-\.]+/[\w\.]+', arxiv_id):
        dir_name = os.path.dirname(arxiv_id)
        pdf_name = file_name.split('/')[-1]
        year_month = pdf_name[:4]
        blob = f"arxiv/{dir_name}/pdf/{year_month}/{pdf_name}"
    else:
        pdf_name = file_name.split('/')[-1]
        year_month = arxiv_id[:4]
        blob = f"arxiv/arxiv/pdf/{year_month}/{pdf_name}"

    storage_client = storage.Client.create_anonymous_client()
    bucket = storage_client.bucket(bucket)
    blob = bucket.blob(blob)
    blob.download_to_filename(file_name)
    # print(f"Downloaded {arxiv_id}.pdf from gs://{bucket}:{blob} successfully.")
    return file_name


def context(file_name) -> dict:
    context = {
        'toc': '',
        'fulltext': [],
    }

    toc_list = []
    with fitz.open(file_name) as doc: # type: ignore
        toc = doc.get_toc(simple=False)
        if len(toc) == 0:
            toc_list.append('No provided table of contents.')
        else:
            for entry in toc:
                toc_list.append(entry[1])

        for page in doc:
            text = page.get_text().encode("utf-8")
            text = text.replace(b'\n', b' ')
            context['fulltext'].append(text.decode("utf-8"))

    context['toc'] = "[Table Of Contents]: \n" + "\n".join(toc_list) + ";"

    return context


def remove(file_name):
    if os.path.exists(file_name):
        os.remove(file_name)

        # print(f"Removed {file_name} successfully.")
