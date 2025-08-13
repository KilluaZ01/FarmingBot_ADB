import time
import subprocess
import os

def launch_instance(instance_name):
    subprocess.run(f'ldconsole.exe launch --name "{instance_name}"', shell=True)

def tap_macro(instance_name, x, y):
    tap_command = f'ldconsole.exe adb --name {instance_name} --command "shell input tap {x} {y}"'
    os.system(tap_command)

def swipe_macro(instance_name, x1, y1, x2, y2):
    tap_command = f'ldconsole.exe adb --name {instance_name} --command "shell input touchscreen swipe {x1} {y1} {x2} {y2} 1000"'
    os.system(tap_command)

def batch(instance_names):
    for instance_name, _ in instance_names:
        launch_instance(instance_name)

    # ⏳ Wait a bit to let instances boot
    time.sleep(40)

    for instance_name, _ in instance_names:
        os.system(f'ldconsole.exe adb --name "{instance_name}" --command "shell monkey -p com.skystone.silverblood.us -c android.intent.category.LAUNCHER 1"')
        print(f"[{instance_name}] - Launched Silver and Blood")
    time.sleep(100)

    # Required After Claiming 14 days login 
    # print(f"Back")
    # for instance_name, _ in instance_names:
    #     tap_macro(instance_name, 60, 40)
    # time.sleep(8)

    print('Start Clicked')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 800, 500)
    time.sleep(30)

    print('Incase')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 1, 1)
    time.sleep(2)
    
    # Start From here After all
    print(f"Open Event")   
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 1104, 114)
    time.sleep(10)

    print(f"10x Scroll Click")   
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 440, 278)
    time.sleep(5)

    print(f"10x Scroll Click")   
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 440, 278)
    time.sleep(8)

    print('Incase')
    for instance_name, _ in instance_names:
        tap_macro(instance_name, 1, 1)
    time.sleep(5)

    # # Start From here After all
    # print(f"Open Event")   
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 1104, 114)
    # time.sleep(10)

    # print(f"10x Scroll Click")   
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 440, 278)
    # time.sleep(5)

    # print(f"10x Scroll Click")   
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 440, 278)
    # time.sleep(8)

    # print('Incase')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 1, 1)
    # time.sleep(5)

    # # For Entering Chapter
    # print('Thread of Fate')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 1135, 630)
    # time.sleep(15)

    # print('Thread of Fate')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 1135, 630)
    # time.sleep(10)

    # print('Start')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 1005, 630)
    # time.sleep(25)

    # print('Skip')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 1210, 50)
    # time.sleep(15)

    # print('Skip')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 1210, 50)
    # time.sleep(10)

    # print('Global')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 1058, 183)
    # time.sleep(10)

    # print('Complete')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 1165, 625)
    # time.sleep(10)

    # print('Continue')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 455, 500)
    # time.sleep(10)

    # print('Global')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 1058, 183)
    # time.sleep(10)

    # print('Global')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 1058, 183)
    # time.sleep(40)

    # print('Global')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 1058, 183)
    # time.sleep(10)

    # print('Vassal')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 482, 615)
    # time.sleep(15)

    # print('Hero')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 285, 255)
    # time.sleep(10)

    # print('Add')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 1100, 315)
    # time.sleep(10)

    # print('Max')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 1195, 540)
    # time.sleep(10)

    # print('Upgrade')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 1075, 650)
    # time.sleep(10)

    # print('Back')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 55, 40)
    # time.sleep(10)

    # print('Back')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 55, 40)
    # time.sleep(10)

    # print('Hero')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 285, 255)
    # time.sleep(10)

    # print('Tap')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 70, 415)
    # time.sleep(10)

    # print('Global')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 1, 1)
    # time.sleep(8)

    # print('Global')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 1, 1)
    # time.sleep(8)

    # print('Global')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 1, 1)
    # time.sleep(8)

    # print('Global')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 1, 1)
    # time.sleep(8)

    # print('Global')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 1, 1)
    # time.sleep(8)

    # print('Back')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 55, 40)
    # time.sleep(8)

    # print('Back')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 55, 40)
    # time.sleep(8)

    # print('Threads')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 1135, 630)
    # time.sleep(10)

    # print('Threads')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 1135, 630)
    # time.sleep(10)

    # print('Start')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 1005, 630)
    # time.sleep(20)

    # print('Skip')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 1210, 50)
    # time.sleep(10)

    # print('Skip')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 1210, 50)
    # time.sleep(8)

    # print('Global')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 1058, 183)
    # time.sleep(8)

    # print('Swipe')
    # for instance_name, _ in guest_data:
    #     swipe_macro(instance_name, 655, 630, 480, 315)
    # time.sleep(3)

    # print('Swipe')
    # for instance_name, _ in guest_data:
    #     swipe_macro(instance_name, 655, 630, 350, 405)
    # time.sleep(3)

    # print('Complete')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 1165, 625)
    # time.sleep(10)

    # print('Global')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 1058, 183)
    # time.sleep(5)

    # print('Global')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 1058, 183)
    # time.sleep(35)

    # print('Continue -> 1-5 Completed')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 1058, 183)
    # time.sleep(20)      # 1-5 Completed

    # print('Global')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 1058, 183)
    # time.sleep(10)

    # print('1-6 Click')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 1005, 630)
    # time.sleep(10)

    # print('Start')  
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 1005, 630)
    # time.sleep(20)

    # print('Skip')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 1210, 50)
    # time.sleep(15)

    # print('Global')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 1058, 183)
    # time.sleep(10)

    # print('Global')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 1058, 183)
    # time.sleep(10)

    # print('Global')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 1058, 183)
    # time.sleep(10)

    # print('Complete')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 1165, 625)
    # time.sleep(20)

    # print('Mixed')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 925, 620)
    # time.sleep(1)

    # print('Mixed')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 380, 422)
    # time.sleep(3)

    # print('Mixed')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 925, 620)
    # time.sleep(1)

    # print('Mixed')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 380, 422)
    # time.sleep(3)

    # print('Mixed')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 925, 620)
    # time.sleep(1)

    # print('Mixed')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 380, 422)
    # time.sleep(3)

    # print('Mixed')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 925, 620)
    # time.sleep(1)

    # print('Mixed')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 380, 422)
    # time.sleep(30)

    # print('Skip')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 1210, 50)
    # time.sleep(10)

    # print('Global')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 1, 1)
    # time.sleep(10)

    # print('Skip')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 1210, 50)
    # time.sleep(20)

    # print('Skip')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 1210, 50)
    # time.sleep(10)

    # print('Global')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 1, 1)
    # time.sleep(10)

    # print('Global')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 1, 1)
    # time.sleep(10)

    # print('Sword')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 815, 175)
    # time.sleep(10)

    # print('Start')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 1005, 630)
    # time.sleep(20)

    # # Sword
    # print('Complete')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 1165, 625)
    # time.sleep(35)

    # print('Global')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 1189, 650)
    # time.sleep(15)

    # print('Start')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 1005, 630)
    # time.sleep(10)

    # print('Start')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 1005, 630)
    # time.sleep(20)

    # print('Skip')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 1210, 50)
    # time.sleep(10)

    # # 1-7
    # print('Complete')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 1165, 625)
    # time.sleep(10)

    # print('Mixed')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 925, 620)
    # time.sleep(1)

    # print('Mixed')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 380, 422)
    # time.sleep(3)

    # print('Mixed')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 925, 620)
    # time.sleep(1)

    # print('Mixed')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 380, 422)
    # time.sleep(3)

    # print('Mixed')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 925, 620)
    # time.sleep(1)

    # print('Mixed')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 380, 422)
    # time.sleep(3)

    # print('Mixed')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 1024, 620)
    # time.sleep(1)

    # print('Mixed')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 380, 422)
    # time.sleep(3)

    # print('Mixed')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 1182, 620)
    # time.sleep(1)

    # print('Mixed')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 380, 422)
    # time.sleep(3)

    # print('Mixed')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 925, 620)
    # time.sleep(1)

    # print('Mixed')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 380, 422)
    # time.sleep(3)

    # print('Mixed')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 1024, 620)
    # time.sleep(1)

    # print('Mixed')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 380, 422)
    # time.sleep(3)

    # print('Mixed')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 1182, 620)
    # time.sleep(1)

    # print('Mixed')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 380, 422)
    # time.sleep(3)

    # print('Mixed')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 925, 620)
    # time.sleep(1)

    # print('Mixed')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 380, 422)
    # time.sleep(3)

    # print('Mixed')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 1024, 620)
    # time.sleep(1)

    # print('Mixed')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 380, 422)
    # time.sleep(3)

    # print('Mixed')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 1182, 620)
    # time.sleep(1)

    # print('Mixed')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 380, 422)
    # time.sleep(3)

    # print('Mixed')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 925, 620)
    # time.sleep(1)

    # print('Mixed')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 380, 422)
    # time.sleep(25)

    # print('Skip')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 1210, 50)
    # time.sleep(10)

    # print('Global')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 1, 1)
    # time.sleep(10)

    # print('Global')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 270, 240)
    # time.sleep(15)

    # print('Global')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 270, 240)
    # time.sleep(10)

    # print('1-8 Start')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 1005, 630)
    # time.sleep(10)

    # print('Start')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 1005, 630)
    # time.sleep(20)

    # print('Skip')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 1210, 50)
    # time.sleep(15)

    # print('Global')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 1, 1)
    # time.sleep(7)

    # print('Global')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 1, 1)
    # time.sleep(7)

    # print('Global')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 1058, 183)
    # time.sleep(7)

    # print('Global')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 1058, 183)
    # time.sleep(2)

    # print('Global')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 1058, 183)
    # time.sleep(5)

    # print('Complete')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 1165, 625)
    # time.sleep(15)

    # print('Swipe')
    # for instance_name, _ in guest_data:
    #     swipe_macro(instance_name, 925, 620, 301, 527)
    # time.sleep(3)

    # print('Swipe')
    # for instance_name, _ in guest_data:
    #     swipe_macro(instance_name, 1054, 620, 301, 527)
    # time.sleep(3)

    # print('Swipe')
    # for instance_name, _ in guest_data:
    #     swipe_macro(instance_name, 1182, 620, 301, 527)
    # time.sleep(3)

    # print('Swipe')
    # for instance_name, _ in guest_data:
    #     swipe_macro(instance_name, 925, 620, 301, 527)
    # time.sleep(3)

    # print('Swipe')
    # for instance_name, _ in guest_data:
    #     swipe_macro(instance_name, 1054, 620, 301, 527)
    # time.sleep(3)

    # print('Swipe')
    # for instance_name, _ in guest_data:
    #     swipe_macro(instance_name, 1182, 620, 301, 527)
    # time.sleep(3)

    # print('Swipe')
    # for instance_name, _ in guest_data:
    #     swipe_macro(instance_name, 925, 620, 301, 527)
    # time.sleep(3)

    # print('Swipe')
    # for instance_name, _ in guest_data:
    #     swipe_macro(instance_name, 925, 620, 301, 527)
    # time.sleep(3)

    # print('Swipe')
    # for instance_name, _ in guest_data:
    #     swipe_macro(instance_name, 1054, 620, 301, 527)
    # time.sleep(3)

    # print('Swipe')
    # for instance_name, _ in guest_data:
    #     swipe_macro(instance_name, 1182, 620, 301, 527)
    # time.sleep(3)

    # print('Swipe')
    # for instance_name, _ in guest_data:
    #     swipe_macro(instance_name, 925, 620, 301, 527)
    # time.sleep(3)

    # print('Swipe')
    # for instance_name, _ in guest_data:
    #     swipe_macro(instance_name, 1054, 620, 301, 527)
    # time.sleep(3)

    # print('Swipe')
    # for instance_name, _ in guest_data:
    #     swipe_macro(instance_name, 1182, 620, 301, 527)
    # time.sleep(10)

    # print('Skip')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 1210, 50)
    # time.sleep(20)

    # print('Global')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 405, 245)
    # time.sleep(10)

    # print('1-9 -> Start')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 1005, 630)
    # time.sleep(10)

    # print('Start')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 1005, 630)
    # time.sleep(35)

    # print('Skip')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 1210, 50)
    # time.sleep(10)

    # print('Skip')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 1210, 50)
    # time.sleep(20)

    # print('Skip')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 1210, 50)
    # time.sleep(10)

    # print('Adding 5 Star Char')
    # for instance_name, _ in guest_data:
    #     swipe_macro(instance_name, 879, 627, 870, 358)
    # time.sleep(5)

    # print('Complete')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 1165, 625)
    # time.sleep(10)

    # print('Global')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 1058, 183)
    # time.sleep(10)

    # print('Global')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 1058, 183)
    # time.sleep(20)

    # print('Global')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 1058, 183)
    # time.sleep(10)

    # print('Global')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 1058, 183)
    # time.sleep(10)

    # print('Skill Attack')
    # for instance_name, _ in guest_data:
    #     swipe_macro(instance_name, 925, 620, 450, 550)
    # time.sleep(10)

    # print('Multi')
    # for instance_name, _ in guest_data:
    #     swipe_macro(instance_name, 925, 620, 777, 250)
    # time.sleep(3)

    # print('Multi')
    # for instance_name, _ in guest_data:
    #     swipe_macro(instance_name, 1054, 620, 450, 550)
    # time.sleep(3)

    # print('Multi')
    # for instance_name, _ in guest_data:
    #     swipe_macro(instance_name, 1182, 620, 777, 250)
    # time.sleep(3)

    # print('Multi')
    # for instance_name, _ in guest_data:
    #     swipe_macro(instance_name, 925, 620, 450, 550)
    # time.sleep(3)

    # print('Multi')
    # for instance_name, _ in guest_data:
    #     swipe_macro(instance_name, 1054, 620, 777, 250)
    # time.sleep(3)

    # print('Multi')
    # for instance_name, _ in guest_data:
    #     swipe_macro(instance_name, 1182, 620, 450, 550)
    # time.sleep(3)

    # print('Multi')
    # for instance_name, _ in guest_data:
    #     swipe_macro(instance_name, 925, 620, 777, 250)
    # time.sleep(3)

    # print('Multi')
    # for instance_name, _ in guest_data:
    #     swipe_macro(instance_name, 1054, 620, 450, 550)
    # time.sleep(3)

    # print('Multi')
    # for instance_name, _ in guest_data:
    #     swipe_macro(instance_name, 1182, 620, 777, 250)
    # time.sleep(3)

    # print('Multi')
    # for instance_name, _ in guest_data:
    #     swipe_macro(instance_name, 925, 620, 450, 550)
    # time.sleep(3)

    # print('Multi')
    # for instance_name, _ in guest_data:
    #     swipe_macro(instance_name, 1054, 620, 777, 250)
    # time.sleep(3)

    # print('Multi')
    # for instance_name, _ in guest_data:
    #     swipe_macro(instance_name, 1182, 620, 450, 550)
    # time.sleep(3)

    # print('Multi')
    # for instance_name, _ in guest_data:
    #     swipe_macro(instance_name, 925, 620, 777, 250)
    # time.sleep(3)

    # print('Multi')
    # for instance_name, _ in guest_data:
    #     swipe_macro(instance_name, 1054, 620, 450, 550)
    # time.sleep(3)

    # print('Multi')
    # for instance_name, _ in guest_data:
    #     swipe_macro(instance_name, 1182, 620, 777, 250)
    # time.sleep(3)

    # print('Multi')
    # for instance_name, _ in guest_data:
    #     swipe_macro(instance_name, 925, 620, 450, 550)
    # time.sleep(3)

    # print('Multi')
    # for instance_name, _ in guest_data:
    #     swipe_macro(instance_name, 1054, 620, 777, 250)
    # time.sleep(3)

    # print('Multi')
    # for instance_name, _ in guest_data:
    #     swipe_macro(instance_name, 1182, 620, 450, 550)
    # time.sleep(3)

    # print('Multi')
    # for instance_name, _ in guest_data:
    #     swipe_macro(instance_name, 925, 620, 777, 250)
    # time.sleep(3)

    # print('Multi')
    # for instance_name, _ in guest_data:
    #     swipe_macro(instance_name, 925, 620, 450, 550)
    # time.sleep(3)

    # print('Multi')
    # for instance_name, _ in guest_data:
    #     swipe_macro(instance_name, 1054, 620, 457, 324)
    # time.sleep(3)

    # print('Multi')
    # for instance_name, _ in guest_data:
    #     swipe_macro(instance_name, 1182, 620, 457, 324)
    # time.sleep(3)

    # print('Multi')
    # for instance_name, _ in guest_data:
    #     swipe_macro(instance_name, 925, 620, 457, 324)
    # time.sleep(3)

    # print('Multi')
    # for instance_name, _ in guest_data:
    #     swipe_macro(instance_name, 1054, 620, 457, 324)
    # time.sleep(3)

    # print('Multi')
    # for instance_name, _ in guest_data:
    #     swipe_macro(instance_name, 1182, 620, 457, 324)
    # time.sleep(10)

    # print('Skip')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 1210, 50)
    # time.sleep(10)

    # print('Multi')
    # for instance_name, _ in guest_data:
    #     swipe_macro(instance_name, 925, 620, 777, 250)
    # time.sleep(3)

    # print('Multi')
    # for instance_name, _ in guest_data:
    #     swipe_macro(instance_name, 1182, 620, 450, 550)
    # time.sleep(3)

    # print('Multi')
    # for instance_name, _ in guest_data:
    #     swipe_macro(instance_name, 1054, 620, 777, 250)
    # time.sleep(3)

    # print('Multi')
    # for instance_name, _ in guest_data:
    #     swipe_macro(instance_name, 925, 620, 450, 550)
    # time.sleep(3)

    # print('Multi')
    # for instance_name, _ in guest_data:
    #     swipe_macro(instance_name, 1054, 620, 777, 250)
    # time.sleep(3)

    # print('Multi')
    # for instance_name, _ in guest_data:
    #     swipe_macro(instance_name, 1182, 620, 450, 550)
    # time.sleep(3)

    # print('Multi')
    # for instance_name, _ in guest_data:
    #     swipe_macro(instance_name, 925, 620, 777, 250)
    # time.sleep(3)

    # print('Multi')
    # for instance_name, _ in guest_data:
    #     swipe_macro(instance_name, 1054, 620, 450, 550)
    # time.sleep(3)

    # print('Multi')
    # for instance_name, _ in guest_data:
    #     swipe_macro(instance_name, 1182, 620, 777, 250)
    # time.sleep(3)

    # print('Multi')
    # for instance_name, _ in guest_data:
    #     swipe_macro(instance_name, 925, 620, 450, 550)
    # time.sleep(3)

    # print('Multi')
    # for instance_name, _ in guest_data:
    #     swipe_macro(instance_name, 1054, 620, 777, 250)
    # time.sleep(3)

    # print('Multi')
    # for instance_name, _ in guest_data:
    #     swipe_macro(instance_name, 1182, 620, 450, 550)
    # time.sleep(3)

    # print('Multi')
    # for instance_name, _ in guest_data:
    #     swipe_macro(instance_name, 925, 620, 777, 250)
    # time.sleep(3)

    # print('Multi')
    # for instance_name, _ in guest_data:
    #     swipe_macro(instance_name, 1054, 620, 450, 550)
    # time.sleep(3)

    # print('Multi')
    # for instance_name, _ in guest_data:
    #     swipe_macro(instance_name, 1182, 620, 777, 250)
    # time.sleep(3)

    # print('Multi')
    # for instance_name, _ in guest_data:
    #     swipe_macro(instance_name, 925, 620, 450, 550)
    # time.sleep(3)

    # print('Multi')
    # for instance_name, _ in guest_data:
    #     swipe_macro(instance_name, 1054, 620, 777, 250)
    # time.sleep(3)

    # print('Multi')
    # for instance_name, _ in guest_data:
    #     swipe_macro(instance_name, 1182, 620, 450, 550)
    # time.sleep(3)

    # print('Multi')
    # for instance_name, _ in guest_data:
    #     swipe_macro(instance_name, 925, 620, 777, 250)
    # time.sleep(3)

    # print('Multi')
    # for instance_name, _ in guest_data:
    #     swipe_macro(instance_name, 1054, 620, 450, 550)
    # time.sleep(3)

    # print('Multi')
    # for instance_name, _ in guest_data:
    #     swipe_macro(instance_name, 1182, 620, 777, 250)
    # time.sleep(3)

    # print('Multi')
    # for instance_name, _ in guest_data:
    #     swipe_macro(instance_name, 925, 620, 450, 550)
    # time.sleep(3)

    # print('Multi')
    # for instance_name, _ in guest_data:
    #     swipe_macro(instance_name, 1054, 620, 777, 250)
    # time.sleep(3)

    # print('Multi')
    # for instance_name, _ in guest_data:
    #     swipe_macro(instance_name, 1182, 620, 450, 550)
    # time.sleep(3)

    # print('Multi')
    # for instance_name, _ in guest_data:
    #     swipe_macro(instance_name, 925, 620, 777, 250)
    # time.sleep(3)

    # print('Multi')
    # for instance_name, _ in guest_data:
    #     swipe_macro(instance_name, 1054, 620, 450, 550)
    # time.sleep(3)

    # print('Multi')
    # for instance_name, _ in guest_data:
    #     swipe_macro(instance_name, 1182, 620, 777, 250)
    # time.sleep(3)

    # print('Multi')
    # for instance_name, _ in guest_data:
    #     swipe_macro(instance_name, 925, 620, 450, 550)
    # time.sleep(3)

    # print('Multi')
    # for instance_name, _ in guest_data:
    #     swipe_macro(instance_name, 1054, 620, 777, 250)
    # time.sleep(3)

    # print('Multi')
    # for instance_name, _ in guest_data:
    #     swipe_macro(instance_name, 1182, 620, 450, 550)
    # time.sleep(3)

    # print('Multi')
    # for instance_name, _ in guest_data:
    #     swipe_macro(instance_name, 925, 620, 777, 250)
    # time.sleep(3)

    # print('Multi')
    # for instance_name, _ in guest_data:
    #     swipe_macro(instance_name, 1054, 620, 450, 550)
    # time.sleep(3)

    # print('Multi')
    # for instance_name, _ in guest_data:
    #     swipe_macro(instance_name, 1182, 620, 777, 250)
    # time.sleep(3)

    # print('Multi')
    # for instance_name, _ in guest_data:
    #     swipe_macro(instance_name, 1054, 620, 450, 550)
    # time.sleep(20)

    # print('Skip')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 1210, 50)
    # time.sleep(10)

    # print('Skip')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 1210, 50)
    # time.sleep(10)

    # print('Skip')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 1210, 50)
    # time.sleep(10)

    # print('Global')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 435, 275)
    # time.sleep(15)

    # print('Global')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 435, 275)
    # time.sleep(10)

    # print('Global')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 435, 275)
    # time.sleep(15)

    # print('Global')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 435, 275)
    # time.sleep(15)

    # print('Global')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 435, 275)
    # time.sleep(5)

    # print('Click 2-1')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 1005, 630)
    # time.sleep(10)

    # print('Start')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 1005, 630)
    # time.sleep(30)

    # print('Skip')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 1210, 50)
    # time.sleep(8)

    # print('Skip')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 1210, 50)
    # time.sleep(15)

    # print('Swipe')
    # for instance_name, _ in guest_data:
    #     swipe_macro(instance_name, 770, 624, 296, 318)
    # time.sleep(10)

    # print('Complete')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 1165, 625)
    # time.sleep(12)

    # print('Swipe')
    # for instance_name, _ in guest_data:
    #     swipe_macro(instance_name, 925, 620, 605, 388)
    # time.sleep(3)

    # print('Swipe')
    # for instance_name, _ in guest_data:
    #     swipe_macro(instance_name, 1054, 620, 605, 388)
    # time.sleep(3)

    # print('Swipe')
    # for instance_name, _ in guest_data:
    #     swipe_macro(instance_name, 1182, 620, 605, 388)
    # time.sleep(3)

    # print('Swipe')
    # for instance_name, _ in guest_data:
    #     swipe_macro(instance_name, 925, 620, 605, 388)
    # time.sleep(3)

    # print('Swipe')
    # for instance_name, _ in guest_data:
    #     swipe_macro(instance_name, 1054, 620, 605, 388)
    # time.sleep(3)

    # print('Swipe')
    # for instance_name, _ in guest_data:
    #     swipe_macro(instance_name, 1182, 620, 605, 388)
    # time.sleep(3)

    # print('Swipe')
    # for instance_name, _ in guest_data:
    #     swipe_macro(instance_name, 925, 620, 605, 388)
    # time.sleep(3)

    # print('Swipe')
    # for instance_name, _ in guest_data:
    #     swipe_macro(instance_name, 1054, 620, 605, 388)
    # time.sleep(3)

    # print('Swipe')
    # for instance_name, _ in guest_data:
    #     swipe_macro(instance_name, 1182, 620, 605, 388)
    # time.sleep(3)

    # print('Swipe')
    # for instance_name, _ in guest_data:
    #     swipe_macro(instance_name, 925, 620, 605, 388)
    # time.sleep(3)

    # print('Swipe')
    # for instance_name, _ in guest_data:
    #     swipe_macro(instance_name, 1054, 620, 605, 388)
    # time.sleep(3)

    # print('Swipe')
    # for instance_name, _ in guest_data:
    #     swipe_macro(instance_name, 1182, 620, 605, 388)
    # time.sleep(3)

    # print('Swipe')
    # for instance_name, _ in guest_data:
    #     swipe_macro(instance_name, 925, 620, 605, 388)
    # time.sleep(20)

    # print('Skip')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 1210, 50)
    # time.sleep(15)

    # print('Global')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 1058, 183)
    # time.sleep(10)

    # print('Global')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 1058, 183)
    # time.sleep(20)

    # print('Global')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 1058, 183)
    # time.sleep(10)

    # print('Global')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 1058, 183)
    # time.sleep(10)

    # # Last Page
    # print('Back')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 1, 1)
    # time.sleep(20)

    # print('Back')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 1, 1)
    # time.sleep(5)

    # print('Back')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 1, 1)
    # time.sleep(5)

    # print('Back')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 1, 1)
    # time.sleep(5)

    # print('Back')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 1, 1)
    # time.sleep(10)

    # print('Global')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 1, 1)
    # time.sleep(5)

    # print('Global')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 1, 1)
    # time.sleep(5)

    # print('Global')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 1, 1)
    # time.sleep(5)

    # print('Vassal')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 75, 655)
    # time.sleep(15)

    # print('Hero')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 295, 240)
    # time.sleep(15)

    # print('Click')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 75, 300)
    # time.sleep(15)

    # print('Global')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 1, 1)
    # time.sleep(10)

    # print('Global')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 1, 1)
    # time.sleep(10)

    # print('Global')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 1, 1)
    # time.sleep(10)

    # print('Quick Equip')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 805, 605)
    # time.sleep(10)

    # print('Global')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 1, 1)
    # time.sleep(10)

    # print('Global')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 1, 1)
    # time.sleep(10)

    # print('Global')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 1, 1)
    # time.sleep(10)

    # print('Global')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 1, 1)
    # time.sleep(10)

    # print('Embrace')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 400, 650)
    # time.sleep(20)

    # print('10x')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 1130, 650)
    # time.sleep(40)

    # print('Skip')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 643, 315)
    # time.sleep(20)

    # print('Skip')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 643, 315)
    # time.sleep(20)

    # print('Skip')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 643, 315)
    # time.sleep(20)

    # print('Skip')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 643, 315)
    # time.sleep(20)

    # print('Skip')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 643, 315)
    # time.sleep(20)

    # print('Skip')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 643, 315)
    # time.sleep(20)

    # print('Skip')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 643, 315)
    # time.sleep(20)

    # print('Skip')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 643, 315)
    # time.sleep(20)

    # print('Skip')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 643, 315)
    # time.sleep(20)

    # print('Skip')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 643, 315)
    # time.sleep(20)

    # print('Back')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 1, 1)
    # time.sleep(5)

    # print('Back')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 1, 1)
    # time.sleep(5)

    # print('Back')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 1, 1)
    # time.sleep(5)

    # print('Back')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 1, 1)
    # time.sleep(5)

    # print('Incase')
    # for instance_name, _ in guest_data:
    #     tap_macro(instance_name, 1045, 170)
    # time.sleep(5)

    # # Template Matching with Dashboard

    # valid_instances = []
    # valid_guest_names = []

    # for instance_name, guest_name in guest_data:
    #     log_func(f"[{instance_name}] Taking screenshot for {guest_name}")
    #     take_screenshot(instance_name)
    #     if is_dashboard_screen(instance_name):
    #         log_func(f"[{instance_name}] ✅ Successfully reached login reward screen.")
    #         valid_instances.append(instance_name)
    #         valid_guest_names.append(guest_name)
    #     else:
    #         log_func(f"[{instance_name}] ❌ Failed to reach reward screen. Closing and deleting instance.")
    #         close_instance(instance_name)
    #         time.sleep(10)
    #         delete_instance(instance_name)

    # log_func(f"✅ Batch {batch_num} completed\n")
    
    # if valid_instances == []:
    #     log_func("Invalid Intances Data not Stored")
    # else:
    #     save_batch_metadata(batch_num, valid_instances, valid_guest_names)

    # for instance_name in valid_instances:
    #     log_func(f"Vassal Clicking")
    #     tap_macro(instance_name, 70, 650)
    # time.sleep(8)

    # for instance_name in valid_instances:
    #     log_func(f"[{instance_name}] Taking screenshot after tap")
    #     take_screenshot(instance_name)
    # time.sleep(5)

    # for instance_name in valid_instances:
    #     log_func(f"[{instance_name}] Closing instance")
    #     close_instance(instance_name)


if __name__ == "__main__":
    batch([['Base_Instance-5', 'Arik']])