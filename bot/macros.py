import pyautogui

def trigger_macro(key1, key2):
    print(f"Sending {key1} + {key2}")
    pyautogui.hotkey(key1, key2)