from cv2 import cv2
import glob
import numpy as np

from .adb import adb


def cv_imread(path: str):
    img = cv2.imdecode(np.fromfile(path, dtype=np.uint8), cv2.IMREAD_COLOR)
    return img

class helper():

    def __init__(self, path: str) -> None:
        self.path = path
        self.adb = None
        self.device = None
        self.templates = {}
        self.required_list = glob.glob('{}\\images\\required\\*.png'.format(self.path))
        self.optional_list = glob.glob('{}\\images\\optional\\*.png'.format(self.path))

    def setup_adb_client(self) -> None:
        self.adb = adb(self.path)
        self.adb.connect_to_BS('127.0.0.1', 5555)
        self.adb.list_devices()
        serial = input('Please select the device by its serial number: ')
        self.device = self.adb.get_device(serial)

    def load_templates(self) -> dict:
        # load re.png
        self.templates['re'] = cv_imread(glob.glob('{}\\images\\re.png'.format(self.path))[0])
        # load skip.png
        self.templates['skip'] = cv_imread(glob.glob('{}\\images\\skip.png'.format(self.path))[0])
        # load required list
        self.templates['required'] = [cv_imread(f) for f in self.required_list]
        # load optional list
        self.templates['optional'] = [cv_imread(f) for f in self.optional_list]

        return self.templates

    def match_template(self, template) -> (float, float):
        bg_img = self.adb.screencap(self.device)
        res = cv2.matchTemplate(bg_img, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, max_loc = cv2.minMaxLoc(res)
        return (max_val, max_loc)

    def tap_screen(self, x: str, y: str) -> None:
        self.adb.tap(self.device, x, y)

