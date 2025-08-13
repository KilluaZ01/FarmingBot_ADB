import os
import subprocess
from config import SCREENSHOT_DIR
import cv2

def clear_app_data(instance_name, package_name):
    os.system(f'ldconsole.exe adb --name {instance_name} --command "shell rm -rf {package_name}"')

def close_instance(instance_name):
    os.system(f'ldconsole.exe quit --name {instance_name}')

def close_app(instance_name):
    os.system(f'ldconsole.exe adb --name {instance_name} --command "shell am force-stop "')

def delete_instance(instance_name):
    # First, stop the instance if it's running
    os.system(f'ldconsole.exe quit --name {instance_name}')
    
    # Then, delete the instance
    os.system(f'ldconsole.exe remove --name {instance_name}')

def input_guest_name(instance_name, name):
    # Type the name
    cmd_input_name = f'ldconsole.exe adb --name {instance_name} --command "shell input text {name}"'
    os.system(cmd_input_name)
    
    # Press Enter key
    cmd_press_enter = f'ldconsole.exe adb --name {instance_name} --command "shell input tap 835 465"'
    os.system(cmd_press_enter)

def take_screenshot(instance_name):
    remote_path = "/sdcard/result.png"
    local_path = os.path.join(SCREENSHOT_DIR, f"{instance_name}.png")

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

def find_template_on_screen(screenshot_path, template_path, threshold=0.8):
    img = cv2.imread(screenshot_path)
    template = cv2.imread(template_path)

    if img is None:
        print(f"❌ Failed to read screenshot: {screenshot_path}")
        return None

    if template is None:
        print(f"❌ Failed to read template: {template_path}")
        return None

    result = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)

    if max_val >= threshold:
        center_x = max_loc[0] + template.shape[1] // 2
        center_y = max_loc[1] + template.shape[0] // 2  
        print(f"✅ Match found at X: {center_x}, Y: {center_y} (Confidence: {max_val:.2f})")
        return center_x, center_y
    else:
        print(f"❌ No match found (Confidence: {max_val:.2f})")
        return None