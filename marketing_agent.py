import sys
sys.path.append(r"C:\agent")
from base_agent import BaseAgent
import os

class MarketingAgent(BaseAgent):
    def __init__(self):
        super().__init__("MarketingAgent")

    def create_campaign_folder(self, campaign_name):
        try:
            base = rf"C:\agent\marketing\{campaign_name}"
            for sub in ["content", "assets", "reports"]:
                os.makedirs(os.path.join(base, sub), exist_ok=True)
            self.log_action(f"Create campaign: {campaign_name}", base, True)
        except Exception as e:
            self.log_action(f"Create campaign: {campaign_name}", str(e), False)

    def write_content(self, topic, content):
        try:
            path = rf"C:\agent\marketing\content_{topic.replace(' ','_')}.txt"
            os.makedirs(r"C:\agent\marketing", exist_ok=True)
            with open(path, "w") as f:
                f.write(content)
            self.log_action(f"Write content: {topic}", path, True)
        except Exception as e:
            self.log_action(f"Write content: {topic}", str(e), False)

    def run(self, task):
        print(f"\n[MarketingAgent] Starting task: {task}")
        if "campaign" in task.lower():
            name = task.lower().replace("create campaign", "").strip()
            self.create_campaign_folder(name)
        return self.finish(f"Marketing task completed: {task}")