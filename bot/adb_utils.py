import os
import subprocess
from config import SCREENSHOT_DIR

def clear_app_data(device_id, package_name):
    os.system(f'ldconsole.exe adb --name {device_id} --command "shell rm -rf {package_name}')

def close_instance(instance_name):
    os.system(f'ldconsole.exe quit --name {instance_name}')

def input_guest_name(device_id, name):
    # Type the name
    cmd_input_name = f'ldconsole.exe adb --name {device_id} --command "shell input text helloworld101"'
    os.system(cmd_input_name)
    
    # Press Enter key
    cmd_press_enter = f'ldconsole.exe adb --name {device_id} --command "shell input keyevent 66"'
    os.system(cmd_press_enter)

def take_screenshot(instance_name, filename):
    remote_path = "/sdcard/result.png"
    local_path = os.path.join(SCREENSHOT_DIR, f"{filename}.png")

    # Step 1: Take screenshot inside emulator
    screencap_cmd = [
        "ldconsole.exe", "adb",
        "--name", instance_name,
        "--command", f"shell screencap -p {remote_path}"
    ]
    result1 = subprocess.run(screencap_cmd, capture_output=True, text=True)
    if result1.returncode != 0:
        print(f"[{instance_name}] Error during screencap: {result1.stderr}")
        return False

    # Step 2: Pull screenshot from emulator to PC
    pull_cmd = [
        "ldconsole.exe", "adb",
        "--name", instance_name,
        "--command", f"pull {remote_path} {local_path}"
    ]
    result2 = subprocess.run(pull_cmd, capture_output=True, text=True)
    if result2.returncode != 0:
        print(f"[{instance_name}] Error during pull: {result2.stderr}")
        return False

    print(f"[{instance_name}] Screenshot saved to {local_path}")
    return True