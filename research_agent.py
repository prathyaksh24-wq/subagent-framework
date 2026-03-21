import sys
sys.path.append(r"C:\agent")
from base_agent import BaseAgent
import subprocess

class ResearchAgent(BaseAgent):
    def __init__(self):
        super().__init__("ResearchAgent")

    def search_web(self, query):
        try:
            url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
            subprocess.Popen(f'start chrome "{url}"', shell=True)
            self.log_action(f"Web search: {query}", "Search opened", True)
        except Exception as e:
            self.log_action(f"Web search: {query}", str(e), False)

    def save_notes(self, topic, notes):
        try:
            path = rf"C:\agent\research\{topic.replace(' ', '_')}.txt"
            import os
            os.makedirs(r"C:\agent\research", exist_ok=True)
            with open(path, "w") as f:
                f.write(notes)
            self.log_action(f"Save notes: {topic}", path, True)
        except Exception as e:
            self.log_action(f"Save notes: {topic}", str(e), False)

    def run(self, task):
        print(f"\n[ResearchAgent] Starting task: {task}")
        self.search_web(task)
        return self.finish(f"Research task completed: {task}")