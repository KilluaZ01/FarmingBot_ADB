import time
import config
import macros
from adb_utils import input_guest_name, clear_app_data, take_screenshot, close_instance

def generate_guest_name(index):
    return f"{config.NAME_PREFIX}_{index:0{config.CYCLE_PADDING}}"

def run_cycle(instance_name, _, guest_index):
    guest_name = generate_guest_name(guest_index)
    print(f"[{instance_name}] Guest: {guest_name}")
    time.sleep(10)

    clear_app_data(instance_name, config.PACKAGE_NAME)
    print(f"[{instance_name}] Cleared app data")
    time.sleep(10)

    print("Waiting for app to launch...")
    print("Triggering macro after game launch...")
    macros.trigger_macro('ctrl', 'z')
    time.sleep(10)

    macros.trigger_macro('ctrl', 'a')
    time.sleep(220)

    macros.trigger_macro('ctrl', 'b')
    time.sleep(10)

    print("Triggering macro Ctrl + B...")
    macros.trigger_macro('ctrl', 'c')
    time.sleep(180)

    input_guest_name(instance_name, guest_name)

    print("Triggering macro Ctrl + C...")
    macros.trigger_macro('ctrl', 'd')
    time.sleep(340)
    
    print("Triggering macro Ctrl + C...")
    macros.trigger_macro('ctrl', 'e')
    time.sleep(210)

    take_screenshot(instance_name, guest_name)
    print(f"[{instance_name}] Screenshot saved")

    close_instance(instance_name)
    print(f"[{instance_name}] Closed Successfully")

