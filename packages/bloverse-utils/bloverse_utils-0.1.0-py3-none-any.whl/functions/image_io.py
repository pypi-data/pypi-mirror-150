"""
This is a general function for image related functionality, including download and upload, leveraging cloudinary etc etc
"""
import warnings
warnings.filterwarnings("ignore")

## Add the root path so modules can be easily imported
import os
import sys
temp = os.path.dirname(os.path.abspath(__file__))
vals = temp.split('/')
BASE_DIR = '/'.join(vals[:-2])
BASE_DIR = '%s/' % BASE_DIR
sys.path.insert(0, BASE_DIR)

import cv2
import numpy as np
from functools import wraps
import errno
import os
import signal
import cloudinary
import cloudinary.uploader
import cloudinary.api

from Config.settings import cloudinary_cloud_name, cloudinary_api_key, cloudinary_api_secret

"""
Image upload
"""
"""
Add timeout functionaltiy
"""

class TimeoutError(Exception):
    pass

def timeout(seconds=10, error_message=os.strerror(errno.ETIME)):
    def decorator(func):
        def _handle_timeout(signum, frame):
            raise TimeoutError(error_message)

        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, _handle_timeout)
            signal.alarm(seconds)
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)
            return result

        return wraps(func)(wrapper)

    return decorator


@timeout(10, os.strerror(errno.ETIMEDOUT))
def url_to_image(url, temp_image_path):
    import requests

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:71.0) Gecko/20100101 Firefox/71.0'}
    
    r = requests.get(url, headers=headers)

    with open(temp_image_path, 'wb') as f:
        f.write(r.content)

    image = cv2.imread(temp_image_path)
    image = cv2.cvtColor(np.uint8(image), cv2.COLOR_BGR2RGB)
    
    return image


"""
Cloudinary
"""
cloudinary.config( 
  cloud_name = cloudinary_cloud_name, 
  api_key = cloudinary_api_key, 
  api_secret = cloudinary_api_secret,
  secure = True
)


def upload_image_to_cloudinary(image_path):
    output_dict = cloudinary.uploader.upload(image_path)
    cloudinary_url = output_dict['url']
    
    return cloudinary_url