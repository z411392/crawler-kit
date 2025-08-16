from firebase_admin import initialize_app, get_app
from firebase_admin.credentials import Certificate
from os import getenv
from re import sub
from tqdm import tqdm
from dotenv import load_dotenv
from os.path import exists
from os import environ
from typing import Collection
import pandas as pd
from firebase_admin.firestore import client

if exists("src/.env"):
    load_dotenv("src/.env", override=True)

try:
    get_app()
except Exception:
    credential = Certificate(
        dict(
            type="service_account",
            project_id=getenv("PROJECT_ID"),
            private_key=sub(r"\\n", "\n", getenv("PRIVATE_KEY")),
            client_email=getenv("CLIENT_EMAIL"),
            token_uri="https://oauth2.googleapis.com/token",
        )
    )
    initialize_app(
        credential=credential,
        options=dict(),
    )
db = client()
collection = db.collection("sources/Ebay/types/product/platforms/web/raw")
docs = collection.get()
data = []
for doc in docs:
    data.append(doc.to_dict())

pd.DataFrame(data).to_csv("ebay_result.csv", index=False)
