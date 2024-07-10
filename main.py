import os
import requests
from pathlib import Path


def download_image(url, file_name, dir_name, extension='.jpg', params=None):
    full_file_name = file_name + extension
    Path(dir_name).mkdir(parents=True, exist_ok=True)
    file_path = os.path.join(dir_name, full_file_name)
    response = requests.get(url, params=params)
    response.raise_for_status()
    with open(file_path, 'wb') as file:
        file.write(response.content)


def download_comic(comic_number):
    comic_url = f'https://xkcd.com/{comic_number}/info.0.json'

    comic_response = requests.get(comic_url)
    comic_response.raise_for_status()

    comic_details = comic_response.json()
    comic_comments = comic_details['alt']
    comic_image_url = comic_details['img']

    image_response = requests.get(comic_image_url)
    image_response.raise_for_status()

    comic_image_name = f'comic_{comic_number}.jpg'
    download_image(comic_image_url, comic_image_name, 'images')

    return comic_image_name, comic_comments


def main():
    comic_image_name, comic_comments = download_comic(353)  # 353 is the number of the comic about Python
    print(comic_image_name, comic_comments)


if __name__ == '__main__':
    main()
