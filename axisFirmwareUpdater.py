import requests
from requests.auth import HTTPDigestAuth
import hashlib

cam_address = ''
cam_username = ''
cam_password = ''
axis_firmware_bin = 'V5915_5_75_1_11.bin'
axis_firmware_hash = '82e44e68b580626b568b07a1b7258b445ab8e22ff4f18ddc167cf87588f0ec46'


def get_file_hash():
    filename = axis_firmware_bin
    sha256_hash = hashlib.sha256()
    with open(filename,"rb") as f:
        # Read and update hash string value in blocks of 4K
        for byte_block in iter(lambda: f.read(4096),b""):
            sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()


if axis_firmware_hash == get_file_hash():
    print("yay!")

headers = {'X-Requested-Auth': 'Digest'}
files = {'file': open(axis_firmware_bin, 'rb')}
response = requests.post('http://{}/axis-cgi/firmwareupgrade.cgi'.format(cam_address), headers=headers, auth=HTTPDigestAuth(cam_username, cam_password), files=files)
print(response.status_code)
print(response.content)

