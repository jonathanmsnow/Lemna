from dotenv import load_dotenv
from huggingface_hub import HfApi
import os

load_dotenv()

hf_token = os.getenv("HF_TOKEN")

api = HfApi(token=hf_token)
api.upload_folder(
    folder_path="./datasets",
    repo_id="jmsnow/duckweed-wells",
    repo_type="dataset",
)