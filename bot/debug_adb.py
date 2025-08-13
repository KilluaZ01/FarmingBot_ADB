import os
import re
import subprocess

# Path to LDPlayer config folder
CONFIG_PATH = r"D:\LDPlayer\LDPlayer9\vms\config"

# 2. Process config files
def adb_debugger():
    for filename in os.listdir(CONFIG_PATH):
        if filename.startswith("leidian") and filename.endswith(".config") and filename != "leidians.config":
            file_path = os.path.join(CONFIG_PATH, filename)
            # print(f"Processing {filename}...")

            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Skip if adbDebug already present
            if '"basicSettings.adbDebug"' in content:
                # print("  ADB already enabled, skipping.")
                continue

            # Split into lines without extra empty ones
            lines = [line.rstrip() for line in content.splitlines()]

            new_lines = []
            adb_added = False
            for line in lines:
                new_lines.append(line)
                if '"propertySettings.macAddress"' in line and not adb_added:
                    new_lines.append('    "basicSettings.adbDebug": 1,')
                    adb_added = True

            if adb_added:
                # Join with CRLF, remove consecutive blank lines
                clean_content = []
                prev_blank = False
                for line in new_lines:
                    if line.strip() == "":
                        if prev_blank:
                            continue
                        prev_blank = True
                    else:
                        prev_blank = False
                    clean_content.append(line)

                new_content = "\r\n".join(clean_content)

                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(new_content)

                # print("  adbDebug added.")
            else:
                # print("  macAddress not found — skipped.")