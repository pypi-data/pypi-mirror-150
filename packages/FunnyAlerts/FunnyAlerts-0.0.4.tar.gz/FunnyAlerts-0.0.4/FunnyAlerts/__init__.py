import pyautogui

def dumb():
    while True:
        a = pyautogui.confirm("Are you dumb?", buttons=['Yes', 'No'])
        if (a == "Yes"):
            break

def gey():
    while True:
        a = pyautogui.confirm("Are you gey?", buttons=['Yes', 'No'])
        if (a == "Yes"):
            break
