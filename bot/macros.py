import os
import time
import subprocess

SCREENSHOT_DIR = "D:/Silver_Blood_Bot/screenshots"

def take_screenshot(instance_name, login_day=None):
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

def tap_macro(instance_name, x, y):
    tap_command = f'ldconsole.exe adb --name {instance_name} --command "shell input tap {x} {y}"'
    os.system(tap_command)

def swipe_macro(instance_name, x1, y1, x2, y2):
    tap_command = f'ldconsole.exe adb --name {instance_name} --command "shell input touchscreen swipe {x1} {y1} {x2} {y2} 1000"'
    os.system(tap_command)

def Till_New_Summon(instance_names):
    print('Incase')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 1, 1)
    time.sleep(2)

    print('Incase')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 1, 1)
    time.sleep(3)

    # Start From here After all
    # print(f"Open Event")   
    # for instance_name, _ in instance_names:
    #     tap_macro(instance_name, 1104, 114)
    # time.sleep(10)

    # For Entering Chapter
    print('Thread of Fate')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 1135, 630)
    time.sleep(15)

    print('Thread of Fate')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 1135, 630)
    time.sleep(10)

    print('Start')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 1005, 630)
    time.sleep(25)

    print('Skip')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 1210, 50)
    time.sleep(15)

    print('Skip')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 1210, 50)
    time.sleep(10)

    print('Global')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 1058, 183)
    time.sleep(10)

    print('Complete')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 1165, 625)
    time.sleep(10)

    print('Continue')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 455, 500)
    time.sleep(10)

    print('Global')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 1058, 183)
    time.sleep(10)

    print('Global')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 1058, 183)
    time.sleep(40)

    print('Global')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 1058, 183)
    time.sleep(10)

    print('Vassal')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 482, 615)
    time.sleep(15)

    print('Hero')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 285, 255)
    time.sleep(10)

    print('Add')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 1100, 315)
    time.sleep(10)

    print('Max')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 1195, 540)
    time.sleep(10)

    print('Upgrade')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 1075, 650)
    time.sleep(10)

    print('Back')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 55, 40)
    time.sleep(10)

    print('Back')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 55, 40)
    time.sleep(10)

    print('Hero')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 285, 255)
    time.sleep(10)

    print('Tap')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 70, 415)
    time.sleep(10)

    print('Global')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 1, 1)
    time.sleep(8)

    print('Global')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 1, 1)
    time.sleep(8)

    print('Global')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 1, 1)
    time.sleep(8)

    print('Global')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 1, 1)
    time.sleep(8)

    print('Global')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 1, 1)
    time.sleep(8)

    print('Back')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 55, 40)
    time.sleep(8)

    print('Back')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 55, 40)
    time.sleep(8)

    print('Threads')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 1135, 630)
    time.sleep(10)

    print('Threads')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 1135, 630)
    time.sleep(10)

    print('Start')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 1005, 630)
    time.sleep(20)

    print('Skip')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 1210, 50)
    time.sleep(10)

    print('Skip')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 1210, 50)
    time.sleep(8)

    print('Global')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 1058, 183)
    time.sleep(8)

    print('Swipe')
    for instance_name, _ in instance_names:
        swipe_macro(instance_name, 655, 630, 480, 315)
    time.sleep(3)

    print('Swipe')
    for instance_name, _ in instance_names:
        swipe_macro(instance_name, 655, 630, 350, 405)
    time.sleep(3)

    print('Complete')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 1165, 625)
    time.sleep(10)

    print('Global')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 1058, 183)
    time.sleep(5)

    print('Global')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 1058, 183)
    time.sleep(35)

    print('Continue -> 1-5 Completed')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 1058, 183)
    time.sleep(20)      # 1-5 Completed

    print('Global')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 1058, 183)
    time.sleep(10)

    print('1-6 Click')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 1005, 630)
    time.sleep(10)

    print('Start')  
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 1005, 630)
    time.sleep(20)

    print('Skip')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 1210, 50)
    time.sleep(15)

    print('Global')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 1058, 183)
    time.sleep(10)

    print('Global')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 1058, 183)
    time.sleep(10)

    print('Global')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 1058, 183)
    time.sleep(10)

    print('Complete')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 1165, 625)
    time.sleep(20)

    print('Mixed')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 925, 620)
    time.sleep(1)

    print('Mixed')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 380, 422)
    time.sleep(3)

    print('Mixed')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 925, 620)
    time.sleep(1)

    print('Mixed')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 380, 422)
    time.sleep(3)

    print('Mixed')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 925, 620)
    time.sleep(1)

    print('Mixed')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 380, 422)
    time.sleep(3)

    print('Mixed')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 925, 620)
    time.sleep(1)

    print('Mixed')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 380, 422)
    time.sleep(30)

    print('Skip')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 1210, 50)
    time.sleep(10)

    print('Global')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 1, 1)
    time.sleep(10)

    print('Skip')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 1210, 50)
    time.sleep(20)

    print('Skip')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 1210, 50)
    time.sleep(10)

    print('Global')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 1, 1)
    time.sleep(10)

    print('Global')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 1, 1)
    time.sleep(10)

    print('Sword')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 815, 175)
    time.sleep(10)

    print('Start')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 1005, 630)
    time.sleep(20)

    # Sword
    print('Complete')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 1165, 625)
    time.sleep(35)

    print('Global')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 1189, 650)
    time.sleep(15)

    print('Start')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 1005, 630)
    time.sleep(10)

    print('Start')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 1005, 630)
    time.sleep(20)

    print('Skip')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 1210, 50)
    time.sleep(10)

    # 1-7
    print('Complete')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 1165, 625)
    time.sleep(10)

    print('Mixed')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 925, 620)
    time.sleep(1)

    print('Mixed')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 380, 422)
    time.sleep(3)

    print('Mixed')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 925, 620)
    time.sleep(1)

    print('Mixed')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 380, 422)
    time.sleep(3)

    print('Mixed')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 925, 620)
    time.sleep(1)

    print('Mixed')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 380, 422)
    time.sleep(3)

    print('Mixed')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 1024, 620)
    time.sleep(1)

    print('Mixed')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 380, 422)
    time.sleep(3)

    print('Mixed')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 1182, 620)
    time.sleep(1)

    print('Mixed')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 380, 422)
    time.sleep(3)

    print('Mixed')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 925, 620)
    time.sleep(1)

    print('Mixed')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 380, 422)
    time.sleep(3)

    print('Mixed')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 1024, 620)
    time.sleep(1)

    print('Mixed')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 380, 422)
    time.sleep(3)

    print('Mixed')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 1182, 620)
    time.sleep(1)

    print('Mixed')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 380, 422)
    time.sleep(3)

    print('Mixed')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 925, 620)
    time.sleep(1)

    print('Mixed')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 380, 422)
    time.sleep(3)

    print('Mixed')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 1024, 620)
    time.sleep(1)

    print('Mixed')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 380, 422)
    time.sleep(3)

    print('Mixed')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 1182, 620)
    time.sleep(1)

    print('Mixed')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 380, 422)
    time.sleep(3)

    print('Mixed')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 925, 620)
    time.sleep(1)

    print('Mixed')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 380, 422)
    time.sleep(25)

    print('Skip')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 1210, 50)
    time.sleep(10)

    print('Global')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 1, 1)
    time.sleep(10)

    print('Global')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 270, 240)
    time.sleep(15)

    print('Global')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 270, 240)
    time.sleep(10)

    print('1-8 Start')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 1005, 630)
    time.sleep(10)

    print('Start')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 1005, 630)
    time.sleep(20)

    print('Skip')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 1210, 50)
    time.sleep(15)

    print('Global')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 1, 1)
    time.sleep(7)

    print('Global')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 1, 1)
    time.sleep(7)

    print('Global')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 1058, 183)
    time.sleep(7)

    print('Global')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 1058, 183)
    time.sleep(2)

    print('Global')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 1058, 183)
    time.sleep(5)

    print('Complete')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 1165, 625)
    time.sleep(15)

    print('Swipe')
    for instance_name, _ in instance_names:
        swipe_macro(instance_name, 925, 620, 301, 527)
    time.sleep(3)

    print('Swipe')
    for instance_name, _ in instance_names:
        swipe_macro(instance_name, 1054, 620, 301, 527)
    time.sleep(3)

    print('Swipe')
    for instance_name, _ in instance_names:
        swipe_macro(instance_name, 1182, 620, 301, 527)
    time.sleep(3)

    print('Swipe')
    for instance_name, _ in instance_names:
        swipe_macro(instance_name, 925, 620, 301, 527)
    time.sleep(3)

    print('Swipe')
    for instance_name, _ in instance_names:
        swipe_macro(instance_name, 1054, 620, 301, 527)
    time.sleep(3)

    print('Swipe')
    for instance_name, _ in instance_names:
        swipe_macro(instance_name, 1182, 620, 301, 527)
    time.sleep(3)

    print('Swipe')
    for instance_name, _ in instance_names:
        swipe_macro(instance_name, 925, 620, 301, 527)
    time.sleep(3)

    print('Swipe')
    for instance_name, _ in instance_names:
        swipe_macro(instance_name, 925, 620, 301, 527)
    time.sleep(3)

    print('Swipe')
    for instance_name, _ in instance_names:
        swipe_macro(instance_name, 1054, 620, 301, 527)
    time.sleep(3)

    print('Swipe')
    for instance_name, _ in instance_names:
        swipe_macro(instance_name, 1182, 620, 301, 527)
    time.sleep(3)

    print('Swipe')
    for instance_name, _ in instance_names:
        swipe_macro(instance_name, 925, 620, 301, 527)
    time.sleep(3)

    print('Swipe')
    for instance_name, _ in instance_names:
        swipe_macro(instance_name, 1054, 620, 301, 527)
    time.sleep(3)

    print('Swipe')
    for instance_name, _ in instance_names:
        swipe_macro(instance_name, 1182, 620, 301, 527)
    time.sleep(10)

    print('Skip')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 1210, 50)
    time.sleep(20)

    print('Global')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 405, 245)
    time.sleep(10)

    print('1-9 -> Start')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 1005, 630)
    time.sleep(10)

    print('Start')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 1005, 630)
    time.sleep(35)

    print('Skip')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 1210, 50)
    time.sleep(10)

    print('Skip')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 1210, 50)
    time.sleep(20)

    print('Skip')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 1210, 50)
    time.sleep(10)

    print('Adding 5 Star Char')
    for instance_name, _ in instance_names:
        swipe_macro(instance_name, 879, 627, 870, 358)
    time.sleep(5)

    print('Complete')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 1165, 625)
    time.sleep(10)

    print('Global')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 1058, 183)
    time.sleep(10)

    print('Global')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 1058, 183)
    time.sleep(20)

    print('Global')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 1058, 183)
    time.sleep(10)

    print('Global')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 1058, 183)
    time.sleep(10)

    print('Skill Attack')
    for instance_name, _ in instance_names:
        swipe_macro(instance_name, 925, 620, 450, 550)
    time.sleep(10)

    print('Multi')
    for instance_name, _ in instance_names:
        swipe_macro(instance_name, 925, 620, 777, 250)
    time.sleep(3)

    print('Multi')
    for instance_name, _ in instance_names:
        swipe_macro(instance_name, 1054, 620, 450, 550)
    time.sleep(3)

    print('Multi')
    for instance_name, _ in instance_names:
        swipe_macro(instance_name, 1182, 620, 777, 250)
    time.sleep(3)

    print('Multi')
    for instance_name, _ in instance_names:
        swipe_macro(instance_name, 925, 620, 450, 550)
    time.sleep(3)

    print('Multi')
    for instance_name, _ in instance_names:
        swipe_macro(instance_name, 1054, 620, 777, 250)
    time.sleep(3)

    print('Multi')
    for instance_name, _ in instance_names:
        swipe_macro(instance_name, 1182, 620, 450, 550)
    time.sleep(3)

    print('Multi')
    for instance_name, _ in instance_names:
        swipe_macro(instance_name, 925, 620, 777, 250)
    time.sleep(3)

    print('Multi')
    for instance_name, _ in instance_names:
        swipe_macro(instance_name, 1054, 620, 450, 550)
    time.sleep(3)

    print('Multi')
    for instance_name, _ in instance_names:
        swipe_macro(instance_name, 1182, 620, 777, 250)
    time.sleep(3)

    print('Multi')
    for instance_name, _ in instance_names:
        swipe_macro(instance_name, 925, 620, 450, 550)
    time.sleep(3)

    print('Multi')
    for instance_name, _ in instance_names:
        swipe_macro(instance_name, 1054, 620, 777, 250)
    time.sleep(3)

    print('Multi')
    for instance_name, _ in instance_names:
        swipe_macro(instance_name, 1182, 620, 450, 550)
    time.sleep(3)

    print('Multi')
    for instance_name, _ in instance_names:
        swipe_macro(instance_name, 925, 620, 777, 250)
    time.sleep(3)

    print('Multi')
    for instance_name, _ in instance_names:
        swipe_macro(instance_name, 1054, 620, 450, 550)
    time.sleep(3)

    print('Multi')
    for instance_name, _ in instance_names:
        swipe_macro(instance_name, 1182, 620, 777, 250)
    time.sleep(3)

    print('Multi')
    for instance_name, _ in instance_names:
        swipe_macro(instance_name, 925, 620, 450, 550)
    time.sleep(3)

    print('Multi')
    for instance_name, _ in instance_names:
        swipe_macro(instance_name, 1054, 620, 777, 250)
    time.sleep(3)

    print('Multi')
    for instance_name, _ in instance_names:
        swipe_macro(instance_name, 1182, 620, 450, 550)
    time.sleep(3)

    print('Multi')
    for instance_name, _ in instance_names:
        swipe_macro(instance_name, 925, 620, 777, 250)
    time.sleep(3)

    print('Multi')
    for instance_name, _ in instance_names:
        swipe_macro(instance_name, 925, 620, 450, 550)
    time.sleep(3)

    print('Multi')
    for instance_name, _ in instance_names:
        swipe_macro(instance_name, 1054, 620, 457, 324)
    time.sleep(3)

    print('Multi')
    for instance_name, _ in instance_names:
        swipe_macro(instance_name, 1182, 620, 457, 324)
    time.sleep(3)

    print('Multi')
    for instance_name, _ in instance_names:
        swipe_macro(instance_name, 925, 620, 457, 324)
    time.sleep(3)

    print('Multi')
    for instance_name, _ in instance_names:
        swipe_macro(instance_name, 1054, 620, 457, 324)
    time.sleep(3)

    print('Multi')
    for instance_name, _ in instance_names:
        swipe_macro(instance_name, 1182, 620, 457, 324)
    time.sleep(10)

    print('Skip')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 1210, 50)
    time.sleep(10)

    print('Multi')
    for instance_name, _ in instance_names:
        swipe_macro(instance_name, 925, 620, 777, 250)
    time.sleep(3)

    print('Multi')
    for instance_name, _ in instance_names:
        swipe_macro(instance_name, 1182, 620, 450, 550)
    time.sleep(3)

    print('Multi')
    for instance_name, _ in instance_names:
        swipe_macro(instance_name, 1054, 620, 777, 250)
    time.sleep(3)

    print('Multi')
    for instance_name, _ in instance_names:
        swipe_macro(instance_name, 925, 620, 450, 550)
    time.sleep(3)

    print('Multi')
    for instance_name, _ in instance_names:
        swipe_macro(instance_name, 1054, 620, 777, 250)
    time.sleep(3)

    print('Multi')
    for instance_name, _ in instance_names:
        swipe_macro(instance_name, 1182, 620, 450, 550)
    time.sleep(3)

    print('Multi')
    for instance_name, _ in instance_names:
        swipe_macro(instance_name, 925, 620, 777, 250)
    time.sleep(3)

    print('Multi')
    for instance_name, _ in instance_names:
        swipe_macro(instance_name, 1054, 620, 450, 550)
    time.sleep(3)

    print('Multi')
    for instance_name, _ in instance_names:
        swipe_macro(instance_name, 1182, 620, 777, 250)
    time.sleep(3)

    print('Multi')
    for instance_name, _ in instance_names:
        swipe_macro(instance_name, 925, 620, 450, 550)
    time.sleep(3)

    print('Multi')
    for instance_name, _ in instance_names:
        swipe_macro(instance_name, 1054, 620, 777, 250)
    time.sleep(3)

    print('Multi')
    for instance_name, _ in instance_names:
        swipe_macro(instance_name, 1182, 620, 450, 550)
    time.sleep(3)

    print('Multi')
    for instance_name, _ in instance_names:
        swipe_macro(instance_name, 925, 620, 777, 250)
    time.sleep(3)

    print('Multi')
    for instance_name, _ in instance_names:
        swipe_macro(instance_name, 1054, 620, 450, 550)
    time.sleep(3)

    print('Multi')
    for instance_name, _ in instance_names:
        swipe_macro(instance_name, 1182, 620, 777, 250)
    time.sleep(3)

    print('Multi')
    for instance_name, _ in instance_names:
        swipe_macro(instance_name, 925, 620, 450, 550)
    time.sleep(3)

    print('Multi')
    for instance_name, _ in instance_names:
        swipe_macro(instance_name, 1054, 620, 777, 250)
    time.sleep(3)

    print('Multi')
    for instance_name, _ in instance_names:
        swipe_macro(instance_name, 1182, 620, 450, 550)
    time.sleep(3)

    print('Multi')
    for instance_name, _ in instance_names:
        swipe_macro(instance_name, 925, 620, 777, 250)
    time.sleep(3)

    print('Multi')
    for instance_name, _ in instance_names:
        swipe_macro(instance_name, 1054, 620, 450, 550)
    time.sleep(3)

    print('Multi')
    for instance_name, _ in instance_names:
        swipe_macro(instance_name, 1182, 620, 777, 250)
    time.sleep(3)

    print('Multi')
    for instance_name, _ in instance_names:
        swipe_macro(instance_name, 925, 620, 450, 550)
    time.sleep(3)

    print('Multi')
    for instance_name, _ in instance_names:
        swipe_macro(instance_name, 1054, 620, 777, 250)
    time.sleep(3)

    print('Multi')
    for instance_name, _ in instance_names:
        swipe_macro(instance_name, 1182, 620, 450, 550)
    time.sleep(3)

    print('Multi')
    for instance_name, _ in instance_names:
        swipe_macro(instance_name, 925, 620, 777, 250)
    time.sleep(3)

    print('Multi')
    for instance_name, _ in instance_names:
        swipe_macro(instance_name, 1054, 620, 450, 550)
    time.sleep(3)

    print('Multi')
    for instance_name, _ in instance_names:
        swipe_macro(instance_name, 1182, 620, 777, 250)
    time.sleep(3)

    print('Multi')
    for instance_name, _ in instance_names:
        swipe_macro(instance_name, 925, 620, 450, 550)
    time.sleep(3)

    print('Multi')
    for instance_name, _ in instance_names:
        swipe_macro(instance_name, 1054, 620, 777, 250)
    time.sleep(3)

    print('Multi')
    for instance_name, _ in instance_names:
        swipe_macro(instance_name, 1182, 620, 450, 550)
    time.sleep(3)

    print('Multi')
    for instance_name, _ in instance_names:
        swipe_macro(instance_name, 925, 620, 777, 250)
    time.sleep(3)

    print('Multi')
    for instance_name, _ in instance_names:
        swipe_macro(instance_name, 1054, 620, 450, 550)
    time.sleep(3)

    print('Multi')
    for instance_name, _ in instance_names:
        swipe_macro(instance_name, 1182, 620, 777, 250)
    time.sleep(3)

    print('Multi')
    for instance_name, _ in instance_names:
        swipe_macro(instance_name, 1054, 620, 450, 550)
    time.sleep(20)

    print('Skip')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 1210, 50)
    time.sleep(10)

    print('Skip')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 1210, 50)
    time.sleep(10)

    print('Skip')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 1210, 50)
    time.sleep(10)

    print('Global')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 435, 275)
    time.sleep(15)

    print('Global')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 435, 275)
    time.sleep(10)

    print('Global')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 435, 275)
    time.sleep(15)

    print('Global')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 435, 275)
    time.sleep(15)

    print('Global')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 435, 275)
    time.sleep(5)

    print('Click 2-1')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 1005, 630)
    time.sleep(10)

    print('Start')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 1005, 630)
    time.sleep(30)

    print('Skip')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 1210, 50)
    time.sleep(8)

    print('Skip')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 1210, 50)
    time.sleep(15)

    print('Swipe')
    for instance_name, _ in instance_names:
        swipe_macro(instance_name, 770, 624, 296, 318)
    time.sleep(10)

    print('Complete')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 1165, 625)
    time.sleep(12)

    print('Swipe')
    for instance_name, _ in instance_names:
        swipe_macro(instance_name, 925, 620, 605, 388)
    time.sleep(3)

    print('Swipe')
    for instance_name, _ in instance_names:
        swipe_macro(instance_name, 1054, 620, 605, 388)
    time.sleep(3)

    print('Swipe')
    for instance_name, _ in instance_names:
        swipe_macro(instance_name, 1182, 620, 605, 388)
    time.sleep(3)

    print('Swipe')
    for instance_name, _ in instance_names:
        swipe_macro(instance_name, 925, 620, 605, 388)
    time.sleep(3)

    print('Swipe')
    for instance_name, _ in instance_names:
        swipe_macro(instance_name, 1054, 620, 605, 388)
    time.sleep(3)

    print('Swipe')
    for instance_name, _ in instance_names:
        swipe_macro(instance_name, 1182, 620, 605, 388)
    time.sleep(3)

    print('Swipe')
    for instance_name, _ in instance_names:
        swipe_macro(instance_name, 925, 620, 605, 388)
    time.sleep(3)

    print('Swipe')
    for instance_name, _ in instance_names:
        swipe_macro(instance_name, 1054, 620, 605, 388)
    time.sleep(3)

    print('Swipe')
    for instance_name, _ in instance_names:
        swipe_macro(instance_name, 1182, 620, 605, 388)
    time.sleep(3)

    print('Swipe')
    for instance_name, _ in instance_names:
        swipe_macro(instance_name, 925, 620, 605, 388)
    time.sleep(3)

    print('Swipe')
    for instance_name, _ in instance_names:
        swipe_macro(instance_name, 1054, 620, 605, 388)
    time.sleep(3)

    print('Swipe')
    for instance_name, _ in instance_names:
        swipe_macro(instance_name, 1182, 620, 605, 388)
    time.sleep(3)

    print('Swipe')
    for instance_name, _ in instance_names:
        swipe_macro(instance_name, 925, 620, 605, 388)
    time.sleep(20)

    print('Skip')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 1210, 50)
    time.sleep(15)

    print('Global')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 1058, 183)
    time.sleep(10)

    print('Global')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 1058, 183)
    time.sleep(20)

    print('Global')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 1058, 183)
    time.sleep(10)

    print('Global')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 1058, 183)
    time.sleep(10)

    # Last Page
    print('Back')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 1, 1)
    time.sleep(20)

    print('Back')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 1, 1)
    time.sleep(5)

    print('Back')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 1, 1)
    time.sleep(5)

    print('Back')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 1, 1)
    time.sleep(5)

    print('Back')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 1, 1)
    time.sleep(10)

    print('Global')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 1, 1)
    time.sleep(5)

    print('Global')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 1, 1)
    time.sleep(5)

    print('Global')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 1, 1)
    time.sleep(5)

    print('Vassal')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 75, 655)
    time.sleep(15)

    print('Hero')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 295, 240)
    time.sleep(15)

    print('Click')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 75, 300)
    time.sleep(15)

    print('Global')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 1, 1)
    time.sleep(10)

    print('Global')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 1, 1)
    time.sleep(10)

    print('Global')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 1, 1)
    time.sleep(10)

    print('Quick Equip')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 805, 605)
    time.sleep(10)

    print('Global')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 1, 1)
    time.sleep(10)

    print('Global')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 1, 1)
    time.sleep(10)

    print('Global')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 1, 1)
    time.sleep(10)

    print('Global')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 1, 1)
    time.sleep(10)

    print('Embrace')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 400, 650)
    time.sleep(20)

    print('10x')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 1130, 650)
    time.sleep(40)

    print('Skip')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 643, 315)
    time.sleep(20)

    print('Skip')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 643, 315)
    time.sleep(20)

    print('Skip')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 643, 315)
    time.sleep(20)

    print('Skip')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 643, 315)
    time.sleep(20)

    print('Skip')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 643, 315)
    time.sleep(20)

    print('Skip')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 643, 315)
    time.sleep(20)

    print('Skip')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 643, 315)
    time.sleep(20)

    print('Skip')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 643, 315)
    time.sleep(20)

    print('Skip')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 643, 315)
    time.sleep(20)

    print('Skip')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 643, 315)
    time.sleep(20)

    print('Back')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 1, 1)
    time.sleep(5)

    print('Back')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 1, 1)
    time.sleep(5)

    print('Back')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 1, 1)
    time.sleep(5)

    print('Back')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 1, 1)
    time.sleep(5)

    print('Incase')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 1045, 170)
    time.sleep(5)

    print(f"Vassal Clicking")
    for instance_name in instance_names:
        tap_macro(instance_name, 70, 650)
    time.sleep(8)

    print(f"[{instance_name}] Taking screenshot after tap")
    for instance_name in instance_names:
        take_screenshot(instance_name, login_day=14)
    time.sleep(5)

    print(f"[{instance_name}] Closing instance")
    for instance_name in instance_names:
        os.system(f'ldconsole.exe quit --name {instance_name}')