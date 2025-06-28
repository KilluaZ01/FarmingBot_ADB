import multiprocessing
import time
from clone_utils import clone_instance, launch_instance
from config import NAME_PREFIX, CYCLE_PADDING, TOTAL_ACCOUNTS, INSTANCES_PER_BATCH
from macros import trigger_macro
from random import randint
from adb_utils import take_screenshot, close_instance, input_guest_name
import requests
from proxy_utils import get_proxy_list, rotate_proxy_ip
import subprocess

def generate_guest_name(index):
    result = f"{NAME_PREFIX}{randint(100, 1000)}X{str(index).zfill(CYCLE_PADDING)}"
    print(f"[NameGen] Index={index}, Result={result}")
    return result

def launch_with_proxifier(profile_path, instance_name):
    subprocess.Popen([
        "C:\\Program Files\\Proxifier\\Proxifier.exe",
        "/profile", profile_path,
        "/run", f"C:\\LDPlayer\\LDPlayer9\\dnplayer.exe --name {instance_name}"
    ])

def prepare_batch(batch_num, instances_per_batch, base_instance, proxy_api, log_func):
    instance_names = []
    proxies = get_proxy_list(proxy_api, log_func)

    if len(proxies) < instances_per_batch:
        raise Exception("Not enough proxies available for this batch")

    for i in range(instances_per_batch):
        new_name = f"LDPlayer-{(batch_num - 1) * instances_per_batch + i + 1}"
        clone_instance(base_instance, new_name)
        launch_instance(new_name)

        proxy = proxies[i]  # Assign 1 proxy per instance
        proxy_ip = proxy["ip"]
        proxy_port = proxy["port"]
        proxy_user = proxy["username"]
        proxy_pass = proxy["password"]
        proxy_id = proxy["id"]

        # Optional: Rotate IP
        rotate_proxy_ip(proxy_api, proxy_id, log_func)

        # Log it
        print(f"[{new_name}] Assigned proxy: {proxy_ip}:{proxy_port} ({proxy_user})")

        if proxy_ip == "127.0.0.1":
            print(f"[{new_name}] Using fallback/localhost — skipping proxifier")
        else:
            launch_with_proxifier(f"C:\\ProxifierProfiles\\proxifier_{i+1}.ppx", new_name)

        instance_names.append(new_name)
    return instance_names


def run_batch(batch_num, start_guest_index, instances_per_batch, log_func, base_instance, proxy_api):
    instance_names = prepare_batch(batch_num, instances_per_batch, base_instance, proxy_api, log_func)
    log_func(f"🛠️ Prepared batch {batch_num} with {len(instance_names)} instances")
    time.sleep(60)  # Let them boot

    guest_data = []
    for i, instance_name in enumerate(instance_names):
        guest_index = start_guest_index + i
        guest_name = generate_guest_name(guest_index)
        guest_data.append((instance_name, guest_name))
        log_func(f"[{instance_name}] Guest: {guest_name}")

    # Step 1: Launch macro to download assets
    for instance_name, _ in guest_data:
        trigger_macro(instance_name, "ctrl", "z")
        log_func(f"[{instance_name}] Launched macro (Openning Mirren)")
    time.sleep(12)

    for instance_name, _ in guest_data:
        trigger_macro(instance_name, "ctrl", "a")
        log_func(f"[{instance_name}] Launched macro (Download Assets)")
    time.sleep(330)

    for instance_name, _ in guest_data:
        trigger_macro(instance_name, "ctrl", "b")
        log_func(f"[{instance_name}] Launched macro (Skip to Name Input)")
    time.sleep(150)

    # Step 2: Input name
    for instance_name, guest_name in guest_data:
        input_guest_name(instance_name, guest_name)
        log_func(f"[{instance_name}] Input guest name: {guest_name}")
    time.sleep(20)

    for instance_name, _ in guest_data:
        trigger_macro(instance_name, "ctrl", "c")
        log_func(f"[{instance_name}] Launched macro (Pre-Summon)")
    time.sleep(580)

    for instance_name, _ in guest_data:
        trigger_macro(instance_name, "ctrl", "d")
        log_func(f"[{instance_name}] Launched macro (10x Summon)")
    time.sleep(245)

    for instance_name, guest_name in guest_data:
        log_func(f"[{instance_name}] Taking screenshot for {guest_name}")
        take_screenshot(instance_name, guest_name)

        log_func(f"[{instance_name}] Closing instance")
        close_instance(instance_name)


    log_func(f"✅ Batch {batch_num} completed\n")

def run_all_batches(base_instance, proxy_api, total_accounts, instances_per_batch, log_func):
    total_batches = total_accounts // instances_per_batch
    guest_index = 1

    for batch in range(1, total_batches + 1):
        log_func(f"🚀 Starting batch {batch}")
        run_batch(batch, guest_index, instances_per_batch, log_func, base_instance, proxy_api)
        guest_index += instances_per_batch

if __name__ == "__main__":
    multiprocessing.freeze_support()
    run_all_batches(TOTAL_ACCOUNTS, INSTANCES_PER_BATCH, print)
