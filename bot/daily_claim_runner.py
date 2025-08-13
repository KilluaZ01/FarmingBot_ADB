import subprocess
from datetime import datetime
import json
import time
import os
from macros import tap_macro
from path_utils import get_persistent_path
import cv2
import numpy as np
import threading
from adb_utils import find_template_on_screen
from template_matching import is_template_present

TEMPLATE_PATHS = ["D:/Silver_Blood_Bot/templates/start_template.png"]
ANOTHER_TEMPLATES = ["D:/Silver_Blood_Bot/templates/download_template.png"]
SCREENSHOT_DIR = "D:/Silver_Blood_Bot/screenshots"

def take_screenshot_another(instance_name, login_day=None):
    remote_path = "/sdcard/result.png"

    # Optional: include day in filename
    suffix = f"_day{login_day}" if login_day else ""
    filename = f"{instance_name}{suffix}.png"
    local_path = os.path.join(SCREENSHOT_DIR, filename)

    # Step 1: Take screenshot inside emulator
    screencap_cmd = [
        "ldconsole.exe", "adb",
        "--name", instance_name,
        "--command", f"shell screencap -p {remote_path}"
    ]
    result1 = subprocess.run(screencap_cmd, capture_output=True, text=True)
    if result1.returncode != 0:
        print(f"[{instance_name}] ❌ Error during screencap: {result1.stderr.strip()}")
        return None

    # Step 2: Pull screenshot
    pull_cmd = [
        "ldconsole.exe", "adb",
        "--name", instance_name,
        "--command", f'pull {remote_path} "{local_path}"'
    ]
    result2 = subprocess.run(pull_cmd, capture_output=True, text=True)
    if result2.returncode != 0:
        print(f"[{instance_name}] ❌ Error during pull: {result2.stderr.strip()}")
        return None

    print(f"[{instance_name}] 📸 Screenshot saved as {filename}")
    return local_path

def detect_regular_summon(instance_name, template_path, threshold=0.80):
    screenshot_path = take_screenshot_another(instance_name)  # You can reuse existing screenshot logic
    if not screenshot_path:
        return None

    screenshot = cv2.imread(screenshot_path, 0)
    if screenshot is None:
        print(f"❌ Could not load screenshot: {screenshot_path}")
        return None

    template = cv2.imread(template_path, 0)
    if template is None:
        print(f"❌ Could not load summon template: {template_path}")
        return None

    result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)

    print(f"[{instance_name}] 🎯 Regular summon match: {max_val:.2f}")
    os.remove(screenshot_path)

    if max_val >= threshold:
        # Return center of matched area
        x = max_loc[0] + template.shape[1] // 2
        y = max_loc[1] + template.shape[0] // 2
        return (x, y)

    return None

def is_template_present_only(instance_name, template_path, threshold=0.8):
    screenshot_path = take_screenshot_another(instance_name)
    if not screenshot_path:
        return False

    img = cv2.imread(screenshot_path, 0)
    template = cv2.imread(template_path, 0)

    if img is None or template is None:
        print(f"❌ Error loading image or template.")
        return False

    result = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, _ = cv2.minMaxLoc(result)

    os.remove(screenshot_path)
    return max_val >= threshold

def detect_screen(instance_name, threshold=0.70):
    screenshot_path = take_screenshot_another(instance_name)
    if not screenshot_path:
        return "unknown"

    screenshot = cv2.imread(screenshot_path, 0)
    if screenshot is None:
        print(f"❌ Could not load screenshot: {screenshot_path}")
        return "unknown"

    # 🧠 Map screen types to a single template path each
    TEMPLATES = {
        "download": "D:/Silver_Blood_Bot/templates/download_template.png",
        "start": "D:/Silver_Blood_Bot/templates/start_template.png"
    }

    for screen_type, template_path in TEMPLATES.items():
        template = cv2.imread(template_path, 0)
        if template is None:
            print(f"❌ Could not load {screen_type} template: {template_path}")
            continue

        res = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, _ = cv2.minMaxLoc(res)

        print(f"[{instance_name}] 🔍 {screen_type.capitalize()} match: {max_val:.2f}")
        if max_val >= threshold:
            os.remove(screenshot_path)
            return screen_type

    os.remove(screenshot_path)
    return "unknown"

def perform_10x_summon(instance_name):
    back_template = "D:/Silver_Blood_Bot/templates/back_button.png"  # your back button image
    max_attempts = 15  # allow enough time for full animation cycle

    print(f"[{instance_name}] 🚀 Starting 10x summon skip loop...")

    for attempt in range(max_attempts):
        print(f"[{instance_name}] ⏩ Skip tap #{attempt+1}")
        tap_macro(instance_name, 1173, 53)
        time.sleep(5)  # adjust based on actual animation speed

        if is_template_present_only(instance_name, back_template, threshold=0.8):
            print(f"[{instance_name}] ✅ Summon animation finished. Back button detected.")
            break
    else:
        print(f"[{instance_name}] ⚠️ Max skip attempts reached. Proceeding anyway.")


def ensure_all_start_screens(instance_names, max_retries=3, threshold=0.70):
    for attempt in range(1, max_retries + 1):
        print(f"\n🔁 Start Screen Check Attempt {attempt}")
        not_ready = []

        for instance_name in instance_names:
            screen_type = detect_screen(instance_name, threshold=threshold)

            if screen_type != "start":
                print(f"[{instance_name}] ❌ On '{screen_type}' screen, retrying launch...")
                os.system(f'ldconsole.exe adb --name "{instance_name}" --command "shell am force-stop com.skystone.silverblood.us"')
                time.sleep(3)
                os.system(f'ldconsole.exe adb --name "{instance_name}" --command "shell monkey -p com.skystone.silverblood.us -c android.intent.category.LAUNCHER 1"')
                not_ready.append(instance_name)
            else:
                print(f"[{instance_name}] ✅ Start screen detected.")

        if not not_ready:
            print("✅ All instances are on the start screen.")
            return True

        time.sleep(100)  # Give time to reload app

    print("❌ Could not reach start screen in all instances after retries.")
    return False

def launch_instance(instance_name):
    subprocess.run(f'ldconsole.exe launch --name "{instance_name}"', shell=True)

def should_claim_today(batch):
    today = datetime.now().strftime("%Y-%m-%d")
    return batch["last_login"] != today and batch["login_day"] <= 14

def is_instance_present(instance_name):
    # Fetch all LDPlayer instances
    output = os.popen("ldconsole.exe list2").read()
    return instance_name in output

path_close_button = "D:/Silver_Blood_Bot/templates/close_button.png"

def do_summon_7days(instance_name):
    coords_close = detect_regular_summon(instance_name, template_path=path_close_button)
    if coords_close:
        print(f"🎯 Tapping close at {coords_close}")
        tap_macro(instance_name, coords_close[0], coords_close[1])
        time.sleep(5)

        tap_macro(instance_name, 1, 1)
        time.sleep(5)

    else:
        print(f"❌ Could not find close for {instance_name}")

    coords_close = detect_regular_summon(instance_name, template_path=path_close_button)
    if coords_close:
        print(f"🎯 Tapping close at {coords_close}")
        tap_macro(instance_name, coords_close[0], coords_close[1])
        time.sleep(5)

        tap_macro(instance_name, 1, 1)
        time.sleep(5)
    else:
        print(f"❌ Could not find regular summon banner for {instance_name}")

    coords_close = detect_regular_summon(instance_name, template_path=path_close_button)
    if coords_close:
        print(f"🎯 Tapping Close at {coords_close}")
        tap_macro(instance_name, coords_close[0], coords_close[1])
        time.sleep(5)

        tap_macro(instance_name, 1, 1)
        time.sleep(5)
    else:
        print(f"❌ Could not find regular summon banner for {instance_name}")

    print(f"Back")   
    tap_macro(instance_name, 1, 1)
    time.sleep(5)

    print(f"Back")   
    tap_macro(instance_name, 1, 1)
    time.sleep(10)

    print('Embrace')
    tap_macro(instance_name, 400, 650)
    time.sleep(10)

    coords = detect_regular_summon(instance_name, template_path="D:/Silver_Blood_Bot/templates/regular_summon_template.png")

    if coords:
        print(f"🎯 Tapping regular summon at {coords}")
        tap_macro(instance_name, coords[0], coords[1])
        time.sleep(5)
    else:
        print(f"❌ Could not find regular summon banner for {instance_name}")

    print('10x')
    tap_macro(instance_name, 1130, 650)
    time.sleep(5)

    print(f"[{instance_name}] ⏩ Skip tap")
    tap_macro(instance_name, 1173, 53)
    time.sleep(5) 

    perform_10x_summon(instance_name)

    print('Back')
    tap_macro(instance_name, 470, 630)
    time.sleep(10)

    print('Back')
    tap_macro(instance_name, 1, 1)
    time.sleep(5)

    print('Back')
    tap_macro(instance_name, 1, 1)
    time.sleep(5)

    print('Back')
    tap_macro(instance_name, 1, 1)
    time.sleep(10)

    print(f"Vassal Clicking")
    tap_macro(instance_name, 70, 650)
    time.sleep(5)

    take_screenshot_another(instance_name, login_day=7)
    time.sleep(5)

    print('Back')
    tap_macro(instance_name, 1, 1)
    time.sleep(5)

    print('Back')
    tap_macro(instance_name, 1, 1)
    time.sleep(5)

def do_summon_14days(instance_name):
    coords_close = detect_regular_summon(instance_name, template_path=path_close_button)
    if coords_close:
        print(f"🎯 Tapping Close at {coords_close}")
        tap_macro(instance_name, coords_close[0], coords_close[1])
        time.sleep(5)

        tap_macro(instance_name, 1, 1)
        time.sleep(5)

    else:
        print(f"❌ Could not find regular summon banner for {instance_name}")

    coords_close = detect_regular_summon(instance_name, template_path=path_close_button)
    if coords_close:
        print(f"🎯 Tapping Close at {coords_close}")
        tap_macro(instance_name, coords_close[0], coords_close[1])
        time.sleep(5)

        tap_macro(instance_name, 1, 1)
        time.sleep(5)
    else:
        print(f"❌ Could not find regular summon banner for {instance_name}")

    coords_close = detect_regular_summon(instance_name, template_path=path_close_button)
    if coords_close:
        print(f"🎯 Tapping Close summon at {coords_close}")
        tap_macro(instance_name, coords_close[0], coords_close[1])
        time.sleep(5)

        tap_macro(instance_name, 1, 1)
        time.sleep(5)
    else:
        print(f"❌ Could not find regular summon banner for {instance_name}")

    print(f"Back")   
    tap_macro(instance_name, 1, 1)
    time.sleep(5)

    print(f"Back")   
    tap_macro(instance_name, 1, 1)
    time.sleep(5)

    print('Embrace')
    tap_macro(instance_name, 400, 650)
    time.sleep(10)

    print('10x')
    tap_macro(instance_name, 1130, 650)
    time.sleep(40)

    print(f"[{instance_name}] ⏩ Skip tap")
    tap_macro(instance_name, 1173, 53)
    time.sleep(5) 

    perform_10x_summon(instance_name)

    print('Again')
    tap_macro(instance_name, 818, 633)
    time.sleep(18)

    print(f"[{instance_name}] ⏩ Skip tap")
    tap_macro(instance_name, 1173, 53)
    time.sleep(5) 

    perform_10x_summon(instance_name)

    print('Back')
    tap_macro(instance_name, 470, 630)
    time.sleep(10)

    print('Back')
    tap_macro(instance_name, 1, 1)
    time.sleep(5)

    print('Back')
    tap_macro(instance_name, 1, 1)
    time.sleep(5)

    print('Back')
    tap_macro(instance_name, 1, 1)
    time.sleep(5)

    print('Embrace')
    tap_macro(instance_name, 400, 650)
    time.sleep(10)

    coords = detect_regular_summon(instance_name, template_path="D:/Silver_Blood_Bot/templates/regular_summon_template.png")

    if coords:
        print(f"🎯 Tapping regular summon at {coords}")
        tap_macro(instance_name, coords[0], coords[1])
        time.sleep(5)
    else:
        print(f"❌ Could not find regular summon banner for {instance_name}")

    print('10x')
    tap_macro(instance_name, 1130, 650)
    time.sleep(18)

    print(f"[{instance_name}] ⏩ Skip tap")
    tap_macro(instance_name, 1173, 53)
    time.sleep(5) 

    perform_10x_summon(instance_name)

    print('Back')
    tap_macro(instance_name, 470, 630)
    time.sleep(10)

    print('Back')
    tap_macro(instance_name, 470, 630)
    time.sleep(10)

    print('Back')
    tap_macro(instance_name, 470, 630)
    time.sleep(10)

    print('Tap')
    tap_macro(instance_name, 1191, 144)
    time.sleep(10)

    print('Global')
    tap_macro(instance_name, 470, 630)
    time.sleep(10)

    print('Add')
    tap_macro(instance_name, 650, 250)
    time.sleep(10)

    print('Global')
    tap_macro(instance_name, 650, 250)
    time.sleep(10)

    print('Global')
    tap_macro(instance_name, 650, 250)
    time.sleep(10)

    print('Global')
    tap_macro(instance_name, 650, 250)
    time.sleep(10)

    print('Cancel')
    tap_macro(instance_name, 710, 650)
    time.sleep(10)

    print('Back')
    tap_macro(instance_name, 1, 1)
    time.sleep(5)

    print('Confirm')
    tap_macro(instance_name, 825, 500)
    time.sleep(5)

    print('10x')
    tap_macro(instance_name, 1130, 650)
    time.sleep(18)

    print(f"[{instance_name}] ⏩ Skip tap")
    tap_macro(instance_name, 1173, 53)
    time.sleep(5) 

    perform_10x_summon(instance_name)

    print('Back')
    tap_macro(instance_name, 470, 630)
    time.sleep(10)

    print('Back')
    tap_macro(instance_name, 1, 1)
    time.sleep(5)

    print('Back')
    tap_macro(instance_name, 1, 1)
    time.sleep(5)

    print('Back')
    tap_macro(instance_name, 1, 1)
    time.sleep(10)

    print(f"Vassal Clicking")
    tap_macro(instance_name, 70, 650)
    time.sleep(5)

    take_screenshot_another(instance_name, login_day=14)
    time.sleep(5)

    print('Back')
    tap_macro(instance_name, 1, 1)
    time.sleep(5)

    print('Back')
    tap_macro(instance_name, 1, 1)
    time.sleep(5)

def claim_login_rewards():
    json_path = get_persistent_path('batches.json')
    with open(json_path, "r") as f:
        batches = json.load(f)

    updated_batches = []

    for batch in batches:
        if not should_claim_today(batch):
            updated_batches.append(batch)
            continue

        instance_names = batch["instance_names"]
        guest_names = batch["guest_names"]

        # ✅ Filter out instances that are no longer present in LDPlayer
        valid_instance_names = []
        valid_guest_names = []

        for i, instance in enumerate(instance_names):
            if is_instance_present(instance):
                valid_instance_names.append(instance)
                valid_guest_names.append(guest_names[i])
            else:
                print(f"⚠️ Skipping missing instance: {instance}")

        # 🧹 If no valid instances remain, skip this batch
        if not valid_instance_names:
            print(f"🗑️ Removing batch {batch['batch_id']} due to no valid instances.")
            continue

        # Update instance and guest names
        batch["instance_names"] = valid_instance_names
        batch["guest_names"] = valid_guest_names

        # 🚀 Launch valid instances
        for instance in valid_instance_names:
            launch_instance(instance)
        time.sleep(50)

        for instance_name in valid_instance_names:
            os.system(f'ldconsole.exe adb --name "{instance_name}" --command "shell monkey -p com.skystone.silverblood.us -c android.intent.category.LAUNCHER 1"')
            print(f"[{instance_name}] - Launched Silver and Blood")
        time.sleep(100)

        # 📱 Download screen logic
        screen = detect_screen(valid_instance_names[0])  # Only check one to decide
        if screen == "download":
            print(f"[{valid_instance_names[0]}] ⬇️ Detected download screen.")
            for instance in valid_instance_names:
                tap_macro(instance, 605, 495)
            time.sleep(60)
            for instance in valid_instance_names:
                tap_macro(instance, 625, 495)
            time.sleep(10)
            for instance in valid_instance_names:
                os.system(f'ldconsole.exe adb --name "{instance}" --command "shell monkey -p com.skystone.silverblood.us -c android.intent.category.LAUNCHER 1"')
            time.sleep(100)

        success = ensure_all_start_screens(valid_instance_names)
        if not success:
            print("❌ Aborting: Some instances failed to reach start screen.")
            continue

        print("Closing Notice!")
        for instance in valid_instance_names:
            tap_macro(instance, 800, 500)
        time.sleep(10)

        day = batch["login_day"]
        print("📦 Claiming Login Reward...")

        taps_needed = 11 
        for _ in range(taps_needed):
            for instance in valid_instance_names:
                tap_macro(instance, 667, 675)
            time.sleep(4)

        path_close_button = "D:/Silver_Blood_Bot/templates/close_button.png"

        for instance_name in valid_instance_names:
            tap_macro(instance_name, 1, 1)
            time.sleep(3)
            coords_close = detect_regular_summon(instance_name, template_path=path_close_button)
            if coords_close:
                print(f"🎯 Tapping close at {coords_close}")
                tap_macro(instance_name, coords_close[0], coords_close[1])
                time.sleep(5)
            else:
                print(f"❌ Could not find regular summon banner for {instance_name}")

        for instance_name in valid_instance_names:
            tap_macro(instance_name, 1, 1)
            time.sleep(3)
            coords_close = detect_regular_summon(instance_name, template_path=path_close_button)
            if coords_close:
                print(f"🎯 Tapping close at {coords_close}")
                tap_macro(instance_name, coords_close[0], coords_close[1])
                time.sleep(5)
            else:
                print(f"❌ Could not find regular summon banner for {instance_name}")
        
        for instance_name in valid_instance_names:
            tap_macro(instance_name, 1, 1)
            time.sleep(2)
            coords_close = detect_regular_summon(instance_name, template_path=path_close_button)
            if coords_close:
                print(f"🎯 Tapping close at {coords_close}")
                tap_macro(instance_name, coords_close[0], coords_close[1])
                time.sleep(5)
            else:
                print(f"❌ Could not find regular summon banner for {instance_name}")

        if day == 7:
            print(f"✨ Performing 10x summon for batch {batch['batch_id']} on Day {day}")
            
            threads = []
            for instance_name in valid_instance_names:
                t = threading.Thread(target=do_summon_7days, args=(instance_name,))
                t.start()
                threads.append(t)

            # Wait for all threads to finish
            for t in threads:
                t.join()

        elif day == 14:
            print(f"✨ Performing 10x summon for batch {batch['batch_id']} on Day {day}")
            
            threads = []
            for instance_name in valid_instance_names:
                t = threading.Thread(target=do_summon_14days, args=(instance_name,))
                t.start()
                threads.append(t)

            # Wait for all threads to finish
            for t in threads:
                t.join()
        
        template_path = "D:/Silver_Blood_Bot/templates/chapter_matcher.png"
        reached = True        

        for instance_name in valid_instance_names:
            print(f"[{instance_name}] Taking screenshot")
            screenshot_path = take_screenshot_another(instance_name)

            if is_template_present(screenshot_path, template_path, threshold=0.80):
                print(f"[{instance_name}] ✅ Successfully reached login reward screen.")
            else:
                reached = False
                print(f"[{instance_name}] ❌ Failed to reach reward screen. Closing instance.")
                
        
        if reached:
            batch["login_day"] += 1
            batch["last_login"] = datetime.now().strftime("%Y-%m-%d")
            updated_batches.append(batch)
        else:
            batch["status"] = "Inactive"
            updated_batches.append(batch)

        for instance in valid_instance_names:
            os.system(f'ldconsole.exe quit --name {instance}')
        time.sleep(5)

        # 💾 Write updated batch list to file
        with open(json_path, "w") as f:
            json.dump(updated_batches, f, indent=2)

    print("✅ Finished all eligible login batches.")

if __name__ == "__main__":
    claim_login_rewards()