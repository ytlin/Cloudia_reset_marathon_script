import os
import subprocess
from cv2 import cv2
import glob
import numpy as np
from ppadb.client import Client as AdbClient

class adb():
    def __init__(self, path):
        self.path = path ##
        self.adb_exe = '{}\\platform-tools\\adb.exe'.format(self.path)
    
    def connect_to_BS(self, ip, port):
        '''
        待測試 => 重開機直接執行
        順便記一下: python 如果不需要return的func要怎麼寫比較好
        '''
        self.client = AdbClient(host="127.0.0.1", port=5037)
        try:
            self.client.remote_connect(ip, port)
        except:
            subprocess.Popen('{} start-server'.format(self.adb_exe), stdout=subprocess.PIPE).stdout.read()
        print('Connect success!')

        return 1

    def list_devices(self):
        devices = self.client.devices()
        print('List of devices attached:')
        for device in devices:
            print('    {}'.format(device.serial))
        return 1
    
    def get_device(self, serial):
        return self.client.device(serial)

    def screencap(self, device):
        image_bytes = device.screencap()
        img = cv2.imdecode(np.frombuffer(image_bytes, dtype='uint8'), cv2.IMREAD_COLOR)
        return img

    def tap(self, device, x, y):
        device.shell('input tap {} {}'.format(x, y))
        return 1


def cv_imread(path):
    img = cv2.imdecode(np.fromfile(path, dtype=np.uint8), cv2.IMREAD_COLOR)
    return img

class helper():

    def __init__(self, path):
        self.path = path
        self.adb = None
        self.device = None
        self.templates = {}
        self.required_list = glob.glob('{}\\images\\required\\*.png'.format(self.path))
        self.optional_list = glob.glob('{}\\images\\optional\\*.png'.format(self.path))

    def setup_adb_client(self):
        self.adb = adb(self.path)
        self.adb.connect_to_BS('127.0.0.1', 5555)
        self.adb.list_devices()
        serial = input('Please select the device by its serial number: ')
        self.device = self.adb.get_device(serial)

    def load_templates(self):
        # load re.png
        self.templates['re'] = cv_imread(glob.glob('{}\\images\\re.png'.format(self.path))[0])
        # load skip.png
        self.templates['skip'] = cv_imread(glob.glob('{}\\images\\skip.png'.format(self.path))[0])
        # load required list
        self.templates['required'] = [cv_imread(f) for f in self.required_list]
        # load optional list
        self.templates['optional'] = [cv_imread(f) for f in self.optional_list]

        return self.templates

    def match_template(self, template):
        '''
        bg_img = self.adb.screencap()
        h, w, _ = template.shape
        res = cv2.matchTemplate(bg_img, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        top_left = max_loc
        bottom_right = (top_left[0] + w, top_left[1] + h)
        cv2.rectangle(bg_img,top_left, bottom_right, 255, 2)
        cv2.imshow('Result', bg_img)
        cv2.waitKey(0)
        '''
        bg_img = self.adb.screencap(self.device)
        res = cv2.matchTemplate(bg_img, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(res)
        return (max_val, max_loc)

    def tap_screen(self, x, y):
        self.adb.tap(self.device, x, y)
        return 1


