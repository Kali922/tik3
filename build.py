import os
import subprocess
import json
import sys

# Configuration file
CONFIG_FILE = "bots_config.json"

if not os.path.isfile(CONFIG_FILE):
    print(f"Configuration file {CONFIG_FILE} not found!")
    sys.exit(1)

# Load configuration
with open(CONFIG_FILE, "r") as f:
    config = json.load(f)

def build_bot(bot_name, bot_config):
    directory = bot_name
    source = bot_config.get("source")
    branch = bot_config.get("branch", "main")

    # Clone or pull repository
    if not os.path.isdir(directory):
        print(f"Cloning {bot_name} from {source} into {directory}")
        result = subprocess.run(["git", "clone", "--branch", branch, source, directory])
        if result.returncode != 0:
            print(f"Failed to clone {source}")
            sys.exit(1)
    else:
        print(f"Directory {directory} already exists. Pulling latest changes.")
        os.chdir(directory)
        result = subprocess.run(["git", "pull"])
        if result.returncode != 0:
            print(f"Failed to pull latest changes for {directory}")
            sys.exit(1)
        os.chdir("..")

    # Install dependencies
    print(f"Installing dependencies for {bot_name}")
    os.chdir(directory)
    result = subprocess.run(["pip3", "install", "-r", "requirements.txt"])
    if result.returncode != 0:
        print(f"Failed to install dependencies for {bot_name}")
        sys.exit(1)
    os.chdir("..")

def main():
    try:
        # Build each bot
        for bot_name, bot_config in config.items():
            build_bot(bot_name, bot_config)
        
        print("Build process completed successfully.\n")

        # Wait for all processes to complete (though no processes in the build script)
        print("""
        ███╗░░░███╗██████╗░  ██╗░░██╗░█████╗░██╗░░░░░██╗███████╗
        ████╗░████║██╔══██╗  ██║░██╔╝██╔══██╗██║░░░░░██║╚════██║
        ██╔████╔██║██████╔╝  █████═╝░███████║██║░░░░░██║░░░░██╔╝
        ██║╚██╔╝██║██╔══██╗  ██╔═██╗░██╔══██║██║░░░░░██║░░░██╔╝░
        ██║░╚═╝░██║██║░░██║  ██║░╚██╗██║░░██║███████╗██║░░██╔╝░░
        ╚═╝░░░░░╚═╝╚═╝░░╚═╝  ╚═╝░░╚═╝╚═╝░░╚═╝╚══════╝╚═╝░░╚═╝░░░
        """)

    except KeyboardInterrupt:
        print("\nKeyboardInterrupt received. Exiting build process.")

if __name__ == "__main__":
    main()
