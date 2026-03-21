import win32api, win32security, win32con
import os, time, sys
sys.path.append(r"C:\agent")
from logger import log_action, log_user_pattern, save_preference
from datetime import datetime

# ── Enable privileges ─────────────────────────────────────────
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

# ── Smart action executor ─────────────────────────────────────
def execute_action(action_name, func, *args, **kwargs):
    start = time.time()
    try:
        result = func(*args, **kwargs)
        duration = time.time() - start
        log_action(action_name, str(result), success=True, duration=duration)
        return result
    except Exception as e:
        duration = time.time() - start
        log_action(action_name, str(e), success=False, duration=duration)
        print(f"[FAIL] {action_name}: {e}")
        return None

# ── Example: organise downloads ───────────────────────────────
def organise_downloads():
    import shutil
    downloads = rf"C:\Users\{os.environ.get('USERNAME')}\Downloads"
    moved = 0
    for filename in os.listdir(downloads):
        filepath = os.path.join(downloads, filename)
        if os.path.isfile(filepath):
            ext = filename.split(".")[-1].upper()
            folder = os.path.join(downloads, f"{ext} Files")
            os.makedirs(folder, exist_ok=True)
            shutil.move(filepath, os.path.join(folder, filename))
            moved += 1
    return f"Organised {moved} files"

# ── Log what the user is doing right now ─────────────────────
current_hour = datetime.now().strftime("%H:00")
log_user_pattern(
    pattern="Agent session started",
    context="User opened Antigravity and started agent",
    preferred_time=current_hour
)

# ── Run an action and log it automatically ───────────────────
print("\n[AGENT] Starting smart session...\n")
execute_action("Organise Downloads folder", organise_downloads)

# ── Save a learned preference ─────────────────────────────────
save_preference("file_organisation", "group by extension", confidence=0.9)

print("\n[AGENT] Session complete. Run reflect.py to review performance.")
