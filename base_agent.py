import sqlite3, time, win32api, win32security, win32con
from datetime import datetime

DB_PATH = r"C:\agent\agent_memory.db"

class BaseAgent:
    def __init__(self, name):
        self.name = name
        self.report = {
            "agent": name,
            "started_at": datetime.now().isoformat(),
            "actions": [],
            "errors": [],
            "summary": ""
        }
        self._enable_privileges()

    def _enable_privileges(self):
        for priv in ["SeDebugPrivilege", "SeShutdownPrivilege", "SeTakeOwnershipPrivilege"]:
            try:
                hToken = win32security.OpenProcessToken(
                    win32api.GetCurrentProcess(),
                    win32con.TOKEN_ADJUST_PRIVILEGES | win32con.TOKEN_QUERY
                )
                luid = win32security.LookupPrivilegeValue(None, priv)
                win32security.AdjustTokenPrivileges(
                    hToken, False, [(luid, win32con.SE_PRIVILEGE_ENABLED)]
                )
            except:
                pass

    def log_action(self, action, result, success):
        entry = {
            "action": action,
            "result": result,
            "success": success,
            "time": datetime.now().isoformat()
        }
        self.report["actions"].append(entry)
        status = "OK" if success else "FAIL"
        print(f"  [{status}] {self.name} → {action}")
        if not success:
            self.report["errors"].append(entry)

        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('''INSERT INTO action_log (action, result, success)
                     VALUES (?, ?, ?)''',
                  (f"[{self.name}] {action}", str(result), int(success)))
        conn.commit()
        conn.close()

    def finish(self, summary):
        self.report["summary"] = summary
        self.report["finished_at"] = datetime.now().isoformat()
        self.report["total_actions"] = len(self.report["actions"])
        self.report["total_errors"] = len(self.report["errors"])
        return self.report