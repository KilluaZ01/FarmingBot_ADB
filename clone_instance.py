import subprocess
import time
from pynput.mouse import Button, Controller as MouseController
from pynput.keyboard import Controller as KeyboardController

# Initialize controllers
mouse = MouseController()
keyboard = KeyboardController()

def launch_multildplayer(path):
    subprocess.Popen(path)  # Launch MultiLDPlayer
    time.sleep(10)  # Wait for it to open

def clone_instance(instance_name, clone_name):
    # Focus on MultiLDPlayer window
    mouse.click(Button.left, 1)  # Click to focus
    time.sleep(1)

    # Click on the base instance (adjust coordinates)
    mouse.position = (200, 200)  # Coordinates for the base instance
    mouse.click(Button.left, 1)
    time.sleep(1)

    # Click on the clone button (adjust coordinates)
    mouse.position = (300, 300)  # Coordinates for the clone option
    mouse.click(Button.left, 1)
    time.sleep(1)

    # Enter the new instance name
    keyboard.type(clone_name)
    time.sleep(1)

    # Confirm the cloning action
    keyboard.press('enter')
    keyboard.release('enter')

# Path to MultiLDPlayer executable
multildplayer_path = "C:/Users/Killua/Desktop/Apps/LDMultiPlayer.lnk"  # Update this path

# Launch MultiLDPlayer
launch_multildplayer(multildplayer_path)

# Clone the instances
clone_instance("LDPlayer", "instance_1")
time.sleep(3)  # Wait for the first clone to finish
clone_instance("LDPlayer", "instance_2")