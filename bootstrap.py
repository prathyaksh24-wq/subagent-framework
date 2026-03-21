import win32api, win32security, win32con

def enable_all_privileges():
    privileges = [
        "SeDebugPrivilege",
        "SeShutdownPrivilege",
        "SeTakeOwnershipPrivilege",
        "SeLoadDriverPrivilege",
        "SeRestorePrivilege",
        "SeBackupPrivilege",
    ]
    for name in privileges:
        try:
            hToken = win32security.OpenProcessToken(
                win32api.GetCurrentProcess(),
                win32con.TOKEN_ADJUST_PRIVILEGES | win32con.TOKEN_QUERY
            )
            luid = win32security.LookupPrivilegeValue(None, name)
            win32security.AdjustTokenPrivileges(
                hToken, False, [(luid, win32con.SE_PRIVILEGE_ENABLED)]
            )
            print(f"[OK] {name}")
        except Exception as e:
            print(f"[FAIL] {name}: {e}")

enable_all_privileges()
print("\n[READY] Agent has full OS permissions.")
```

Save with `Ctrl+S`.

---

## Step 3 — Tell Antigravity's agent to always run this first

In Antigravity, there is a knowledge base where the agent stores useful context to improve future tasks.  Use this to give the agent a standing instruction. In the Antigravity chat/agent panel, type exactly this:
```
Always run C:\agent\bootstrap.py at the start of every session before doing 
anything else. This grants the necessary Windows OS privileges including 
SeDebugPrivilege, SeShutdownPrivilege, and SeTakeOwnershipPrivilege. 
The agent has full administrator access on this Windows 10 Pro machine.
```

---

## Step 4 — Test it inside Antigravity

In the Antigravity agent panel, type:
```
Run C:\agent\test.py and show me the output