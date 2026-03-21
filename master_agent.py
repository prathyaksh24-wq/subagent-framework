import sys, json
sys.path.append(r"C:\agent")

from browser_agent   import BrowserAgent
from desktop_agent   import DesktopAgent
from research_agent  import ResearchAgent
from marketing_agent import MarketingAgent
from sales_agent     import SalesAgent
from general_agent   import GeneralAgent

class MasterAgent:
    def __init__(self):
        print("\n=== MASTER AGENT STARTING ===\n")
        self.agents = {
            "browser":   BrowserAgent(),
            "desktop":   DesktopAgent(),
            "research":  ResearchAgent(),
            "marketing": MarketingAgent(),
            "sales":     SalesAgent(),
            "general":   GeneralAgent(),
        }
        self.reports = []

    def route(self, task):
        task_lower = task.lower()

        # Route to the right agent based on keywords
        if any(w in task_lower for w in ["chrome", "browser", "search", "website", "url", "tab"]):
            agent_name = "browser"
        elif any(w in task_lower for w in ["file", "folder", "download", "desktop", "organise", "organize"]):
            agent_name = "desktop"
        elif any(w in task_lower for w in ["research", "find info", "look up", "summarise"]):
            agent_name = "research"
        elif any(w in task_lower for w in ["marketing", "campaign", "content", "social"]):
            agent_name = "marketing"
        elif any(w in task_lower for w in ["sales", "lead", "outreach", "crm"]):
            agent_name = "sales"
        else:
            agent_name = "general"

        print(f"[MASTER] Routing '{task}' → {agent_name.upper()} agent")
        return agent_name

    def execute(self, task):
        agent_name = self.route(task)
        agent = self.agents[agent_name]
        report = agent.run(task)
        self.reports.append(report)
        self._print_report(report)
        return report

    def _print_report(self, report):
        print(f"\n--- Report from {report['agent']} ---")
        print(f"  Summary    : {report['summary']}")
        print(f"  Actions    : {report['total_actions']}")
        print(f"  Errors     : {report['total_errors']}")
        if report['errors']:
            print(f"  Error list :")
            for e in report['errors']:
                print(f"    - {e['action']} → {e['result']}")
        print(f"  Status     : {'ALL OK' if report['total_errors'] == 0 else 'HAS ERRORS'}")

    def run_all_reports(self):
        print("\n=== FULL SYSTEM REPORT ===")
        for r in self.reports:
            self._print_report(r)

# ── Run the master agent ──────────────────────────────────────
if __name__ == "__main__":
    master = MasterAgent()

    # Test each agent with a sample task
    master.execute("search Python tutorials")
    master.execute("organise my downloads folder")
    master.execute("research latest AI tools 2026")
    master.execute("create campaign summer sale")
    master.execute("add lead John Doe")
    master.execute("take a screenshot")

    master.run_all_reports()
    print("\n=== MASTER AGENT COMPLETE ===")