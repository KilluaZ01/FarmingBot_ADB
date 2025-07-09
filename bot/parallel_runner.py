import multiprocessing
import time
from clone_utils import clone_instance, launch_instance
from config import CYCLE_PADDING, TOTAL_ACCOUNTS, INSTANCES_PER_BATCH
from macros import trigger_macro
from random import randint
from adb_utils import take_screenshot, close_instance, input_guest_name, tap_macro
import requests
import subprocess
import os
from proxy_config import AIRPROXY


download_time = 0

def generate_guest_name(index, prefix):
    result = f"{prefix}{randint(100, 1000)}X{str(index).zfill(CYCLE_PADDING)}"
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

        log_func(f"[{new_name}] Assigned AirProxy: {proxy_ip}:{proxy_port} ({proxy_user})")

        if proxy_ip == "127.0.0.1":
            log_func(f"[{new_name}] Skipping proxifier — using localhost")
        else:
            proxifier_profile = f"C:\\ProxifierProfiles\\profile-1.ppx"
            if not os.path.exists(proxifier_profile):
                log_func(f"❌ Missing Proxifier profile: {proxifier_profile}")
            else:
                launch_with_proxifier(proxifier_profile, new_name)

        instance_names.append(new_name)

    return instance_names


def run_batch(batch_num, start_guest_index, instances_per_batch, log_func, base_instance, guest_name_prefix):

    if instances_per_batch == 4:
        download_time = 540
    elif instances_per_batch == 3:
        download_time = 400
    else:
        download_time = 330

    instance_names = prepare_batch(batch_num, instances_per_batch, base_instance, log_func)
    log_func(f"🛠️ Prepared batch {batch_num} with {len(instance_names)} instances")
    time.sleep(80)  # Let them boot

    guest_data = []
    for i, instance_name in enumerate(instance_names):
        guest_index = start_guest_index + i
        guest_name = generate_guest_name(guest_index, guest_name_prefix)
        guest_data.append((instance_name, guest_name))
        log_func(f"[{instance_name}] Guest: {guest_name}")
    
    

    for instance_name, _ in guest_data:
        os.system(f'"ldconsole.exe adb --name {instance_name} --command "shell monkey -p com.mirrenapjob.eu -c android.intent.category.LAUNCHER 1"')
        log_func(f"[{instance_name}] - Openning Mirren")
    time.sleep(15)

    for instance_name, _ in guest_data:
        tap_macro(instance_name ,366, 337)
    time.sleep(5)

    for instance_name, _ in guest_data:
        tap_macro(instance_name ,366, 381)
    time.sleep(5)

    for instance_name, _ in guest_data:
        tap_macro(instance_name ,630, 455)
        log_func(f"[{instance_name}] - Downloading Assets")
    time.sleep(60)

    for instance_name, _ in guest_data:
        tap_macro(instance_name, 383, 401)
    time.sleep(5)
    
    for instance_name, _ in guest_data:
        tap_macro(instance_name, 826, 492)
    time.sleep(400)

    for instance_name, _ in guest_data:
        log_func(f"[{instance_name}] - Download Completed")
        tap_macro(instance_name, 300, 300)
    time.sleep(5)

    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1237, 81)
    time.sleep(10)

    for instance_name, _ in guest_data:
        tap_macro(instance_name, 643, 544)
    time.sleep(5)

    for instance_name, _ in guest_data:
        tap_macro(instance_name, 732, 557)
    time.sleep(5)

    for instance_name, _ in guest_data:
        tap_macro(instance_name, 812, 273)
    time.sleep(2)

    for instance_name, _ in guest_data:
        tap_macro(instance_name, 668, 495)
    time.sleep(30)

    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1235, 42)
    time.sleep(5)

    for instance_name, _ in guest_data:
        tap_macro(instance_name, 546, 446)
    time.sleep(2)

    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1047, 517)
    time.sleep(30)

    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1235, 42)
    time.sleep(5)

    for instance_name, _ in guest_data:
        tap_macro(instance_name, 546, 446)
    time.sleep(2)

    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1235, 42)
    time.sleep(5)

    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1020, 517)
    time.sleep(10)

    for instance_name, _ in guest_data:
        tap_macro(instance_name, 790, 491)
    time.sleep(5)

    for instance_name, guest_name in guest_data:
        input_guest_name(instance_name, guest_name)
        log_func(f"[{instance_name}] Input guest name: {guest_name}")
    time.sleep(20)

    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1103, 522)
    time.sleep(20)

    for instance_name, _ in guest_data:
        tap_macro(instance_name, 119, 206)
    time.sleep(5)

    for instance_name, _ in guest_data:
        tap_macro(instance_name, 74, 473)
    time.sleep(5)

    for instance_name, _ in guest_data:
        tap_macro(instance_name, 85, 633)
    time.sleep(5)

    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1117, 645)
    time.sleep(5)

    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1117, 645)
    time.sleep(5)

    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1200, 234)
    time.sleep(5)

    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1200, 234)
    time.sleep(10)

    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1117, 645)
    time.sleep(8)

    for instance_name, _ in guest_data:
        tap_macro(instance_name, 74, 473)
    time.sleep(5)

    for instance_name, _ in guest_data:
        tap_macro(instance_name, 74, 473)
    time.sleep(20)

    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1235, 42)
    time.sleep(5)

    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1020, 517)
    time.sleep(10)

    for instance_name, _ in guest_data:
        tap_macro(instance_name, 500, 500)
    time.sleep(5)

    for instance_name, _ in guest_data:
        tap_macro(instance_name, 500, 500)
    time.sleep(10)

    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1235, 42)
    time.sleep(5)

    for instance_name, _ in guest_data:
        tap_macro(instance_name, 670, 450)
    time.sleep(20)

    for instance_name, _ in guest_data:
        tap_macro(instance_name, 670, 450)
    time.sleep(5)

    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1235, 42)
    time.sleep(5)

    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1020, 517)
    time.sleep(10)

    for instance_name, _ in guest_data:
        tap_macro(instance_name, 670, 415)
    time.sleep(3)

    for instance_name, _ in guest_data:
        tap_macro(instance_name, 670, 415)
    time.sleep(5)

    for instance_name, _ in guest_data:
        tap_macro(instance_name, 670, 540)
    time.sleep(10)

    for instance_name, _ in guest_data:
        tap_macro(instance_name, 525, 285)
    time.sleep(5)

    for instance_name, _ in guest_data:
        tap_macro(instance_name, 525, 285)
    time.sleep(5)

    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1173, 678)
    time.sleep(5)

    for instance_name, _ in guest_data:
        tap_macro(instance_name, 707, 139)
    time.sleep(5)

    for instance_name, _ in guest_data:
        tap_macro(instance_name, 622, 125)
    time.sleep(5)

    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1173, 678)
    time.sleep(5)

    for instance_name, _ in guest_data:
        tap_macro(instance_name, 440, 395)
    time.sleep(5)

    for instance_name, _ in guest_data:
        tap_macro(instance_name, 928, 290)
    time.sleep(5)

    for instance_name, _ in guest_data:
        tap_macro(instance_name, 900, 290)
    time.sleep(5)

    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1173, 678)
    time.sleep(5)

    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1117, 675)
    time.sleep(10)

    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1235, 42)
    time.sleep(5)

    for instance_name, _ in guest_data:
        tap_macro(instance_name, 546, 446)
    time.sleep(10)

    for instance_name, _ in guest_data:
        tap_macro(instance_name, 430, 260)
    time.sleep(5)

    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1173, 678)
    time.sleep(5)

    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1210, 235)
    time.sleep(5)

    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1210, 235)
    time.sleep(5)

    for instance_name, _ in guest_data:
        tap_macro(instance_name, 430, 260)
    time.sleep(5)

    for instance_name, _ in guest_data:
        tap_macro(instance_name, 74, 473)
    time.sleep(10)

    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1177, 118)
    time.sleep(5)

    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1173, 678)
    time.sleep(5)

    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1117, 678)
    time.sleep(5)

    for instance_name, _ in guest_data:
        tap_macro(instance_name, 720, 395)
    time.sleep(8)

    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1173, 678)
    time.sleep(8)

    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1210, 235)
    time.sleep(5)

    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1210, 235)
    time.sleep(10)

    for instance_name, _ in guest_data:
        tap_macro(instance_name, 74, 473)
    time.sleep(5)

    for instance_name, _ in guest_data:
        tap_macro(instance_name, 74, 473)
    time.sleep(10)

    for instance_name, _ in guest_data:
        tap_macro(instance_name, 74, 473)
    time.sleep(8)

    for instance_name, _ in guest_data:
        tap_macro(instance_name, 74, 473)
    time.sleep(20)

    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1235, 42)
    time.sleep(5)

    for instance_name, _ in guest_data:
        tap_macro(instance_name, 540, 445)
    time.sleep(3)

    for instance_name, _ in guest_data:
        tap_macro(instance_name, 995, 515)
    time.sleep(10)

    for instance_name, _ in guest_data:
        tap_macro(instance_name, 670, 415)
    time.sleep(5)

    for instance_name, _ in guest_data:
        tap_macro(instance_name, 670, 415)
    time.sleep(10)

    for instance_name, _ in guest_data:
        tap_macro(instance_name, 130, 475)
    time.sleep(5)

    for instance_name, _ in guest_data:
        tap_macro(instance_name, 130, 475)
    time.sleep(8)

    for instance_name, _ in guest_data:
        tap_macro(instance_name, 670, 415)
    time.sleep(5)

    for instance_name, _ in guest_data:
        tap_macro(instance_name, 42, 35)
    time.sleep(10)

    for instance_name, _ in guest_data:
        tap_macro(instance_name, 85, 640)
    time.sleep(5)

    for instance_name, _ in guest_data:
        tap_macro(instance_name, 830, 640)
    time.sleep(8)

    for instance_name, _ in guest_data:
        tap_macro(instance_name, 445, 480)
    time.sleep(5)

    for instance_name, _ in guest_data:
        tap_macro(instance_name, 42, 35)
    time.sleep(10)

    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1216, 90)
    time.sleep(5)

    for instance_name, _ in guest_data:
        tap_macro(instance_name, 55, 140)
    time.sleep(5)

    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1095, 615)
    time.sleep(5)

    for instance_name, _ in guest_data:
        tap_macro(instance_name, 670, 415)
    time.sleep(5)

    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1242, 80)
    time.sleep(5)

    for instance_name, _ in guest_data:
        tap_macro(instance_name, 80, 625)
    time.sleep(5)

    for instance_name, _ in guest_data:
        tap_macro(instance_name, 1145, 650)
    time.sleep(5)


    for instance_name, _ in guest_data:
        tap_macro(instance_name, 825, 476)
    time.sleep(20)

    for i in range(9):
        for instance_name, _ in guest_data:
            tap_macro(instance_name, 1190, 40)
        time.sleep(20)

    # for instance_name, _ in guest_data:
    #     trigger_macro(instance_name, "ctrl", "a")
    #     log_func(f"[{instance_name}] Launched macro (Download Assets)")
    # time.sleep(download_time)

    # for instance_name, _ in guest_data:
    #     trigger_macro(instance_name, "ctrl", "b")
    #     log_func(f"[{instance_name}] Launched macro (Skip to Name Input)")
    # time.sleep(150)

    # for instance_name, guest_name in guest_data:
    #     input_guest_name(instance_name, guest_name)
    #     log_func(f"[{instance_name}] Input guest name: {guest_name}")
    # time.sleep(20)

    # for instance_name, _ in guest_data:
    #     trigger_macro(instance_name, "ctrl", "c")
    #     log_func(f"[{instance_name}] Launched macro (First Summon and small battle)")
    # time.sleep(320)

    # for instance_name, _ in guest_data:
    #     trigger_macro(instance_name, "ctrl", "d")
    #     log_func(f"[{instance_name}] Launched macro (Sensitive macro part)")
    # time.sleep(140)

    # for instance_name, _ in guest_data:
    #     trigger_macro(instance_name, "ctrl", "e")
    #     log_func(f"[{instance_name}] Launched macro (Long Battle)")
    # time.sleep(290)

    # for instance_name, _ in guest_data:
    #     trigger_macro(instance_name, "ctrl", "x")
    #     log_func(f"[{instance_name}] Launched macro (Pre-Summon)")
    # time.sleep(205)

    # for instance_name, _ in guest_data:
    #     trigger_macro(instance_name, "ctrl", "y")
    #     log_func(f"[{instance_name}] Launched macro (10x Summon)")
    # time.sleep(280)

    for instance_name, guest_name in guest_data:
        log_func(f"[{instance_name}] Taking screenshot for {guest_name}")
        take_screenshot(instance_name)

        log_func(f"[{instance_name}] Closing instance")
        close_instance(instance_name)

    log_func(f"✅ Batch {batch_num} completed\n")

def run_all_batches(base_instance, total_accounts, instances_per_batch,guest_name , log_func):
    total_batches = total_accounts // instances_per_batch
    guest_index = 1

    for batch in range(1, total_batches + 1):
        log_func(f"🚀 Starting batch {batch}")
        run_batch(batch, guest_index, instances_per_batch, log_func, base_instance, guest_name)
        guest_index += instances_per_batch

if __name__ == "__main__":
    multiprocessing.freeze_support()
    run_all_batches(TOTAL_ACCOUNTS, INSTANCES_PER_BATCH, print)
