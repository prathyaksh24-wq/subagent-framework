import sys
sys.path.append(r"C:\agent")
from base_agent import BaseAgent
import subprocess, time

class BrowserAgent(BaseAgent):
    def __init__(self):
        super().__init__("BrowserAgent")

    def open_url(self, url):
        try:
            subprocess.Popen(
                f'start chrome "{url}"', shell=True
            )
            time.sleep(2)
            self.log_action(f"Open URL: {url}", "Chrome launched", True)
        except Exception as e:
            self.log_action(f"Open URL: {url}", str(e), False)

    def search(self, query):
        url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        self.open_url(url)

    def run(self, task):
        print(f"\n[BrowserAgent] Starting task: {task}")
        if "search" in task.lower():
            query = task.lower().replace("search", "").strip()
            self.search(query)
        elif "open" in task.lower():
            url = task.lower().replace("open", "").strip()
            self.open_url(url)
        return self.finish(f"Browser task completed: {task}")