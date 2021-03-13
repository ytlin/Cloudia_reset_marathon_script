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
    
    def connect_to_server(self, ip, port):
        self.client = AdbClient(host=ip, port=port)
        try:
            v = self.client.version()
        except:
            subprocess.Popen('{} start-server'.format(self.adb_exe), stdout=subprocess.PIPE).stdout.read()
            v = self.client.version()
        print('Connect success! Version {}'.format(v))

        return 1

    def list_devices(self):
        devices = self.client.devices()
        print('List of devices attached:')
        for device in devices:
            print(device.serial)

        return 1

    def screencap(self):
        pass
      

    def tap(self, x, y):
        pass

project_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
a = adb(project_path)
a.connect_to_server('127.0.0.1', 5037)
a.list_devices()

def cv_imread(path):
    img = cv2.imdecode(np.fromfile(path, dtype=np.uint8), cv2.IMREAD_COLOR)
    return img

class helper():

    def __init__(self, path):
        self.path = path
        self.adb = adb(self.path)
        self.templates = {}
        self.required_list = glob.glob('{}\\images\\required\\*.png'.format(self.path))
        self.optional_list = glob.glob('{}\\images\\optional\\*.png'.format(self.path))

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
        bg_img = self.adb.screencap()
        res = cv2.matchTemplate(bg_img, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(res)
        return (max_val, max_loc)

    def tap_screen(self, x, y):
        self.adb.tap(x, y)
        return 1


