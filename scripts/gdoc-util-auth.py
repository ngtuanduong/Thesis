"""
gdoc-util-auth: shared auth + service builder for all gdoc-* scripts.

Usage (as a library):
    from gdoc_util_auth import get_docs_service, DOC_ID
    service = get_docs_service()
"""
import warnings
warnings.filterwarnings("ignore")

import os
from google.oauth2 import service_account
from googleapiclient.discovery import build

KEY_FILE = os.environ.get(
    "GDOC_KEY_FILE",
    "C:/Users/duong/WebstormProjects/Thesis/infra-inkwell-465003-f2-369235afe5ac.json",
)
DOC_ID = os.environ.get(
    "GDOC_DOC_ID",
    "1O4wJNovNTFjD5DORC-WOJ2AftbcjfyoQ6HuzRSlYFfA",
)
SCOPES = [
    "https://www.googleapis.com/auth/documents",
    "https://www.googleapis.com/auth/drive",
]


def get_docs_service():
    creds = service_account.Credentials.from_service_account_file(KEY_FILE, scopes=SCOPES)
    return build("docs", "v1", credentials=creds)


def get_drive_service():
    creds = service_account.Credentials.from_service_account_file(KEY_FILE, scopes=SCOPES)
    return build("drive", "v3", credentials=creds)


def get_document(service=None, doc_id=None):
    service = service or get_docs_service()
    return service.documents().get(documentId=doc_id or DOC_ID).execute()


def iter_paragraphs(doc):
    """Yield (startIndex, endIndex, text, namedStyleType) for each paragraph."""
    for elem in doc["body"]["content"]:
        if "paragraph" not in elem:
            continue
        para = elem["paragraph"]
        text = ""
        for el in para.get("elements", []):
            if "textRun" in el:
                text += el["textRun"]["content"]
        style = para.get("paragraphStyle", {}).get("namedStyleType", "NORMAL_TEXT")
        yield elem["startIndex"], elem["endIndex"], text, style
