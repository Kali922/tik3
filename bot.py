import subprocess

class Bot:
    def __init__(self):
        pass

    def build(self):
        """Run the build process using build.py."""
        print("Building bots...")
        try:
            result = subprocess.run(["python3", "build.py"], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Build failed with exit code {e.returncode}.")
            exit(1)

    def run(self):
        """Run the bots using run.py."""
        print("Running bots...")
        try:
            # Use subprocess.run to display logs in real-time
            result = subprocess.run(["python3", "run.py"], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Run failed with exit code {e.returncode}.")
            exit(1)
