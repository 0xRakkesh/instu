from pathlib import Path
import re
from instafetch import download_insta_post
from pdf import convert_to_pdf
def main():
    print("Insta Notes Downloader")
    storage_path = Path(input("Give Me Path Location for Notes: ").strip()).expanduser()
    storage_path.mkdir(parents=True, exist_ok=True)
    insta_url = input("Instagram Post URL: ").strip()
    pattern = r'/?\?.*$'
    insta_url = re.sub(pattern, '', insta_url)

    print(f"Your Path: {storage_path}")
    print(f"URL: {insta_url}")

    target_dir = download_insta_post(insta_url, storage_path)
    folder_name = input("Enter Folder Name (No .pdf): ").strip()
    convert_to_pdf(target_dir,folder_name)

if __name__ == "__main__":
    main()
