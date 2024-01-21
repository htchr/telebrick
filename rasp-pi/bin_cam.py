from picamera2 import Picamera2
from datetime import datetime
import requests
import os
import time

project = 'test'
path = '/home/tm/launch'
url = 'http://10.0.0.185:8000/'

def error(e):
    print('An error occurred:')
    print(type(e))
    print(e)

if __name__ == '__main__':
    for f in os.listdir(path):
        if f.endswith('.jpg'):
            fpath = os.path.join(path, f)
            os.remove(fpath)

    while True:
        rn = datetime.now()
        name = rn.strftime('%Y%m%d%H%M') + project + '.jpg'

        try:
            cam = Picamera2()
            config = cam.create_still_configuration()
            cam.configure(config)
            cam.start()
            metadata = cam.capture_file(name)
            cam.close()
        except Exception as e:
            error(e)

        with open(name, 'rb') as jpg:
            files = {'file': jpg}
            try:
                response = requests.post(url + 'upload', files=files)
            except requests.exceptions.ConnectionError as e:
                print('Could not connect to server')
            except Exception as e:
                error(e)

        status = requests.get(url + 'light')
        light = status.json()['light']
        if light:
            # turn light on
            print(light)
        else:
            # turn light off
            print(light)

        os.remove(name)
        time.sleep(60)

