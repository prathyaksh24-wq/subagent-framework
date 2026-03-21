import sys
sys.path.append(r"C:\agent")
from base_agent import BaseAgent
import os, csv
from datetime import datetime

class SalesAgent(BaseAgent):
    def __init__(self):
        super().__init__("SalesAgent")

    def add_lead(self, name, email, status="new"):
        try:
            path = r"C:\agent\sales\leads.csv"
            os.makedirs(r"C:\agent\sales", exist_ok=True)
            file_exists = os.path.exists(path)
            with open(path, "a", newline="") as f:
                writer = csv.writer(f)
                if not file_exists:
                    writer.writerow(["name", "email", "status", "date"])
                writer.writerow([name, email, status, datetime.now().isoformat()])
            self.log_action(f"Add lead: {name}", email, True)
        except Exception as e:
            self.log_action(f"Add lead: {name}", str(e), False)

    def list_leads(self):
        try:
            path = r"C:\agent\sales\leads.csv"
            with open(path, "r") as f:
                leads = f.readlines()
            self.log_action("List leads", f"{len(leads)-1} leads", True)
            return leads
        except Exception as e:
            self.log_action("List leads", str(e), False)
            return []

    def run(self, task):
        print(f"\n[SalesAgent] Starting task: {task}")
        if "add lead" in task.lower():
            self.add_lead("Test Lead", "test@example.com")
        elif "list leads" in task.lower():
            self.list_leads()
        return self.finish(f"Sales task completed: {task}")