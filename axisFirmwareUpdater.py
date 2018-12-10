import requests
from requests.auth import HTTPDigestAuth
import hashlib
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
conf = config['DEFAULT']

cam_username = conf['cam_username']
cam_password = conf['cam_password']
cam_list = conf['cam_list']
axis_firmware_bin = 'firmware/' + conf['axis_firmware_bin']
axis_firmware_hash = conf['axis_firmware_hash']


def get_file_hash():
    filename = axis_firmware_bin
    sha256_hash = hashlib.sha256()
    try:
        with open(filename,"rb") as f:
            # Read and update hash string value in blocks of 4K
            for byte_block in iter(lambda: f.read(4096),b""):
                sha256_hash.update(byte_block)
            return sha256_hash.hexdigest()
    except IOError as fileerror:
        print('firmware file not found: ERROR! ' + str(fileerror))


def check_hash():
    if axis_firmware_hash == get_file_hash():
        return True
    else:
        return False


def run_update(cam_address):
    print('uploading firmware to the camera, please wait')
    headers = {'X-Requested-Auth': 'Digest'}
    try:
        files = {'file': open(axis_firmware_bin, 'rb')}
    except IOError as fileerror:
        print('firmware file not found: ERROR! ' + str(fileerror))

    try:
        response = requests.post('http://{}/axis-cgi/firmwareupgrade.cgi'.format(cam_address), headers=headers, auth=HTTPDigestAuth(cam_username, cam_password), files=files)
    except Exception as e:
        print('network error communication with the camera: ERROR ' + str(e))
        return
    print('Status code: ' + response.status_code)
    print(response.content)


for i in cam_list.split():
    if check_hash():
        print('firmware file matches given checksum: OK!')
        run_update(i)
    else:
        print('firmware file possibly corrupted, please re-download firmware: ERROR!')
