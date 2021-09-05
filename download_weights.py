import os
import zipfile
import tempfile
import requests

from tqdm.auto import tqdm
import nltk
nltk.downloader.download('maxent_ne_chunker')
nltk.downloader.download('words')
nltk.downloader.download('treebank')
nltk.downloader.download('maxent_treebank_pos_tagger')
nltk.downloader.download('punkt')
nltk.download('averaged_perceptron_tagger')

import text_model

# Pre-trained weights for /pol GPT-2 Model
WEIGHTS_URL = 'http://www.dropbox.com/s/s7k50558gg2ircl/weights_and_vocab.zip?dl=1'
WEIGHTS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), 'weights'))


def download(url, dest_path, file_name=None):
    resp = requests.get(url, stream=True)

    os.makedirs(dest_path, exist_ok=True)
    if not file_name:
        file_name = os.path.basename(url)
    output = os.path.abspath(os.path.join(dest_path, file_name))

    total = int(resp.headers.get('content-length', 0))
    with open(output, 'wb') as file, tqdm(
            desc=file_name,
            total=total,
            unit='iB',
            unit_scale=True,
            unit_divisor=1024,
    ) as bar:
        for data in resp.iter_content(chunk_size=1024):
            size = file.write(data)
            bar.update(size)


def extract_zipfile(src_file: str, dest_path: str):
    with zipfile.ZipFile(src_file,"r") as zip_ref:
        zip_ref.extractall(dest_path)


def download_and_extract_zipfile(url, dest_path):
    archive_name = 'weights_and_vocab.zip'
    with tempfile.TemporaryDirectory() as temp_dir:
        download(url, dest_path=temp_dir, file_name=archive_name)
        extract_zipfile(os.path.join(temp_dir, archive_name), dest_path)


def main():
    download_and_extract_zipfile(WEIGHTS_URL, 'weights')
    # This makes sure all of the weights are downloaded 
    # for the default model, speeding up initialization
    text_model.generate_text(prompt_text="test")

if __name__ == "__main__":
    main()
