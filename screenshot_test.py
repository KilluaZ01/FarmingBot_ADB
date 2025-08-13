import cv2
import sys

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
        print(f"✅ Match found at X: {max_loc[0]}, Y: {max_loc[1]} (Confidence: {max_val:.2f})")
        center_x = max_loc[0] + template.shape[1] // 2
        center_y = max_loc[1] + template.shape[0] // 2  
        print(center_x, center_y)

        return center_x, center_y
    else:
        print(f"❌ No match found (Confidence: {max_val:.2f})")
        return None

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python test.py <screenshot.png> <template.png>")
        sys.exit(1)

    screenshot_path = sys.argv[1]
    template_path = sys.argv[2]

    find_template_on_screen(screenshot_path, template_path)
