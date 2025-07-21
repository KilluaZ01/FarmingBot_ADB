import multiprocessing
import time
from clone_utils import clone_instance, launch_instance
from config import CYCLE_PADDING, TOTAL_ACCOUNTS, INSTANCES_PER_BATCH
from macros import tap_macro, swipe_macro
from random import randint
from adb_utils import take_screenshot, close_instance, input_guest_name, delete_instance
from template_matching import is_reward_screen
import requests
import threading
import subprocess
import os
from proxy_config import AIRPROXY


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

    for i in range(instances_per_batch):
        new_name = f"{base_instance}-{(batch_num - 1) * instances_per_batch + i + 1}"
        clone_instance(base_instance, new_name)
        launch_instance(new_name)

        proxy_ip = AIRPROXY.get("host")
        proxy_port = AIRPROXY.get("port")
        proxy_user = AIRPROXY.get("username")
        proxy_pass = AIRPROXY.get("password")

        # print(f"[{new_name}] Assigned AirProxy: {proxy_ip}:{proxy_port} ({proxy_user})")

        if proxy_ip == "127.0.0.1":
            log_func(f"[{new_name}] Skipping proxifier — using localhost")
        else:
            proxifier_profile = f"C:\\ProxifierProfiles\\profile-1.ppx"
            if not os.path.exists(proxifier_profile):
                # print(f"❌ Missing Proxifier profile: {proxifier_profile}")
                pass
            else:
                launch_with_proxifier(proxifier_profile, new_name)

        instance_names.append(new_name)

    return instance_names


def run_batch(batch_num, start_guest_index, instances_per_batch, log_func, base_instance, guest_name_prefix):
    instance_names = prepare_batch(batch_num, instances_per_batch, base_instance, log_func)
    log_func(f"🛠️ Prepared batch {batch_num} with {len(instance_names)} instances")
    time.sleep(50)  # Let them boot

    guest_data = []

    apk_dir = "C:/Users/Administrator/Desktop/silver_blood_extracted"
    # apk_dir = "C:/Users/Killua/Desktop/Silver/silver_blood_extracted"
    apk_files = [
        "com.skystone.silverblood.us.apk",
        "config.arm64_v8a.apk",
        "install_time_pack.apk"
    ]
    apk_paths = " ".join([f"{apk_dir}/{apk}" for apk in apk_files])
    INSTALL_TIMEOUT = 190  # seconds
    MAX_RETRIES = 2

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
    time.sleep(150)

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
    time.sleep(10)

    log_func(f"Download")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 605, 495)
    time.sleep(20)

    log_func(f"Download")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 605, 495)
    time.sleep(80)

    log_func(f"Background download Selected")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 370, 546)
    time.sleep(50)

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
    time.sleep(35)

    log_func(f"Swipe")
    for instance_name, _ in guest_data:
        swipe_macro(instance_name, 1060, 625, 755, 300)
    time.sleep(40)

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
    time.sleep(25)

    log_func(f"Skip")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1210, 50)
    time.sleep(20)

    log_func(f"Skip")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1210, 50)
    time.sleep(20)

    log_func(f"Click")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 900, 280)
    time.sleep(20)

    log_func(f"Skip")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1210, 50)
    time.sleep(25)

    log_func(f"Swipe")
    for instance_name, _ in guest_data:
        swipe_macro(instance_name, 905, 405, 695, 330)
    time.sleep(30)

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
    time.sleep(25)

    log_func(f"Swipe")
    for instance_name, _ in guest_data:
        swipe_macro(instance_name, 930, 625, 300, 490)
    time.sleep(40)

    log_func(f"Skip")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1210, 50)
    time.sleep(15)

    log_func(f"Skip")
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

    log_func(f"Start")
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
    time.sleep(10)

    log_func(f"Click")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 520, 300)
    time.sleep(10)

    log_func(f"Click")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 520, 300)
    time.sleep(20)

    log_func(f"Swipe")
    for instance_name, _ in guest_data:
        swipe_macro(instance_name, 920, 625, 515, 340)
    time.sleep(30)

    log_func(f"Skip")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1210, 50)
    time.sleep(20)

    log_func(f"Click")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 525, 420)
    time.sleep(10)

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
    time.sleep(45)

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
    time.sleep(5)

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
    time.sleep(5)

    log_func(f"Click") #Done
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1135, 210)
    time.sleep(5)

    log_func(f"Click")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1135, 210)
    time.sleep(5)

    log_func(f"Click")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1135, 210)
    time.sleep(5)

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
    time.sleep(5)

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
    time.sleep(5)

    log_func(f"Lost Courtyard")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1200, 475)
    time.sleep(5)

    log_func(f"Lost Courtyard")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1200, 475)
    time.sleep(5)

    log_func(f"Lost Courtyard")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1200, 475)
    time.sleep(10)

    log_func(f"Lost Courtyard")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1200, 475)
    time.sleep(5)

    log_func(f"Lost Courtyard")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1200, 475)
    time.sleep(5)

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
    time.sleep(5)

    log_func(f"Click Timeworn")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1100, 150)
    time.sleep(5)

    log_func(f"Click Timeworn")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1100, 150)
    time.sleep(5)

    log_func(f"Click Timeworn")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1100, 150)
    time.sleep(5)

    log_func(f"Click Timeworn")
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1100, 150)
    time.sleep(5)

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
    time.sleep(5)

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

    log_func(f"Close Notice")   
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1171, 104)
    time.sleep(20)

    log_func(f"Continue 7x")   
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1171, 104)
    time.sleep(20)

    log_func(f"Close 7x")   
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1171, 104)
    time.sleep(20)

    log_func(f"Continue 14x")   
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1171, 104)
    time.sleep(20)

    # log_func(f"Open Event")   
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 913, 116)
    # time.sleep(20)

    # log_func(f"10x Scroll")   
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 82, 166)
    # time.sleep(20)

    # log_func(f"10x Scroll Click")   
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 440, 278)
    # time.sleep(20)

    # log_func(f"10x Scroll Click")   
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 440, 278)
    # time.sleep(20)



    # log_func(f"Click New")
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 953, 640)
    # time.sleep(10)

    # log_func(f"Click New")
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 953, 640)
    # time.sleep(10)

    # log_func(f"Click New")
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 953, 640)
    # time.sleep(5)

    # log_func(f"Click New")
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 953, 640)
    # time.sleep(5)

    # log_func(f"Click New")
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 953, 640)
    # time.sleep(5)

    # log_func(f"Click New")
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 953, 640)
    # time.sleep(10)

    # log_func(f"Click New")
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 953, 640)
    # time.sleep(10)

    # log_func(f"Click New")
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 953, 640)
    # time.sleep(10)

    # log_func(f"Click New")
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 1172, 630)
    # time.sleep(30)

    # log_func(f"Swipe")
    # for instance_name, _ in guest_data:
    #     swipe_macro(instance_name, 930, 620, 1135, 365)
    # time.sleep(2)

    # log_func(f"Swipe")
    # for instance_name, _ in guest_data:
    #     swipe_macro(instance_name, 930, 620, 1048, 255)
    # time.sleep(2)

    # log_func(f"Swipe")
    # for instance_name, _ in guest_data:
    #     swipe_macro(instance_name, 930, 620, 1070, 335)
    # time.sleep(2)

    # log_func(f"Swipe")
    # for instance_name, _ in guest_data:
    #     swipe_macro(instance_name, 930, 620, 1006, 166)
    # time.sleep(15)

    # log_func(f"Click")
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 1135, 365)
    # time.sleep(15)

    # log_func(f"Click")
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 1135, 365)
    # time.sleep(10)

    # log_func(f"Click")
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 1135, 365)
    # time.sleep(10)

    # log_func(f"Click")
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 1135, 365)
    # time.sleep(10)

    # log_func(f"Click")
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 1135, 365)
    # time.sleep(5)

    # log_func(f"Click")
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 1135, 365)
    # time.sleep(5)

    # log_func(f"Click")
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 1252, 42)
    # time.sleep(10)

    # log_func(f"Swipe")
    # for instance_name, _ in guest_data:
    #     swipe_macro(instance_name, 871, 533, 399, 171)
    # time.sleep(15)

    # log_func(f"Skip")
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 399, 171)
    # time.sleep(10)

    # log_func(f"Click")
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 397, 171)
    # time.sleep(10)

    # log_func(f"Swipe")
    # for instance_name, _ in guest_data:
    #     swipe_macro(instance_name, 871, 171, 396, 171)
    # time.sleep(15)

    # log_func(f"Click")
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 397, 171)
    # time.sleep(10)

    # log_func(f"Return")
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 1033, 650)
    # time.sleep(18)

    # log_func(f"Click")
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 1033, 650)
    # time.sleep(10)

    # log_func(f"Swipe")
    # for instance_name, _ in guest_data:
    #     swipe_macro(instance_name, 874, 172, 328, 284)
    # time.sleep(15)

    # log_func(f"Swipe")
    # for instance_name, _ in guest_data:
    #     swipe_macro(instance_name, 870, 352, 399, 279)
    # time.sleep(15)

    # log_func(f"Click")
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 399, 279)
    # time.sleep(5)

    # log_func(f"Click")
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 399, 279)
    # time.sleep(5)

    # log_func(f"Click")
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 399, 279)
    # time.sleep(10)

    # log_func(f"Click")
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 1033, 650)
    # time.sleep(10)

    # log_func(f"Swipe")
    # for instance_name, _ in guest_data:
    #     swipe_macro(instance_name, 926, 621, 1144, 252)
    # time.sleep(20)

    # log_func(f"Click")
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 1033, 650)
    # time.sleep(30)

    # log_func(f"Click")
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 1033, 650)
    # time.sleep(15)

    # log_func(f"Back")
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 60, 40)
    # time.sleep(8)

    # log_func(f"Back")
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 60, 40)
    # time.sleep(8)

    # log_func(f"Back")
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 60, 40)
    # time.sleep(10)

    # log_func(f"Back")
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 60, 40)
    # time.sleep(10)

    # log_func(f"Back")
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 60, 40)
    # time.sleep(20)

    # log_func(f"Click")
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 75, 170)
    # time.sleep(15)

    # log_func(f"Click") # From Here
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 808, 111)
    # time.sleep(10)

    # log_func(f"Click")
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 445, 275)
    # time.sleep(10)

    # log_func(f"Click")
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 445, 275)
    # time.sleep(10)

    # log_func(f"Back")
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 60, 40)
    # time.sleep(10)

    # log_func(f"Click")
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 1141, 351)
    # time.sleep(15)

    # log_func(f"Click")
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 1141, 351)
    # time.sleep(10)

    valid_instances = []
    valid_guest_names = []

    for instance_name, guest_name in guest_data:
        log_func(f"[{instance_name}] Taking screenshot for {guest_name}")
        take_screenshot(instance_name)
        if is_reward_screen(instance_name):
            log_func(f"[{instance_name}] ✅ Successfully reached login reward screen.")
            valid_instances.append(instance_name)
            valid_guest_names.append(guest_name)

            log_func(f"[{instance_name}] Closing instance")
            close_instance(instance_name)

        else:
            log_func(f"[{instance_name}] ❌ Failed to reach reward screen. Closing and deleting instance.")
            close_instance(instance_name)
            delete_instance(instance_name)

    log_func(f"✅ Batch {batch_num} completed\n")
    
    if valid_instances == []:
        log_func("Invalid Intances Data not Stored")
    else:
        save_batch_metadata(batch_num, valid_instances, valid_guest_names)

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
        "summon_done": False,
        "screenshot_saved": False
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
