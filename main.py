import os
import requests
from pathlib import Path
from dotenv import load_dotenv
import random
import logging

import telegram
import telegram.error as tg_error


def download_image(url, file_name, dir_name, extension='.jpg', params=None):
    full_file_name = file_name + extension
    file_path = os.path.join(dir_name, full_file_name)
    response = requests.get(url, params=params)
    response.raise_for_status()
    with open(file_path, 'wb') as file:
        file.write(response.content)


def download_comic(comic_number, dir_name):
    comic_url = f'https://xkcd.com/{comic_number}/info.0.json'

    comic_response = requests.get(comic_url)
    comic_response.raise_for_status()

    comic_details = comic_response.json()
    comic_comments = comic_details['alt']
    comic_image_url = comic_details['img']

    image_response = requests.get(comic_image_url)
    image_response.raise_for_status()

    comic_image_name = f'comic_{comic_number}.jpg'
    download_image(comic_image_url, comic_image_name, dir_name)

    return comic_image_name, comic_comments


def get_last_comic_number():
    current_comic_url = 'https://xkcd.com/info.0.json'
    xkcd_response = requests.get(current_comic_url)
    xkcd_response.raise_for_status()
    last_comic_number = xkcd_response.json()['num']
    return last_comic_number


def get_settings():
    load_dotenv()
    token = os.environ['TG_BOT_TOKEN']
    chat_id = os.environ['TG_CHANNEL_ID']
    bot = telegram.Bot(token=token)
    return bot, chat_id


def get_files_list(folder):
    path = os.getcwd()
    files = [os.path.join(path, folder, f) for f in os.listdir(folder)]
    return files


def send_file(bot, chat_id, file_name):
    with open(file_name, 'rb') as file_to_send:
        bot.send_document(chat_id=chat_id, document=file_to_send)


def main():
    bot, chat_id = get_settings()

    dir_name = 'images'
    Path(dir_name).mkdir(parents=True, exist_ok=True)

    last_comic_number = get_last_comic_number()
    random_comic_number = random.randint(1, last_comic_number)
    comic_image_name, comic_comments = download_comic(random_comic_number, dir_name)
    print(f'Downloaded comic number {random_comic_number} image {comic_image_name} with {comic_comments} comments.')

    files = get_files_list('images')
    if not files:
        logging.error('The directory with images is empty')
        return

    try:
        print('Start posting comics to the tg channel.')
        if files[0]:
            send_file(bot, chat_id, files[0])
    except tg_error.NetworkError as e:
        logging.info('There was no internet connection')
    finally:
        for f in files:
            os.remove(f)


if __name__ == '__main__':
    main()
