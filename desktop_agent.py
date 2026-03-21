import sys
sys.path.append(r"C:\agent")
from base_agent import BaseAgent
import os, shutil

class DesktopAgent(BaseAgent):
    def __init__(self):
        super().__init__("DesktopAgent")

    def create_folder(self, path):
        try:
            os.makedirs(path, exist_ok=True)
            self.log_action(f"Create folder: {path}", "Created", True)
        except Exception as e:
            self.log_action(f"Create folder: {path}", str(e), False)

    def move_file(self, src, dst):
        try:
            shutil.move(src, dst)
            self.log_action(f"Move file: {src} to {dst}", "Moved", True)
        except Exception as e:
            self.log_action(f"Move file: {src}", str(e), False)

    def list_folder(self, path):
        try:
            items = os.listdir(path)
            self.log_action(f"List folder: {path}", f"{len(items)} items", True)
            return items
        except Exception as e:
            self.log_action(f"List folder: {path}", str(e), False)
            return []

    def organise_downloads(self):
        import os, shutil
        downloads = rf"C:\Users\{os.environ.get('USERNAME')}\Downloads"
        moved = 0
        for filename in os.listdir(downloads):
            filepath = os.path.join(downloads, filename)
            if os.path.isfile(filepath):
                ext = filename.split(".")[-1].upper()
                folder = os.path.join(downloads, f"{ext} Files")
                os.makedirs(folder, exist_ok=True)
                shutil.move(filepath, os.path.join(folder, filename))
                moved += 1
        self.log_action("Organise downloads", f"Moved {moved} files", True)

    def run(self, task):
        print(f"\n[DesktopAgent] Starting task: {task}")
        if "organise" in task.lower() or "organize" in task.lower():
            self.organise_downloads()
        elif "create folder" in task.lower():
            path = task.lower().replace("create folder", "").strip()
            self.create_folder(path)
        return self.finish(f"Desktop task completed: {task}")