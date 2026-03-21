import win32api, win32security, win32con
import psutil, subprocess, pyautogui
import win32gui, win32process
import os, json

# ── Enable privileges ────────────────────────────────────────
def enable_privilege(name):
    try:
        hToken = win32security.OpenProcessToken(
            win32api.GetCurrentProcess(),
            win32con.TOKEN_ADJUST_PRIVILEGES | win32con.TOKEN_QUERY
        )
        luid = win32security.LookupPrivilegeValue(None, name)
        win32security.AdjustTokenPrivileges(
            hToken, False, [(luid, win32con.SE_PRIVILEGE_ENABLED)]
        )
    except Exception as e:
        print(f"[WARN] {name}: {e}")

for priv in ["SeDebugPrivilege", "SeShutdownPrivilege", "SeTakeOwnershipPrivilege"]:
    enable_privilege(priv)

# ── 1. Get all open windows ───────────────────────────────────
print("\n=== OPEN WINDOWS ===")
open_windows = []
def enum_windows(hwnd, _):
    if win32gui.IsWindowVisible(hwnd):
        title = win32gui.GetWindowText(hwnd)
        if title.strip():
            open_windows.append(title)
win32gui.EnumWindows(enum_windows, None)
for w in open_windows:
    print(f"  {w}")

# ── 2. Get all running apps ───────────────────────────────────
print("\n=== RUNNING APPS ===")
seen = set()
for proc in psutil.process_iter(['pid', 'name', 'status']):
    try:
        name = proc.info['name']
        if name not in seen:
            seen.add(name)
            print(f"  [{proc.info['pid']}] {name}")
    except:
        pass

# ── 3. Get Chrome tabs ────────────────────────────────────────
print("\n=== CHROME TABS ===")
try:
    import requests
    response = requests.get("http://localhost:9222/json")
    tabs = response.json()
    for tab in tabs:
        print(f"  {tab.get('title', 'No title')} → {tab.get('url', '')}")
except:
    print("  [INFO] To see Chrome tabs, launch Chrome with remote debugging:")
    print(r'  chrome.exe --remote-debugging-port=9222')

# ── 4. Take a screenshot of the desktop ──────────────────────
print("\n=== DESKTOP SCREENSHOT ===")
screenshot_path = r"C:\agent\desktop_snapshot.png"
screenshot = pyautogui.screenshot()
screenshot.save(screenshot_path)
print(f"  Saved to: {screenshot_path}")

# ── 5. List desktop files and folders ────────────────────────
print("\n=== DESKTOP CONTENTS ===")
desktop = rf"c:\Users\{os.environ.get('USERNAME')}\OneDrive\Desktop"
for item in os.listdir(desktop):
    item_type = "folder" if os.path.isdir(os.path.join(desktop, item)) else "file"
    print(f"  [{item_type}] {item}")

print("\n[READY] Vision snapshot complete.")