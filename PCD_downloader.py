import pyautogui
import time
import keyboard
from subprocess import Popen
import numpy as np
import os

# file ref.dat contains list of all valid PCD reference numbers

with open(r'ref.dat') as f:  # if not in the same folder, path to ref.dat must be given
    data = np.genfromtxt(f, usecols=(0,))
    x = data[:]
    ref_numbers = np.array(x)  # makes a numpy array of valid Pearson ref numbers

downloaded_refs = np.array([])  # reference numbers of downloaded entries will be stored in this array

for filename in os.listdir(r'C:\Users\User1\Documents\all_PCD'):  # path to destination folder must be given
    if filename.endswith('cif'):
        downloaded_ref = int(filename.split(".")[0])
        downloaded_refs = np.append(downloaded_refs, downloaded_ref)

# refs_to_get is array of ref numbers that are not yet downloaded

refs_to_get = np.array([i for i in ref_numbers if i not in downloaded_refs])

time.sleep(2)

start_range = 0

entry_range = 6  # range of reference numbers to retrieve in one session (limited by the search field length)

t_between = 0.3  # time between clicks/ other actions


def clicker_download(range_of_refs):
    i = 0
    while i < range_of_refs + 1:
        pyautogui.typewrite(["enter"])  # pressing "Enter" closes any error message, e.g., from Lazy Pulverix
        time.sleep(t_between)
        pyautogui.click(770, 60)  # coordinates of "Export" button must be adjusted
        time.sleep(t_between)
        pyautogui.click(770, 90)  # coordinates of "Export to cif" button must be adjusted
        time.sleep(t_between)
        pyautogui.typewrite(["enter"])
        time.sleep(t_between)
        i += 1
        pyautogui.typewrite(["down"])
        time.sleep(t_between)
        if keyboard.is_pressed("q"):  # press "q" to interrupt
            break


while start_range < len(refs_to_get) + 1:
    Popen(['C:\\Program Files (x86)\\Pearsons Crystal Data\\PCD.exe'], shell=True)  # opens database
    time.sleep(1)
    pyautogui.click(166, 34)  # coordinates of "Search" button must be adjusted
    time.sleep(t_between)
    pyautogui.click(166, 80)  # coordinates of "Selection criteria..." button must be adjusted
    time.sleep(t_between)
    # The default "Selection criteria..." tab must be "Processing information"
    for ref_number in refs_to_get[start_range: start_range + entry_range + 1]:
        pyautogui.typewrite("{};".format(int(ref_number)))
    pyautogui.typewrite(["enter"])
    time.sleep(t_between)
    pyautogui.typewrite(["enter"])
    time.sleep(3)
    clicker_download(entry_range)
    Popen('TASKKILL /F /IM PCD.exe')  # closes database
    time.sleep(t_between)
    start_range = start_range+entry_range+1
    if keyboard.is_pressed("q"):  # press "q" to interrupt
        break
