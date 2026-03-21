import ctypes, psutil, win32api, win32security, win32con, os

# ── Enable privileges FIRST (same process) ──────────────────
def enable_privilege(name):
    try:
        hToken = win32security.OpenProcessToken(
            win32api.GetCurrentProcess(),
            win32con.TOKEN_ADJUST_PRIVILEGES | win32con.TOKEN_QUERY
        )
        luid = win32security.LookupPrivilegeValue(None, name)
        win32security.AdjustTokenPrivileges(
            hToken, False,
            [(luid, win32con.SE_PRIVILEGE_ENABLED)]
        )
    except Exception as e:
        print(f"[WARN] Could not enable {name}: {e}")

enable_privilege("SeDebugPrivilege")
enable_privilege("SeShutdownPrivilege")
enable_privilege("SeTakeOwnershipPrivilege")

# ── Now test everything ──────────────────────────────────────
print("=== AGENT PERMISSION TEST ===\n")

is_admin = ctypes.windll.shell32.IsUserAnAdmin()
print(f"[{'OK' if is_admin else 'FAIL'}] Running as Administrator: {is_admin}")

print(f"[OK] Process ID: {os.getpid()}")
print(f"[OK] Running as user: {os.environ.get('USERNAME')}")

def check_privilege(name):
    try:
        h = win32security.OpenProcessToken(win32api.GetCurrentProcess(), win32con.TOKEN_QUERY)
        luid = win32security.LookupPrivilegeValue(None, name)
        privs = win32security.GetTokenInformation(h, win32security.TokenPrivileges)
        for p_luid, flags in privs:
            if p_luid == luid:
                return bool(flags & win32con.SE_PRIVILEGE_ENABLED)
    except:
        return False
    return False

for priv in ["SeDebugPrivilege", "SeShutdownPrivilege", "SeTakeOwnershipPrivilege"]:
    status = check_privilege(priv)
    print(f"[{'OK' if status else 'FAIL'}] {priv}: {status}")

try:
    with open(r"C:\Windows\Temp\agent_test.txt", "w") as f:
        f.write("test")
    os.remove(r"C:\Windows\Temp\agent_test.txt")
    print("[OK] File system write: success")
except Exception as e:
    print(f"[FAIL] File system write: {e}")

try:
    import winreg
    k = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE", 0, winreg.KEY_WRITE)
    winreg.CreateKey(k, "AgentPermTest")
    winreg.DeleteKey(k, "AgentPermTest")
    print("[OK] Registry write: success")
except Exception as e:
    print(f"[FAIL] Registry write: {e}")

try:
    procs = list(psutil.process_iter(['pid', 'name']))
    print(f"[OK] Process enumeration: {len(procs)} processes visible")
except Exception as e:
    print(f"[FAIL] Process enumeration: {e}")

print("\n=== TEST COMPLETE ===")
