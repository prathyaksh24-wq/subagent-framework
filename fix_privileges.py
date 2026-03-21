import win32api, win32security, win32con

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
        print(f"[OK] Enabled: {name}")
    except Exception as e:
        print(f"[FAIL] Could not enable {name}: {e}")

enable_privilege("SeShutdownPrivilege")
enable_privilege("SeTakeOwnershipPrivilege")

print("\nDone. Now re-run test.py to verify.")