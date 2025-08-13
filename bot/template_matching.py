import cv2
import numpy as np
import os

DASHBOARD_PATHS = ["D:/Silver_Blood_Bot/templates/dashboard.png"]
SCREENSHOT_DIR = "D:/Silver_Blood_Bot/screenshots"

# def is_reward_screen(instance_name, threshold=0.70):
#     screenshot_path = os.path.join(SCREENSHOT_DIR, f"{instance_name}.png")
#     screenshot = cv2.imread(screenshot_path, 0)

#     if screenshot is None:
#         print(f"❌ Could not load screenshot: {screenshot_path}")
#         return False

#     for template_path in TEMPLATE_PATHS:
#         template = cv2.imread(template_path, 0)
#         if template is None:
#             print(f"❌ Could not load template: {template_path}")
#             continue

#         res = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
#         min_val, max_val, _, _ = cv2.minMaxLoc(res)

#         print(f"🔍 Compared with {template_path}, match: {max_val:.2f}")
#         if max_val >= threshold:
#             return True  # Success, no need to check other templates

#     return False

def is_dashboard_screen(instance_name, threshold=0.70):
    screenshot_path = os.path.join(SCREENSHOT_DIR, f"{instance_name}.png")
    screenshot = cv2.imread(screenshot_path, 0)

    if screenshot is None:
        print(f"❌ Could not load screenshot: {screenshot_path}")
        return False

    for template_path in DASHBOARD_PATHS:
        template = cv2.imread(template_path, 0)
        if template is None:
            print(f"❌ Could not load template: {template_path}")
            continue

        res = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, _, _ = cv2.minMaxLoc(res)

        print(f"🔍 Compared with {template_path}, match: {max_val:.2f}")
        if max_val >= threshold:
            return True  # Success, no need to check other templates

    return False

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

def is_template_present(screenshot_path, template_path, threshold=0.8):
    img = cv2.imread(screenshot_path)
    template = cv2.imread(template_path)

    if img is None:
        print(f"❌ Failed to read screenshot: {screenshot_path}")
        return False

    if template is None:
        print(f"❌ Failed to read template: {template_path}")
        return False

    result = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, _ = cv2.minMaxLoc(result)

    return max_val >= threshold


