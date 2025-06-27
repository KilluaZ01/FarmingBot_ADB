import os
import time

# Path to ldconsole.exe (adjust if different)
LDPLAYER_PATH = r"C:\LDPlayer\LDPlayer9\ldconsole.exe"

def clone_and_rename(base_name, new_name):
    # Step 1: Clone the base instance
    print(f"Cloning instance '{base_name}'...")
    os.system(f'"ldconsole.exe copy --name {new_name} --from {base_name}')

    # Step 2: Wait a bit for cloning to complete
    time.sleep(2)

# 🔧 Usage
clone_and_rename(base_name="LDPlayer", new_name="LDTester")
