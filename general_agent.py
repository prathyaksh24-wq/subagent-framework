import sys
sys.path.append(r"C:\agent")
from base_agent import BaseAgent
import subprocess, os

class GeneralAgent(BaseAgent):
    def __init__(self):
        super().__init__("GeneralAgent")

    def run_command(self, cmd):
        try:
            result = subprocess.check_output(cmd, shell=True, text=True)
            self.log_action(f"Run command: {cmd}", result.strip(), True)
            return result
        except Exception as e:
            self.log_action(f"Run command: {cmd}", str(e), False)

    def take_screenshot(self):
        try:
            import pyautogui
            path = r"C:\agent\screenshots\snapshot.png"
            os.makedirs(r"C:\agent\screenshots", exist_ok=True)
            pyautogui.screenshot().save(path)
            self.log_action("Take screenshot", path, True)
        except Exception as e:
            self.log_action("Take screenshot", str(e), False)

    def run(self, task):
        print(f"\n[GeneralAgent] Starting task: {task}")
        if "screenshot" in task.lower():
            self.take_screenshot()
        else:
            self.run_command(task)
        return self.finish(f"General task completed: {task}")