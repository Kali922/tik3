import subprocess

class Bot:
    def __init__(self):
        pass

    def build(self):
        """Run the build process using build.py."""
        print("Building bots...")
        result = subprocess.run(["python3", "build.py"], capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Build failed:\n{result.stderr}")
            exit(1)
        print(f"Build successful:\n{result.stdout}")

    def run(self):
        """Run the bots using run.py."""
        print("Running bots...")
        result = subprocess.run(["python3", "run.py"], capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Run failed:\n{result.stderr}")
            exit(1)
        print(f"Run successful:\n{result.stdout}")
