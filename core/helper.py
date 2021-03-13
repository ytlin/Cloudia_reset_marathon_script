import os
import subprocess
from cv2 import cv2
import glob
import numpy as np

class adb():
    def __init__(self, path):
        self.path = path ##
        self.adb_exe = '{}\\platform-tools\\adb.exe'.format(self.path)

    def start_ADB_server(self):
        subprocess.Popen('{} start-server'.format(self.adb_exe), stdout=subprocess.PIPE).stdout.read()
        return self

    def list_devices(self):
        out = subprocess.Popen('{} devices'.format(self.adb_exe), stdout=subprocess.PIPE)
        return out.stdout.read()

    def screencap(self):
        out = subprocess.Popen('{} shell screencap -p'.format(self.adb_exe), stdout=subprocess.PIPE)
        bytes_arr = np.frombuffer(out.stdout.read().replace(b'\r\n', b'\n'), dtype='uint8')
        img = cv2.imdecode(bytes_arr, cv2.IMREAD_COLOR)
       
        return img

    def tap(self, x, y):
        out = subprocess.Popen('{} shell input tap {} {}'.format(self.adb_exe, x, y), stdout=subprocess.PIPE)
        return out.stdout.read()


def cv_imread(path):
    img = cv2.imdecode(np.fromfile(path, dtype=np.uint8), cv2.IMREAD_COLOR)
    return img

class helper():

    def __init__(self, path):
        self.path = path
        self.adb = adb(self.path).start_ADB_server()
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


