import subprocess
import numpy as np
from cv2 import cv2
from ppadb.client import Client as AdbClient


class adb():
    def __init__(self, path: str) -> None:
        self.path = path ##
        self.adb_exe = '{}\\platform-tools\\adb.exe'.format(self.path)
    
    def connect_to_BS(self, ip: str, port: int) -> None:
        '''
        待測試 => 重開機直接執行
        '''
        self.client = AdbClient(host="127.0.0.1", port=5037)
        try:
            self.client.remote_connect(ip, port)
        except:
            subprocess.Popen('{} start-server'.format(self.adb_exe), stdout=subprocess.PIPE).stdout.read()
        print('Connect success!')

    def list_devices(self) -> None:
        devices = self.client.devices()
        print('List of devices attached:')
        for device in devices:
            print('    {}'.format(device.serial))
    
    def tap(self, device, x: str, y: str) -> None:
        device.shell('input tap {} {}'.format(x, y))

    def get_device(self, serial: str):
        return self.client.device(serial)

    def screencap(self, device):
        image_bytes = device.screencap()
        img = cv2.imdecode(np.frombuffer(image_bytes, dtype='uint8'), cv2.IMREAD_COLOR)
        return img