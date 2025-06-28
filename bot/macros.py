import pygetwindow as gw
import pyautogui
import time

def trigger_macro(instance_title, key1, key2):
    windows = [w for w in gw.getWindowsWithTitle(instance_title) if instance_title in w.title]
    if not windows:
        print(f"[{instance_title}] ❌ Window not found.")
        return

    try:
        win = windows[0]
        if win.isMinimized:
            win.restore()
            time.sleep(0.5)

        retries = 3
        for attempt in range(retries):
            win.activate()
            time.sleep(0.7)
            if win.isActive:
                break
            else:
                print(f"[{instance_title}] Attempt {attempt+1} to activate window failed.")
        else:
            print(f"[{instance_title}] ⚠️ Failed to activate window after {retries} attempts.")
            return

        print(f"[{instance_title}] Sending {key1} + {key2}")
        pyautogui.hotkey(key1, key2)

    except Exception as e:
        print(f"[{instance_title}] ⚠️ Error while triggering macro: {e}")
