FILENAME_EXTENSION = 'jpg'
IMAGE_FORMAT = 'jpeg'

from datetime import datetime
import os
import re
import time

from PIL import ImageGrab

def crunch(image, factor):
    new_size = list(map(lambda x: x/factor, image.size))
    image.thumbnail(new_size)
    return image

def capture_image():
    image = ImageGrab.grab()
    crunch(image, 9)
    return image

def image_filename():
    '''Make a date-based filename for a captured image.

    The filename should be iso standard but Windows-friendly, which means strip
    the punctuation.
    '''

    omit_pattern = r'[^0-9T]'
    iso_string = datetime.now().isoformat(timespec='seconds')
    scrubbed = re.sub(omit_pattern, '', iso_string)
    filename = f'{scrubbed}.{FILENAME_EXTENSION}'
    return filename

def current_directory():
    return os.path.dirname(os.path.realpath(__file__))

def image_directory_path():
    return os.path.sep.join([
        current_directory(),
        'images',
    ])

def file_path():
    return os.path.sep.join([
        image_directory_path(),
        image_filename(),
    ])

def store_screenshot():
    '''Store a thumnail screenshot to curdir'''

    image = capture_image()
    os.makedirs(image_directory_path(), exist_ok=True)
    image.save(file_path(), IMAGE_FORMAT)

def log(message):
    timestamp = datetime.now().isoformat()
    print(f'{timestamp}: {message}')

# input: context of Hovis working
# output: directory of screenshot thumbnails
def main():
    '''Periodically store a thumbnail screenshot of the desktop'''

    import time
    while True:
        log(f'Storing screenshot {image_filename()}')
        store_screenshot()
        time.sleep(5*60)
