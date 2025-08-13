import multiprocessing
import time
from clone_utils import clone_instance, launch_instance
from config import CYCLE_PADDING, TOTAL_ACCOUNTS, INSTANCES_PER_BATCH
from macros import tap_macro, swipe_macro
from random import randint
from adb_utils import close_instance, input_guest_name, delete_instance
from template_matching import is_dashboard_screen
from daily_claim_runner import take_screenshot_another, detect_regular_summon
import requests
import threading
import subprocess
import os
from proxy_config import AIRPROXY
from template_matching import is_template_present, find_template_on_screen
from debug_adb import adb_debugger


download_time = 0

def generate_guest_name(index, prefix):
    result = f"{prefix}{randint(1000, 10000)}x{index}"
    print(f"[NameGen] Index={index}, Result={result}")
    return result
    
def is_process_running(process_name):
    try:
        # Use tasklist to check if the process is running
        output = subprocess.check_output(f'tasklist /FI "IMAGENAME eq {process_name}"', shell=True).decode()
        return process_name.lower() in output.lower()
    except subprocess.CalledProcessError:
        return False

def launch_with_proxifier(profile_path, instance_name):
    proxifier_path = "C:\\Program Files\\Proxifier\\Proxifier.exe"
    ldplayer_path = "C:\\LDPlayer\\LDPlayer9\\dnplayer.exe"

    if not os.path.exists(proxifier_path):
        print("❌ Proxifier not found at:", proxifier_path)
        return

    if not os.path.exists(profile_path):
        print(f"❌ Proxifier profile not found: {profile_path}")
        return
    
    if not is_process_running("Proxifier.exe"):
        print("Starting Proxifier...")
        try:
            subprocess.Popen([
                proxifier_path,
                "/profile", profile_path,
                "/silent",
                "/run", ldplayer_path,
                "--name", instance_name
            ])
            print(f"✅ Launched {instance_name} via Proxifier profile: {os.path.basename(profile_path)}")
        except Exception as e:
            print(f"❌ Failed to launch {instance_name} with Proxifier: {e}")
    else:
        print("Proxifier is already running.")
        

def prepare_batch(batch_num, instances_per_batch, base_instance, log_func):
    instance_names = []
    unique_num = randint(0, 1000)

    for i in range(instances_per_batch):
        # 1. Create a unique name for the new instance
        new_name = f"{base_instance}-{(batch_num - 1) * instances_per_batch + i + 1}-{unique_num}"
        
        # 2. Create the instance using LDPlayer CLI
        log_func(f"📦 Creating new instance: {new_name}")
        os.system(f'ldconsole add --name {new_name} --resolution 1280,720,240')

        # 3. Run adb_debugger() to enable ADB debug in its config
        log_func(f"🔧 Enabling ADB Debug for {new_name}")
        adb_debugger()

        # 4. Launch instance
        log_func(f"🚀 Launching {new_name}")
        launch_instance(new_name)

        # 5. Apply proxy if needed
        proxy_ip = AIRPROXY.get("host")
        proxy_port = AIRPROXY.get("port")
        proxy_user = AIRPROXY.get("username")
        proxy_pass = AIRPROXY.get("password")

        if proxy_ip == "127.0.0.1":
            log_func(f"[{new_name}] Skipping proxifier — using localhost")
        else:
            proxifier_profile = f"C:\\ProxifierProfiles\\profile-1.ppx"
            if os.path.exists(proxifier_profile):
                launch_with_proxifier(proxifier_profile, new_name)

        instance_names.append(new_name)

    return instance_names


def run_batch(batch_num, start_guest_index, instances_per_batch, log_func, base_instance, guest_name_prefix):
    instance_names = prepare_batch(batch_num, instances_per_batch, base_instance, log_func)
    log_func(f"🛠️ Prepared batch {batch_num} with {len(instance_names)} instances")
    time.sleep(50)  # Let them boot

    guest_data = []

    apk_dir = "C:/Users/Administrator/Desktop/silver_blood_extracted"
    # apk_dir = "C:/Users/Killua/Desktop/silver_blood"
    apk_files = [
        "com.skystone.silverblood.us.apk",
        "config.armeabi_v7a.apk",
        "install_time_pack.apk"
    ]
    apk_paths = " ".join([f"{apk_dir}/{apk}" for apk in apk_files])
    INSTALL_TIMEOUT = 200  # seconds
    MAX_RETRIES = 3

    def install_apk(instance_name):
        for attempt in range(1, MAX_RETRIES + 1):
            command = f'ldconsole.exe adb --name "{instance_name}" --command "install-multiple {apk_paths}"'
            try:
                subprocess.run(command, shell=True, timeout=INSTALL_TIMEOUT)
                print(f"[{instance_name}] APK installed successfully on attempt {attempt}.")
                return
            except subprocess.TimeoutExpired:
                print(f"[{instance_name}] APK install timed out on attempt {attempt}. Retrying...")
            except Exception as e:
                print(f"[{instance_name}] APK install failed: {e}. Retrying...")
            time.sleep(3)

        print(f"[{instance_name}] APK install failed after {MAX_RETRIES} attempts.")

    threads = []
    guest_names = []

    for i, instance_name in enumerate(instance_names):
        guest_index = start_guest_index + i
        guest_name = generate_guest_name(guest_index, guest_name_prefix)
        guest_data.append((instance_name, guest_name))
        guest_names.append(guest_name)
        log_func(f"[{instance_name}] Guest: {guest_name}")
        log_func(f"BATCH INFO - Saved")

    for instance_name, _ in guest_data:
        t = threading.Thread(target=install_apk, args=(instance_name,))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    time.sleep(5)

    for instance_name, _ in guest_data:
        os.system(f'ldconsole.exe adb --name "{instance_name}" --command "shell monkey -p com.skystone.silverblood.us -c android.intent.category.LAUNCHER 1"')
        log_func(f"[{instance_name}] - Launched Silver and Blood")
    time.sleep(100)

    log_func(f"Agreed!")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 160, 406)
    time.sleep(1)

    log_func(f"Agreed!")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 160, 460)
    time.sleep(1)

    log_func(f"Agreed!")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 160, 530)
    time.sleep(1)

    log_func(f"Terms and Condition! - Done")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 820, 600)
    time.sleep(4)

    log_func(f"Guest")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 627, 543)
    time.sleep(20)

    # log_func(f"Download")
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 605, 495)
    # time.sleep(30)

    # log_func(f"Download")
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 605, 495)
    # time.sleep(50)

    log_func(f"Background download Selected")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 370, 546)
    time.sleep(15)

    log_func(f"Settings")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1213, 232)
    time.sleep(8)

    log_func(f"Graphics")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 170, 280)
    time.sleep(5)

    log_func(f"Graphics")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 923, 204)
    time.sleep(5)

    log_func(f"Graphics")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 902, 411)
    time.sleep(5)

    log_func(f"Sound")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 170, 347)
    time.sleep(5)

    log_func(f"Sound")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 730, 272)
    time.sleep(5)

    log_func(f"Battle")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 170, 479)
    time.sleep(5)
    
    log_func(f"Battle")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 936, 424)
    time.sleep(5)

    log_func(f"Close")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1160, 103)
    time.sleep(8)

    log_func(f"Start!!")
    for instance_name, _ in guest_data: # Start
        tap_macro(instance_name, 800, 500)
    time.sleep(40)

    log_func(f"Skip")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1210, 50)
    time.sleep(7)

    log_func(f"Skip")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1210, 50)
    time.sleep(12)

    log_func(f"Skip")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1210, 50)
    time.sleep(12)

    log_func(f"Skip")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1210, 50)
    time.sleep(20)

    log_func(f"Click")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 635, 295)
    time.sleep(12)

    log_func(f"Click")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 865, 628)
    time.sleep(12)

    log_func(f"Click")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 800, 630)
    time.sleep(20)
    
    log_func(f"Swipe!")
    for instance_name, _ in guest_data:
        swipe_macro(instance_name, 925, 615, 710, 303)
    time.sleep(20)

    log_func(f"Skip")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1210, 50)
    time.sleep(15)

    log_func(f"Skip")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1210, 50)
    time.sleep(15)

    log_func(f"Skip")
    for instance_name, _ in guest_data: # First Finish
        tap_macro(instance_name, 1210, 50)
    time.sleep(20)

    log_func(f"Skip")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1210, 50)
    time.sleep(20)

    log_func(f"Swipe!")
    for instance_name, _ in guest_data:
        swipe_macro(instance_name, 320, 620, 388, 320)
    time.sleep(10)

    log_func(f"Continue")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1175, 620)
    time.sleep(30)

    log_func(f"Skip")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1210, 50)
    time.sleep(15)

    log_func(f"Click")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1060, 625)
    time.sleep(10)

    log_func(f"Click")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 795, 640)
    time.sleep(10)

    log_func(f"Click")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 795, 640)
    time.sleep(10)

    log_func(f"Click")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1060, 625)
    time.sleep(30)

    log_func(f"Swipe")
    for instance_name, _ in guest_data:
        swipe_macro(instance_name, 1060, 625, 755, 300)
    time.sleep(30)

    log_func(f"Skip")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1210, 50)
    time.sleep(90)

    log_func(f"Skip")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1210, 50)
    time.sleep(20)

    log_func(f"Click")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 560, 325)
    time.sleep(15)

    log_func(f"Click")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 560, 325)
    time.sleep(20)

    log_func(f"Skip")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1210, 50)
    time.sleep(15)

    log_func(f"Skip")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1210, 50)
    time.sleep(15)

    log_func(f"Click")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 900, 280)
    time.sleep(15)

    log_func(f"Skip")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1210, 50)
    time.sleep(25)

    log_func(f"Swipe")
    for instance_name, _ in guest_data:
        swipe_macro(instance_name, 905, 405, 695, 330)
    time.sleep(20)

    log_func(f"Skip")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1210, 50)
    time.sleep(20)

    log_func(f"Complete")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1175, 620)
    time.sleep(30)

    log_func(f"Click")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 350, 475)
    time.sleep(15)

    log_func(f"Click")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 870, 160)
    time.sleep(10)

    log_func(f"Click")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 930, 625)
    time.sleep(15)

    log_func(f"Skip")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1210, 50)
    time.sleep(30)

    log_func(f"Swipe")
    for instance_name, _ in guest_data:
        swipe_macro(instance_name, 925, 615, 340, 530)
    time.sleep(40)

    log_func(f"Attack")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 310, 430)
    time.sleep(10)

    log_func(f"1st Character")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 930, 625)
    time.sleep(20)

    log_func(f"Swipe")
    for instance_name, _ in guest_data:
        swipe_macro(instance_name, 930, 625, 300, 490)
    time.sleep(40)

    log_func(f"Skip")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1210, 50)
    time.sleep(15)

    log_func(f"0-2 Completed")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1210, 50)
        print('second finished')
    time.sleep(15)

    log_func(f"Skip")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1210, 50)
    time.sleep(10)
    
    log_func(f"Click")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 560, 325)
    time.sleep(30)

    log_func(f"Skip")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1210, 50)
    time.sleep(10)

    log_func(f"Skip")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1175, 620)
    time.sleep(15)

    log_func(f"Start - 0-3")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1000, 645)
    time.sleep(30)

    log_func(f"Skip")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1210, 50)
    time.sleep(15)

    log_func(f"Skip")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1210, 50)
    time.sleep(25)

    log_func(f"Swipe")
    for instance_name, _ in guest_data:
        swipe_macro(instance_name, 435, 635, 270, 380)
    time.sleep(25)

    log_func(f"Complete")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1175, 620)
    time.sleep(20)

    log_func(f"Skip")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1210, 50)
    time.sleep(15)

    log_func(f"Click")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 520, 300)
    time.sleep(15)

    log_func(f"Click")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 520, 300)
    time.sleep(25)

    log_func(f"Swipe")
    for instance_name, _ in guest_data:
        swipe_macro(instance_name, 920, 625, 515, 340)
    time.sleep(5)

    log_func(f"Swipe")
    for instance_name, _ in guest_data:
        swipe_macro(instance_name, 920, 625, 515, 340)
    time.sleep(5)

    log_func(f"Swipe")
    for instance_name, _ in guest_data:
        swipe_macro(instance_name, 920, 625, 515, 340)
    time.sleep(25)

    log_func(f"Skip")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1210, 50)
    time.sleep(25)

    log_func(f"Click")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 525, 420)
    time.sleep(15)

    log_func(f"Click")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 525, 420)
    time.sleep(25)

    log_func(f"Swipe")
    for instance_name, _ in guest_data:
        swipe_macro(instance_name, 920, 625, 525, 420)
    time.sleep(35)

    log_func(f"Click")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 575, 440)
    time.sleep(35)

    log_func(f"Swipe")
    for instance_name, _ in guest_data:
        swipe_macro(instance_name, 1050, 630, 575, 440)
    time.sleep(55)

    log_func(f"Skip")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1210, 50)
    time.sleep(10)

    log_func(f"Skip")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1210, 50)
    time.sleep(10)

    log_func(f"Skip")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1210, 50)
    time.sleep(10)

    log_func(f"Skip")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1210, 50)
    time.sleep(10)

    log_func(f"Skip")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1210, 50)
    time.sleep(10)

    log_func(f"Skip")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1210, 50)
    time.sleep(20)

    log_func(f"Click")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 560, 325)
    time.sleep(10)

    log_func(f"Click")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 560, 325)
    time.sleep(20)

    log_func(f"Click")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 560, 325)
    time.sleep(20)

    log_func(f"Click")
    for instance_name, _ in guest_data: 
        tap_macro(instance_name, 920, 625)
    time.sleep(15)

    log_func(f"Click")
    for instance_name, _ in guest_data: 
        tap_macro(instance_name, 920, 625)
    time.sleep(20)

    log_func(f"Click")
    for instance_name, _ in guest_data: 
        tap_macro(instance_name, 920, 625)
    time.sleep(20)

    log_func(f"Click")
    for instance_name, _ in guest_data: # Third Page Finish
        tap_macro(instance_name, 920, 625)
    time.sleep(20)

    log_func(f"Skip")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1210, 50)
    time.sleep(15)

    log_func(f"Skip")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1210, 50)
    time.sleep(20)

    log_func(f"Click")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 920, 625)
    time.sleep(10)

    log_func(f"Click")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 920, 625)
    time.sleep(10)

    log_func(f"Enter Name")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 565, 420)
    time.sleep(10)

    log_func(f"Click")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 800, 410)
    time.sleep(15)

    log_func(f"Click")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 825, 605)
    time.sleep(15)

    log_func(f"Click")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 565, 420)
    time.sleep(10)

    # Name Logic
    for instance_name, guest_name in guest_data:
        input_guest_name(instance_name, guest_name)
        log_func(f"[{instance_name}] Input guest name: {guest_name}")
    time.sleep(20)

    log_func(f"Click")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 810, 600)
    time.sleep(10)

    log_func(f"Click")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 920, 625)
    time.sleep(10)

    log_func(f"Click")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 920, 625)
    time.sleep(15)

    log_func(f"Click")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 560, 325)
    time.sleep(15)

    log_func(f"Click")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 920, 625)
    time.sleep(10)

    log_func(f"Click")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 920, 625)
    time.sleep(10)

    log_func(f"Click")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 920, 625)
    time.sleep(10)

    log_func(f"Click")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 410, 645)
    time.sleep(15)

    log_func(f"Skip")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1210, 50)
    time.sleep(10)

    log_func(f"Click")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 805, 640)
    time.sleep(10)

    log_func(f"Skip")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1210, 50)
    time.sleep(10)

    log_func(f"Skip")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1210, 50)
    time.sleep(10)

    log_func(f"Back")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 480, 630)
    time.sleep(10)

    log_func(f"Click")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 120, 45)
    time.sleep(15)

    log_func(f"Click")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 920, 625)
    time.sleep(10)

    log_func(f"Click")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 920, 625)
    time.sleep(10)

    log_func(f"Click")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 920, 625)
    time.sleep(10)

    log_func(f"Click")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 920, 625)
    time.sleep(10)

    log_func(f"Click")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 920, 625)
    time.sleep(10)

    log_func(f"Click")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 920, 625)
    time.sleep(10)

    log_func(f"Click")
    for instance_name, _ in guest_data: # Forth Page Finish
        tap_macro(instance_name, 920, 625)
    time.sleep(10)

    log_func(f"Click")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 920, 625)
    time.sleep(10)

    log_func(f"Click")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 920, 625)
    time.sleep(15)

    log_func(f"Click")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1175, 620)
    time.sleep(15)

    log_func(f"Click")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 920, 625)
    time.sleep(10)

    log_func(f"Click")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1175, 620)
    time.sleep(15)

    log_func(f"Click")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1010, 626)
    time.sleep(35)

    log_func(f"Skip")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1210, 50)
    time.sleep(10)

    log_func(f"Skip")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1210, 50)
    time.sleep(10)

    log_func(f"Skip")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1210, 50)
    time.sleep(20)

    log_func(f"Skip")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1210, 50)
    time.sleep(15)

    log_func(f"Click")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 265, 535)
    time.sleep(10)

    log_func(f"Click")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 265, 535)
    time.sleep(10)

    log_func(f"Click")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 300, 620)
    time.sleep(10)

    log_func(f"Click")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 392, 590)
    time.sleep(10)

    log_func(f"Click")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 392, 590)
    time.sleep(10)

    log_func(f"Click")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 392, 590)
    time.sleep(10)

    log_func(f"Click")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 392, 590)
    time.sleep(10)

    log_func(f"Click")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 392, 590)
    time.sleep(15)

    log_func(f"Swipe")
    for instance_name, _ in guest_data:
        swipe_macro(instance_name, 430, 630, 245, 355)
    time.sleep(20)

    log_func(f"Complete")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1175, 620)
    time.sleep(15)

    log_func(f"Skip")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1210, 50)
    time.sleep(15)

    log_func(f"Click")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 785, 630)
    time.sleep(20)

    log_func(f"Swipe")
    for instance_name, _ in guest_data:
        swipe_macro(instance_name, 920, 620, 785, 285)
    time.sleep(20)

    log_func(f"Click")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 747, 588)
    time.sleep(10)

    log_func(f"Click")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 747, 588)
    time.sleep(10)

    log_func(f"Click")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 747, 588)
    time.sleep(15)

    log_func(f"Swipe")
    for instance_name, _ in guest_data:
        swipe_macro(instance_name, 1050, 625, 660, 350)
    time.sleep(25)

    log_func(f"Swipe")
    for instance_name, _ in guest_data:
        swipe_macro(instance_name, 1180, 620, 855, 215)
    time.sleep(50)

    log_func(f"Skip")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1210, 50)
    time.sleep(10)

    log_func(f"Skip")
    for instance_name, _ in guest_data: # Fifth Page Fisnihed
        tap_macro(instance_name, 1210, 50)
    time.sleep(15)

    log_func(f"Click")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 560, 325)
    time.sleep(10)

    log_func(f"Skip")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1210, 50)
    time.sleep(20)

    log_func(f"Skip")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1175, 620)
    time.sleep(10)

    log_func(f"Skip")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1005, 625)
    time.sleep(20)

    log_func(f"Skip")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1210, 50)
    time.sleep(15)

    log_func(f"Skip")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1160, 50)
    time.sleep(10)

    log_func(f"Skip")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1160, 50)
    time.sleep(10)

    log_func(f"Skip")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1160, 50)
    time.sleep(10)

    log_func(f"Complete")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1175, 620)
    time.sleep(50)

    log_func(f"Skip")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1210, 50)
    time.sleep(15)

    log_func(f"Click")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 560, 325)
    time.sleep(30)

    log_func(f"Click")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 920, 625)
    time.sleep(10)

    log_func(f"Click")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 920, 625)
    time.sleep(10)

    log_func(f"Click")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 920, 625)
    time.sleep(10)

    log_func(f"Click")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 920, 625)
    time.sleep(10)

    log_func(f"Click")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 820, 350)
    time.sleep(15)

    log_func(f"Click")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 820, 350)
    time.sleep(15)

    log_func(f"Click")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 820, 350)
    time.sleep(15)

    log_func(f"Click")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 820, 350)
    time.sleep(15)

    log_func(f"Click")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 820, 350)
    time.sleep(15)

    log_func(f"Complete")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1175, 620)
    time.sleep(10)

    log_func(f"Click")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1010, 635)
    time.sleep(15)

    log_func(f"Skip")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1210, 50)
    time.sleep(15)

    log_func(f"Skip")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1210, 50)
    time.sleep(15)

    log_func(f"Complete")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1175, 620)
    time.sleep(65)

    log_func(f"Skip")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1210, 50)
    time.sleep(15)

    log_func(f"Click")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 560, 325)
    time.sleep(15)

    log_func(f"Click")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 560, 325) # Click
    time.sleep(30)

    log_func(f"Complete")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1175, 620) # Complete
    time.sleep(10)

    log_func(f"Click")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1010, 635)
    time.sleep(20)

    log_func(f"Skip")
    for instance_name, _ in guest_data: # Sixth Page Finish SKIP
        tap_macro(instance_name, 1210, 50)
    time.sleep(10)

    log_func(f"Skip")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1210, 50)
    time.sleep(20)

    log_func(f"Click")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 965, 230)
    time.sleep(10)

    log_func(f"Complete")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1175, 620)
    time.sleep(20)

    log_func(f"Click")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 475, 275)
    time.sleep(10)

    log_func(f"Click")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 475, 275)
    time.sleep(20)

    log_func(f"Swipe")
    for instance_name, _ in guest_data:
        swipe_macro(instance_name, 480, 305, 470, 397)
    time.sleep(15)

    log_func(f"Complete")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1175, 620)
    time.sleep(60)

    log_func(f"Click")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 560, 325)
    time.sleep(15)

    log_func(f"Click")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 560, 325)
    time.sleep(10)

    log_func(f"Click")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 560, 325)
    time.sleep(10)

    log_func(f"Click")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 560, 325)
    time.sleep(10)

    log_func(f"Click")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 560, 325)
    time.sleep(15)

    log_func(f"Click")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 560, 325)
    time.sleep(15)

    log_func(f"Click")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 270, 40)
    time.sleep(20)

    log_func(f"Click")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 395, 650)
    time.sleep(30)

    log_func(f"Complete")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1175, 620)
    time.sleep(30)

    log_func(f"Skip")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1210, 50)
    time.sleep(15)

    log_func(f"Skip")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1210, 50)
    time.sleep(15)

    log_func(f"Skip")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1210, 50)
    time.sleep(15)

    log_func(f"Skip")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1210, 50)
    time.sleep(15)

    log_func(f"Skip")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1210, 50)
    time.sleep(15)

    log_func(f"Skip")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1210, 50)
    time.sleep(15)

    log_func(f"Skip")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1210, 50)
    time.sleep(15)

    log_func(f"Skip")
    for instance_name, _ in guest_data: # Seventh Finished Page
        tap_macro(instance_name, 1210, 50)
    time.sleep(7)

    log_func(f"Click")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 470, 629)
    time.sleep(10)

    log_func(f"Home")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 265, 37)
    time.sleep(10)

    log_func(f"Click")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 160, 585)
    time.sleep(10)

    log_func(f"Click")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 900, 100)
    time.sleep(10)

    log_func(f"Click") #Done
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 900, 100)
    time.sleep(10)

    log_func(f"Click") #Done
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 900, 100)
    time.sleep(10)

    log_func(f"Click") #Done
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1100, 660)
    time.sleep(10)

    log_func(f"Click") #Done
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 900, 100)
    time.sleep(10)

    log_func(f"Click") #Done
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1135, 210)
    time.sleep(10)

    log_func(f"Click") #Done
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1135, 210)
    time.sleep(7)

    log_func(f"Click") #Done
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1135, 210)
    time.sleep(7)

    log_func(f"Click")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1135, 210)
    time.sleep(7)

    log_func(f"Click")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1135, 210)
    time.sleep(7)

    log_func(f"Click")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1135, 210)
    time.sleep(8)

    log_func(f"Click")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 265, 37)
    time.sleep(8)

    log_func(f"Click")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 265, 37)
    time.sleep(10)

    log_func(f"Click")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 70, 650)
    time.sleep(10)

    log_func(f"Click")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 285, 260)
    time.sleep(10)

    log_func(f"Click")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1100, 313)
    time.sleep(10)

    log_func(f"Click")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1073, 648)
    time.sleep(10)

    log_func(f"Click")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 631, 625)
    time.sleep(10)

    log_func(f"Click Upgrade")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1073, 648)
    time.sleep(10)

    log_func(f"Click Home")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 265, 37)
    time.sleep(10)

    log_func(f"Click")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 265, 37)
    time.sleep(7)

    log_func(f"Click")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 265, 37)
    time.sleep(8)

    log_func(f"Click")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 265, 37)
    time.sleep(8)

    log_func(f"Lost Courtyard")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1200, 475)
    time.sleep(8)

    log_func(f"Lost Courtyard")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1200, 475)
    time.sleep(7)

    log_func(f"Lost Courtyard")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1200, 475)
    time.sleep(7)

    log_func(f"Lost Courtyard")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1200, 475)
    time.sleep(7)

    log_func(f"Lost Courtyard")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1200, 475)
    time.sleep(10)

    log_func(f"Lost Courtyard")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1200, 475)
    time.sleep(7)

    log_func(f"Lost Courtyard")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1200, 475)
    time.sleep(7)

    log_func(f"Lost Courtyard")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1200, 475)
    time.sleep(10)

    log_func(f"Click Timeworn")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1100, 150)
    time.sleep(10)

    log_func(f"Click Timeworn")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1100, 150)
    time.sleep(10)

    log_func(f"Click Timeworn")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1100, 150)
    time.sleep(10)

    log_func(f"Click Timeworn")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1100, 150)
    time.sleep(10)

    log_func(f"Click Timeworn")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1100, 150)
    time.sleep(7)

    log_func(f"Click Timeworn")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1100, 150)
    time.sleep(7)

    log_func(f"Click Timeworn")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1100, 150)
    time.sleep(7)

    log_func(f"Click Timeworn")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1100, 150)
    time.sleep(7)

    log_func(f"Click Timeworn")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1100, 150)
    time.sleep(7)

    log_func(f"Click Timeworn")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1100, 150)
    time.sleep(10)

    log_func(f"Click New")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 331, 371)
    time.sleep(10)

    log_func(f"Click New")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 331, 371)
    time.sleep(10)

    log_func(f"Click New")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 331, 371)
    time.sleep(10)

    log_func(f"Click New")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 331, 371)
    time.sleep(8)

    log_func(f"Click New")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 331, 371)
    time.sleep(7)

    log_func(f"Click New")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 331, 371)
    time.sleep(8)

    log_func(f"Click New")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 331, 371)
    time.sleep(10)

    log_func(f"Close Game") # New Start
    for instance_name, _ in guest_data:
        os.system(f'ldconsole.exe adb --name "{instance_name}" --command "shell am force-stop com.skystone.silverblood.us"')
    time.sleep(10)

    log_func("Open Game")
    for instance_name, _ in guest_data:
        os.system(f'ldconsole.exe adb --name "{instance_name}" --command "shell monkey -p com.skystone.silverblood.us -c android.intent.category.LAUNCHER 1"')
        log_func(f"[{instance_name}] - Launched Silver and Blood")
    time.sleep(150)

    log_func("Start")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 800, 500)
    time.sleep(20)

    log_func(f"Close Notice")   
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1171, 104)
    time.sleep(10)

    log_func(f"New Event")   
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1171, 104)
    time.sleep(10)

    log_func(f"New Event")   
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1171, 104)
    time.sleep(10)

    log_func(f"Continue 7x")   
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1171, 104)
    time.sleep(10)

    log_func(f"Close 7x")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1171, 104)
    time.sleep(10)

    log_func(f"Continue 14x")   
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1171, 104)
    time.sleep(10)

    log_func(f"Back")   
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1, 1)
    time.sleep(5)

    log_func(f"Back")   
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1, 1)
    time.sleep(5)
    
    # Start From here After all
    print(f"Open Event")   
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1104, 114)
    time.sleep(10)

    print(f"10x Scroll Click")   
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 440, 278)
    time.sleep(5)

    print(f"10x Scroll Click")   
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 440, 278)
    time.sleep(8)

    print('Incase')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1, 1)
    time.sleep(5)

    log_func(f"Back")   
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1, 1)
    time.sleep(5)

    print('Embrace')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 400, 650)
    time.sleep(20)

    print('10x')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1130, 650)
    time.sleep(40)

    print('Skip')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 643, 315)
    time.sleep(20)

    print('Skip')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 643, 315)
    time.sleep(20)

    print('Skip')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 643, 315)
    time.sleep(20)

    print('Skip')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 643, 315)
    time.sleep(20)

    print('Skip')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 643, 315)
    time.sleep(20)

    print('Skip')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 643, 315)
    time.sleep(20)

    print('Skip')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 643, 315)
    time.sleep(20)

    print('Skip')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 643, 315)
    time.sleep(20)

    print('Skip')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 643, 315)
    time.sleep(18)

    print('Skip')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 643, 315)
    time.sleep(18)

    log_func('Back')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 470, 630)
    time.sleep(10)

    print('Back')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1, 1)
    time.sleep(5)

    print('Back')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1, 1)
    time.sleep(15)

    for instance_name, _ in guest_data:
        log_func(f"Vassal Clicking")
        tap_macro(instance_name, 70, 650)
    time.sleep(8)

    print('Hero')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 285, 255)
    time.sleep(10)

    print('Tap')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 70, 415)
    time.sleep(10)

    print('Global')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1, 1)
    time.sleep(8)

    print('Global')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1, 1)
    time.sleep(8)

    print('Global')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1, 1)
    time.sleep(8)

    print('Global')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1, 1)
    time.sleep(8)

    print('Global')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1, 1)
    time.sleep(8)

    print('Back')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1, 1)
    time.sleep(8)

    print('Back')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1, 1)
    time.sleep(8)

    print('Back')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1, 1)
    time.sleep(8)

    for instance_name, _ in guest_data:
        log_func(f"Vassal Clicking")
        tap_macro(instance_name, 70, 650)
    time.sleep(8)

    for instance_name, _ in guest_data:
        log_func(f"[{instance_name}] Taking screenshot of Heros")
        take_screenshot_another(instance_name, login_day=1)
    time.sleep(5)

    print('Back')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1, 1)
    time.sleep(3)

    print('Back')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1, 1)
    time.sleep(3)

    # For Entering Chapter
    print('Thread of Fate')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1135, 630)
    time.sleep(15)

    print('Thread of Fate')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1135, 630)
    time.sleep(10)

    print('Start')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1005, 630)
    time.sleep(25)

    print('Skip')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1210, 50)
    time.sleep(15)

    print('Skip')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1210, 50)
    time.sleep(10)

    print('Global')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1058, 183)
    time.sleep(10)

    print('Complete')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1165, 625)
    time.sleep(10)

    print('Continue')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 455, 500)
    time.sleep(10)

    print('Global')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1058, 183)
    time.sleep(10)

    print('Global')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1058, 183)
    time.sleep(40)

    print('Global')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1058, 183)
    time.sleep(10)

    print('Vassal')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 482, 615)
    time.sleep(15)

    print('Hero')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 285, 255)
    time.sleep(10)

    print('Add')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1100, 315)
    time.sleep(10)

    print('Max')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1195, 540)
    time.sleep(10)

    print('Upgrade')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1075, 650)
    time.sleep(10)

    print('Back')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 55, 40)
    time.sleep(10)

    print('Back')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 55, 40)
    time.sleep(10)

    print('Hero')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 285, 255)
    time.sleep(10)

    print('Tap')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 70, 415)
    time.sleep(10)

    print('Global')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1, 1)
    time.sleep(8)

    print('Global')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1, 1)
    time.sleep(8)

    print('Global')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1, 1)
    time.sleep(8)

    print('Global')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1, 1)
    time.sleep(8)

    print('Global')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1, 1)
    time.sleep(8)

    print('Back')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 55, 40)
    time.sleep(8)

    print('Back')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 55, 40)
    time.sleep(8)

    print('Threads')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1135, 630)
    time.sleep(10)

    print('Threads')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1135, 630)
    time.sleep(10)

    print('Start')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1005, 630)
    time.sleep(20)

    print('Skip')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1210, 50)
    time.sleep(10)

    print('Skip')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1210, 50)
    time.sleep(8)

    print('Global')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1058, 183)
    time.sleep(8)

    print('Swipe')
    for instance_name, _ in guest_data:
        swipe_macro(instance_name, 655, 630, 480, 315)
    time.sleep(3)

    print('Swipe')
    for instance_name, _ in guest_data:
        swipe_macro(instance_name, 655, 630, 350, 405)
    time.sleep(3)

    print('Complete')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1165, 625)
    time.sleep(10)

    print('Global')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1058, 183)
    time.sleep(5)

    print('Global')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1058, 183)
    time.sleep(35)

    print('Continue -> 1-5 Completed')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1058, 183)
    time.sleep(20)      # 1-5 Completed

    print('Global')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1058, 183)
    time.sleep(10)

    print('1-6 Click')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1005, 630)
    time.sleep(10)

    print('Start')  
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1005, 630)
    time.sleep(20)

    print('Skip')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1210, 50)
    time.sleep(15)

    print('Global')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1058, 183)
    time.sleep(10)

    print('Global')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1058, 183)
    time.sleep(10)

    print('Global')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1058, 183)
    time.sleep(10)

    print('Complete')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1165, 625)
    time.sleep(20)

    print('Mixed')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 925, 620)
    time.sleep(1)

    print('Mixed')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 380, 422)
    time.sleep(3)

    print('Mixed')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 925, 620)
    time.sleep(1)

    print('Mixed')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 380, 422)
    time.sleep(3)

    print('Mixed')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 925, 620)
    time.sleep(1)

    print('Mixed')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 380, 422)
    time.sleep(3)

    print('Mixed')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 925, 620)
    time.sleep(1)

    print('Mixed')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 380, 422)
    time.sleep(30)

    print('Skip')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1210, 50)
    time.sleep(10)

    print('Global')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1, 1)
    time.sleep(10)

    print('Skip')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1210, 50)
    time.sleep(20)

    print('Skip')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1210, 50)
    time.sleep(10)

    print('Global')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1, 1)
    time.sleep(10)

    print('Global')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1, 1)
    time.sleep(10)

    print('Sword')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 815, 175)
    time.sleep(10)

    print('Start')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1005, 630)
    time.sleep(20)

    # Sword
    print('Complete')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1165, 625)
    time.sleep(35)

    print('Global')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1189, 650)
    time.sleep(15)

    print('Start')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1005, 630)
    time.sleep(10)

    print('Start')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1005, 630)
    time.sleep(20)

    print('Skip')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1210, 50)
    time.sleep(10)

    # 1-7
    print('Complete')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1165, 625)
    time.sleep(10)

    print('Mixed')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 925, 620)
    time.sleep(1)

    print('Mixed')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 380, 422)
    time.sleep(3)

    print('Mixed')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 925, 620)
    time.sleep(1)

    print('Mixed')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 380, 422)
    time.sleep(3)

    print('Mixed')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 925, 620)
    time.sleep(1)

    print('Mixed')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 380, 422)
    time.sleep(3)

    print('Mixed')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1024, 620)
    time.sleep(1)

    print('Mixed')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 380, 422)
    time.sleep(3)

    print('Mixed')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1182, 620)
    time.sleep(1)

    print('Mixed')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 380, 422)
    time.sleep(3)

    print('Mixed')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 925, 620)
    time.sleep(1)

    print('Mixed')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 380, 422)
    time.sleep(3)

    print('Mixed')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1024, 620)
    time.sleep(1)

    print('Mixed')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 380, 422)
    time.sleep(3)

    print('Mixed')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1182, 620)
    time.sleep(1)

    print('Mixed')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 380, 422)
    time.sleep(3)

    print('Mixed')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 925, 620)
    time.sleep(1)

    print('Mixed')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 380, 422)
    time.sleep(3)

    print('Mixed')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1024, 620)
    time.sleep(1)

    print('Mixed')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 380, 422)
    time.sleep(3)

    print('Mixed')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1182, 620)
    time.sleep(1)

    print('Mixed')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 380, 422)
    time.sleep(3)

    print('Mixed')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 925, 620)
    time.sleep(1)

    print('Mixed')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 380, 422)
    time.sleep(25)

    print('Skip')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1210, 50)
    time.sleep(10)

    print('Skip')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1170, 105)
    time.sleep(2)

    print('Global')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1, 1)
    time.sleep(10)

    print('Global')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 270, 240)
    time.sleep(15)

    print('Global')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 270, 240)
    time.sleep(10)

    print('1-8 Start')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1005, 630)
    time.sleep(10)

    print('Start')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1005, 630)
    time.sleep(20)

    print('Skip')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1210, 50)
    time.sleep(15)

    print('Global')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1, 1)
    time.sleep(7)

    print('Global')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1, 1)
    time.sleep(7)

    print('Global')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1058, 183)
    time.sleep(7)

    print('Global')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1058, 183)
    time.sleep(2)

    print('Global')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1058, 183)
    time.sleep(5)

    print('Complete')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1165, 625)
    time.sleep(15)

    print('Swipe')
    for instance_name, _ in guest_data:
        swipe_macro(instance_name, 925, 620, 301, 527)
    time.sleep(3)

    print('Swipe')
    for instance_name, _ in guest_data:
        swipe_macro(instance_name, 1054, 620, 301, 527)
    time.sleep(3)

    print('Swipe')
    for instance_name, _ in guest_data:
        swipe_macro(instance_name, 1182, 620, 301, 527)
    time.sleep(3)

    print('Swipe')
    for instance_name, _ in guest_data:
        swipe_macro(instance_name, 925, 620, 301, 527)
    time.sleep(3)

    print('Swipe')
    for instance_name, _ in guest_data:
        swipe_macro(instance_name, 1054, 620, 301, 527)
    time.sleep(3)

    print('Swipe')
    for instance_name, _ in guest_data:
        swipe_macro(instance_name, 1182, 620, 301, 527)
    time.sleep(3)

    print('Swipe')
    for instance_name, _ in guest_data:
        swipe_macro(instance_name, 925, 620, 301, 527)
    time.sleep(3)

    print('Swipe')
    for instance_name, _ in guest_data:
        swipe_macro(instance_name, 925, 620, 301, 527)
    time.sleep(3)

    print('Swipe')
    for instance_name, _ in guest_data:
        swipe_macro(instance_name, 1054, 620, 301, 527)
    time.sleep(3)

    print('Swipe')
    for instance_name, _ in guest_data:
        swipe_macro(instance_name, 1182, 620, 301, 527)
    time.sleep(3)

    print('Swipe')
    for instance_name, _ in guest_data:
        swipe_macro(instance_name, 925, 620, 301, 527)
    time.sleep(3)

    print('Swipe')
    for instance_name, _ in guest_data:
        swipe_macro(instance_name, 1054, 620, 301, 527)
    time.sleep(3)

    print('Swipe')
    for instance_name, _ in guest_data:
        swipe_macro(instance_name, 1182, 620, 301, 527)
    time.sleep(3)

    print('Swipe')
    for instance_name, _ in guest_data:
        swipe_macro(instance_name, 925, 620, 301, 527)
    time.sleep(3)

    print('Swipe')
    for instance_name, _ in guest_data:
        swipe_macro(instance_name, 1054, 620, 301, 527)
    time.sleep(3)

    print('Swipe')
    for instance_name, _ in guest_data:
        swipe_macro(instance_name, 1182, 620, 301, 527)
    time.sleep(3)

    print('Swipe')
    for instance_name, _ in guest_data:
        swipe_macro(instance_name, 925, 620, 301, 527)
    time.sleep(3)

    print('Swipe')
    for instance_name, _ in guest_data:
        swipe_macro(instance_name, 1054, 620, 301, 527)
    time.sleep(3)

    print('Swipe')
    for instance_name, _ in guest_data:
        swipe_macro(instance_name, 1182, 620, 301, 527)
    time.sleep(10)

    print('Skip')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1210, 50)
    time.sleep(5)

    print('Skip')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1170, 105)
    time.sleep(15)

    print('Incase')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1045, 170)
    time.sleep(5)

    print('Global')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 405, 245)
    time.sleep(10)

    print('1-9 -> Start')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1005, 630)
    time.sleep(10)

    print('Start')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1005, 630)
    time.sleep(35)

    print('Skip')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1210, 50)
    time.sleep(10)

    print('Skip')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1210, 50)
    time.sleep(20)

    print('Skip')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1210, 50)
    time.sleep(10)

    print('Adding 5 Star Char')
    for instance_name, _ in guest_data:
        swipe_macro(instance_name, 879, 627, 870, 358)
    time.sleep(5)

    print('Removing Healer')
    for instance_name, _ in guest_data:
        swipe_macro(instance_name, 960, 364, 943, 640)
    time.sleep(5)

    for instance_name, _ in guest_data:
        tank_path = "D:/Silver_Blood_Bot/templates/tank.png"
        log_func(f"[{instance_name}] Taking screenshot for {guest_name}")
        new_screenshot_path = take_screenshot_another(instance_name)

        match_coords = find_template_on_screen(new_screenshot_path, tank_path)
        if match_coords:
            x1, y1 = match_coords
            print('Swiping Tank')
            swipe_macro(instance_name, x1, y1, 685, 440)
        else:
            print('Tank Not Found')

    print('Complete')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1165, 625)
    time.sleep(5)

    print('Complete')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 420, 500)
    time.sleep(10)

    print('Global')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1058, 183)
    time.sleep(10)

    print('Global')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1058, 183)
    time.sleep(20)

    print('Global')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1058, 183)
    time.sleep(10)

    print('Global')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1058, 183)
    time.sleep(10)

    print('Skill Attack')
    for instance_name, _ in guest_data:
        swipe_macro(instance_name, 925, 620, 450, 550)
    time.sleep(10)

    print('Multi')
    for instance_name, _ in guest_data:
        swipe_macro(instance_name, 1054, 620, 777, 250)
    time.sleep(3)

    print('Multi')
    for instance_name, _ in guest_data:
        swipe_macro(instance_name, 1182, 620, 777, 250)
    time.sleep(3)

    print('Multi')
    for instance_name, _ in guest_data:
        swipe_macro(instance_name, 1182, 620, 777, 250)
    time.sleep(3)

    print('Multi')
    for instance_name, _ in guest_data:
        swipe_macro(instance_name, 1054, 620, 450, 550)
    time.sleep(3)

    print('Multi')
    for instance_name, _ in guest_data:
        swipe_macro(instance_name, 925, 620, 450, 550)
    time.sleep(3)

    print('Multi')
    for instance_name, _ in guest_data:
        swipe_macro(instance_name, 925, 620, 450, 550)
    time.sleep(3)

    print('Multi')
    for instance_name, _ in guest_data:
        swipe_macro(instance_name, 1182, 620, 777, 250)
    time.sleep(3)

    print('Multi')
    for instance_name, _ in guest_data:
        swipe_macro(instance_name, 925, 620, 777, 250)
    time.sleep(3)

    print('Multi')
    for instance_name, _ in guest_data:
        swipe_macro(instance_name, 925, 620, 777, 250)
    time.sleep(5)

    print('Multi')
    for instance_name, _ in guest_data:
        swipe_macro(instance_name, 1054, 620, 450, 550)
    time.sleep(3)

    print('Multi')
    for instance_name, _ in guest_data:
        swipe_macro(instance_name, 925, 620, 450, 550)
    time.sleep(3)

    print('Multi')
    for instance_name, _ in guest_data:
        swipe_macro(instance_name, 925, 620, 450, 550)
    time.sleep(3)

    print('Multi')
    for instance_name, _ in guest_data:
        swipe_macro(instance_name, 1182, 620, 777, 250)
    time.sleep(3)

    print('Multi')
    for instance_name, _ in guest_data:
        swipe_macro(instance_name, 925, 620, 777, 250)
    time.sleep(3)

    print('Multi')
    for instance_name, _ in guest_data:
        swipe_macro(instance_name, 925, 620, 777, 250)
    time.sleep(3)

    print('Multi')
    for instance_name, _ in guest_data:
        swipe_macro(instance_name, 1054, 620, 450, 550)
    time.sleep(3)

    print('Multi')
    for instance_name, _ in guest_data:
        swipe_macro(instance_name, 1182, 620, 777, 250)
    time.sleep(3)

    print('Multi')
    for instance_name, _ in guest_data:
        swipe_macro(instance_name, 925, 620, 457, 324)
    time.sleep(3)

    print('Multi')
    for instance_name, _ in guest_data:
        swipe_macro(instance_name, 1054, 620, 457, 324)
    time.sleep(3)

    print('Multi')
    for instance_name, _ in guest_data:
        swipe_macro(instance_name, 1182, 620, 457, 324)
    time.sleep(3)

    print('Multi')
    for instance_name, _ in guest_data:
        swipe_macro(instance_name, 925, 620, 457, 324)
    time.sleep(3)

    print('Multi')
    for instance_name, _ in guest_data:
        swipe_macro(instance_name, 1054, 620, 457, 324)
    time.sleep(3)

    print('Multi')
    for instance_name, _ in guest_data:
        swipe_macro(instance_name, 1182, 620, 457, 324)
    time.sleep(3)

    print('Skip')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1210, 50)
    time.sleep(3)

    print('Resume')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 770, 585)
    time.sleep(7)

    print('Multi')
    for instance_name, _ in guest_data:
        swipe_macro(instance_name, 925, 620, 450, 550)
    time.sleep(3)

    print('Multi')
    for instance_name, _ in guest_data:
        swipe_macro(instance_name, 1054, 620, 777, 250)
    time.sleep(3)

    print('Multi') # Auxa
    for instance_name, _ in guest_data:
        swipe_macro(instance_name, 925, 620, 777, 250)
    time.sleep(3)

    print('Multi')
    for instance_name, _ in guest_data:
        swipe_macro(instance_name, 925, 620, 777, 250)
    time.sleep(3)

    print('Multi')
    for instance_name, _ in guest_data:
        swipe_macro(instance_name, 1182, 620, 450, 550)
    time.sleep(3)

    print('Multi')
    for instance_name, _ in guest_data:
        swipe_macro(instance_name, 925, 620, 450, 550)
    time.sleep(3)

    print('Multi')
    for instance_name, _ in guest_data:
        swipe_macro(instance_name, 925, 620, 450, 550)
    time.sleep(3)

    print('Multi')
    for instance_name, _ in guest_data:
        swipe_macro(instance_name, 1054, 620, 777, 250)
    time.sleep(3)

    print('Multi')
    for instance_name, _ in guest_data:
        swipe_macro(instance_name, 925, 620, 777, 250)
    time.sleep(3)

    print('Multi')
    for instance_name, _ in guest_data:
        swipe_macro(instance_name, 925, 620, 777, 250)
    time.sleep(5)

    print('Multi')
    for instance_name, _ in guest_data:
        swipe_macro(instance_name, 1182, 620, 450, 550)
    time.sleep(3)

    print('Multi')
    for instance_name, _ in guest_data:
        swipe_macro(instance_name, 925, 620, 450, 550)
    time.sleep(3)

    print('Multi')
    for instance_name, _ in guest_data:
        swipe_macro(instance_name, 925, 620, 450, 550)
    time.sleep(3)

    print('Multi')
    for instance_name, _ in guest_data:
        swipe_macro(instance_name, 1054, 620, 777, 250)
    time.sleep(3)

    print('Multi')
    for instance_name, _ in guest_data:
        swipe_macro(instance_name, 925, 620, 450, 550)
    time.sleep(3)

    print('Multi')
    for instance_name, _ in guest_data:
        swipe_macro(instance_name, 925, 620, 450, 550)
    time.sleep(3)

    print('Multi')
    for instance_name, _ in guest_data:
        swipe_macro(instance_name, 1054, 620, 457, 324)
    time.sleep(3)

    print('Multi')
    for instance_name, _ in guest_data:
        swipe_macro(instance_name, 1182, 620, 457, 300)
    time.sleep(3)

    print('Multi')
    for instance_name, _ in guest_data:
        swipe_macro(instance_name, 1054, 620, 457, 324)
    time.sleep(3)

    print('Multi')
    for instance_name, _ in guest_data:
        swipe_macro(instance_name, 1182, 620, 457, 300)
    time.sleep(3)

    print('Multi')
    for instance_name, _ in guest_data:
        swipe_macro(instance_name, 1182, 620, 457, 324)
    time.sleep(8)

    print('Multi')
    for instance_name, _ in guest_data:
        swipe_macro(instance_name, 1054, 620, 457, 300)
    time.sleep(10)

    print('Skip')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1210, 50)
    time.sleep(10)

    print('Skip')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1210, 50)
    time.sleep(10)

    print('Skip')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1210, 50)
    time.sleep(10)

    print('Incase')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1045, 170)
    time.sleep(5)

    print('Global')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 960, 160)
    time.sleep(5)

    print('Global')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 435, 275)
    time.sleep(10)

    print('Global')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 435, 275)
    time.sleep(10)

    print('Global')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 435, 275)
    time.sleep(5)

    print('Global')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 435, 275)
    time.sleep(5)

    print('Click 2-1')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1005, 630)
    time.sleep(10)

    print('Start')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1005, 630)
    time.sleep(30)

    print('Skip')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1210, 50)
    time.sleep(8)

    print('Skip')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1210, 50)
    time.sleep(15)

    print('Swipe')
    for instance_name, _ in guest_data:
        swipe_macro(instance_name, 770, 624, 296, 318)
    time.sleep(10)

    print('Complete')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1165, 625)
    time.sleep(3)

    print('Complete')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 818, 495)
    time.sleep(3)

    print('Swipe')
    for instance_name, _ in guest_data:
        swipe_macro(instance_name, 925, 620, 605, 388)
    time.sleep(3)

    print('Swipe')
    for instance_name, _ in guest_data:
        swipe_macro(instance_name, 1054, 620, 605, 388)
    time.sleep(3)

    print('Swipe')
    for instance_name, _ in guest_data:
        swipe_macro(instance_name, 1182, 620, 605, 388)
    time.sleep(3)

    print('Swipe')
    for instance_name, _ in guest_data:
        swipe_macro(instance_name, 925, 620, 605, 388)
    time.sleep(3)

    print('Swipe')
    for instance_name, _ in guest_data:
        swipe_macro(instance_name, 1054, 620, 605, 388)
    time.sleep(3)

    print('Swipe')
    for instance_name, _ in guest_data:
        swipe_macro(instance_name, 1182, 620, 605, 388)
    time.sleep(3)

    print('Swipe')
    for instance_name, _ in guest_data:
        swipe_macro(instance_name, 925, 620, 605, 388)
    time.sleep(3)

    print('Swipe')
    for instance_name, _ in guest_data:
        swipe_macro(instance_name, 1054, 620, 605, 388)
    time.sleep(3)

    print('Swipe')
    for instance_name, _ in guest_data:
        swipe_macro(instance_name, 1182, 620, 605, 388)
    time.sleep(3)

    print('Swipe')
    for instance_name, _ in guest_data:
        swipe_macro(instance_name, 925, 620, 605, 388)
    time.sleep(3)

    print('Swipe')
    for instance_name, _ in guest_data:
        swipe_macro(instance_name, 1054, 620, 605, 388)
    time.sleep(3)

    print('Swipe')
    for instance_name, _ in guest_data:
        swipe_macro(instance_name, 1182, 620, 605, 388)
    time.sleep(3)

    print('Swipe')
    for instance_name, _ in guest_data:
        swipe_macro(instance_name, 925, 620, 605, 388)
    time.sleep(20)

    print('Skip')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1210, 50)
    time.sleep(15)

    print('Global')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1058, 183)
    time.sleep(10)

    print('Global')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1058, 183)
    time.sleep(20)

    print('Global')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1058, 183)
    time.sleep(10)

    # print('Global')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 1058, 183)
    # time.sleep(10)

    log_func(f"Close Game") # New Start
    for instance_name, _ in guest_data:
        os.system(f'ldconsole.exe adb --name "{instance_name}" --command "shell am force-stop com.skystone.silverblood.us"')
    time.sleep(10)

    log_func("Open Game")
    for instance_name, _ in guest_data:
        os.system(f'ldconsole.exe adb --name "{instance_name}" --command "shell monkey -p com.skystone.silverblood.us -c android.intent.category.LAUNCHER 1"')
        log_func(f"[{instance_name}] - Launched Silver and Blood")
    time.sleep(105)

    log_func("Start")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 800, 500)
    time.sleep(20)

    log_func(f"Close Notice")   
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1171, 104)
    time.sleep(10)

    print('Back')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1, 1)
    time.sleep(5)

    print('Back')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1, 1)
    time.sleep(5)

    path_close_button = "D:/Silver_Blood_Bot/templates/close_button.png"
    
    for instance_name, _ in guest_data:
        coords_close = detect_regular_summon(instance_name, template_path=path_close_button)
        if coords_close:
            print(f"🎯 Tapping close at {coords_close}")
            tap_macro(instance_name, coords_close[0], coords_close[1])
            time.sleep(5)
        else:
            print(f"❌ Could not find regular summon banner for {instance_name}")

    print('Incase')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1045, 170)
    time.sleep(5)

    print('Back')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1, 1)
    time.sleep(5)

    for instance_name, _ in guest_data:
        coords_close = detect_regular_summon(instance_name, template_path=path_close_button)
        if coords_close:
            print(f"🎯 Tapping close at {coords_close}")
            tap_macro(instance_name, coords_close[0], coords_close[1])
            time.sleep(5)
        else:
            print(f"❌ Could not find regular summon banner for {instance_name}")

    print('Incase')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1045, 170)
    time.sleep(5)

    for instance_name, _ in guest_data:
        coords_close = detect_regular_summon(instance_name, template_path=path_close_button)
        if coords_close:
            print(f"🎯 Tapping close at {coords_close}")
            tap_macro(instance_name, coords_close[0], coords_close[1])
            time.sleep(5)
        else:
            print(f"❌ Could not find regular summon banner for {instance_name}")
    
    print('Incase')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1045, 170)
    time.sleep(5)

    for instance_name, _ in guest_data:
        coords_close = detect_regular_summon(instance_name, template_path=path_close_button)
        if coords_close:
            print(f"🎯 Tapping close at {coords_close}")
            tap_macro(instance_name, coords_close[0], coords_close[1])
            time.sleep(5)
        else:
            print(f"❌ Could not find regular summon banner for {instance_name}")


    print('Incase')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1045, 170)
    time.sleep(5)

    print('Vassal')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 75, 655)
    time.sleep(15)

    print('Hero')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 295, 240)
    time.sleep(15)

    print('Click')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 75, 300)
    time.sleep(15)

    print('Global')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1, 1)
    time.sleep(10)

    print('Global')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1, 1)
    time.sleep(10)

    print('Global')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1, 1)
    time.sleep(10)

    print('Quick Equip')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 805, 605)
    time.sleep(10)

    print('Global')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1, 1)
    time.sleep(10)

    print('Global')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1, 1)
    time.sleep(10)

    print('Global')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1, 1)
    time.sleep(10)

    print('Global')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1, 1)
    time.sleep(10)

    print('Back')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1, 1)
    time.sleep(5)

    print('Back')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1, 1)
    time.sleep(5)

    print('Back')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1, 1)
    time.sleep(5)

    print('Back')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1, 1)
    time.sleep(5)

    print('Incase')
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1045, 170)
    time.sleep(5)

    template_path = "D:/Silver_Blood_Bot/templates/chapter_matcher.png"
    SCREENSHOT_DIR  = "D:/Silver_Blood_Bot/screenshots"

    valid_instances = []
    valid_guest_names = []

    for instance_name, guest_name in guest_data:
        log_func(f"[{instance_name}] Taking screenshot for {guest_name}")
        screenshot_path = take_screenshot_another(instance_name)

        if is_template_present(screenshot_path, template_path, threshold=0.80):
            log_func(f"[{instance_name}] ✅ Successfully reached login reward screen.")
            valid_instances.append(instance_name)
            valid_guest_names.append(guest_name)
        else:
            log_func(f"[{instance_name}] ❌ Failed to reach reward screen. Closing and deleting instance.")

            for day_file in os.listdir(SCREENSHOT_DIR):
                if day_file.startswith(instance_name):
                    try:
                        os.remove(os.path.join(SCREENSHOT_DIR, day_file))
                        log_func(f"[{instance_name}] 🗑️ Deleted extra screenshot {day_file}")
                    except Exception as e:
                        log_func(f"[{instance_name}] ⚠️ Could not delete {day_file}: {e}")

            close_instance(instance_name)
            time.sleep(10)
            delete_instance(instance_name)

        if os.path.exists(screenshot_path):
            os.remove(screenshot_path)

        log_func(f"✅ Batch {batch_num} completed\n")
    
    if valid_instances == []:
        log_func("Invalid Intances Data not Stored")
    else:
        save_batch_metadata(batch_num, valid_instances, valid_guest_names)

    for instance_name in valid_instances:
        log_func(f"[{instance_name}] Closing instance")
        close_instance(instance_name)

def run_all_batches(base_instance, total_accounts, instances_per_batch,guest_name , log_func):
    total_batches = total_accounts // instances_per_batch
    guest_index = 1

    for batch in range(1, total_batches + 1):
        log_func(f"🚀 Starting batch {batch}")
        run_batch(batch, guest_index, instances_per_batch, log_func, base_instance, guest_name)
        guest_index += instances_per_batch

import json
import os
from datetime import datetime

def get_persistent_path(filename, subdir=None):
    # Get Windows Local AppData folder, fallback to current dir if env var missing
    base_dir = os.path.join(os.getenv('LOCALAPPDATA'), 'SilverBloodReq')
    if subdir:
        base_dir = os.path.join(base_dir, subdir)
    os.makedirs(base_dir, exist_ok=True)
    return os.path.join(base_dir, filename)

def save_batch_metadata(batch_index, instance_names, guest_names):
    batch_id = f"batch_{batch_index:03d}"
    batch_data = {
        "batch_id": batch_id,
        "instance_names": instance_names,
        "guest_names": guest_names,
        "login_day": 1,
        "last_login": datetime.now().strftime("%Y-%m-%d"),
        "status": "Active"
    }

    json_path = get_persistent_path('batches.json')

    try:
        with open(json_path, "r") as f:
            all_batches = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        all_batches = []

    all_batches.append(batch_data)

    with open(json_path, "w") as f:
        json.dump(all_batches, f, indent=2)

if __name__ == "__main__":
    multiprocessing.freeze_support()
    run_all_batches(TOTAL_ACCOUNTS, INSTANCES_PER_BATCH, print)