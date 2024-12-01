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

def run_bot(bot_name, bot_config):
    directory = bot_name
    script = bot_config.get("run")
    env_vars = bot_config.get("env", {})

    # Set environment variables
    print(f"Setting environment variables for {bot_name}")
    string_env_vars = {key: str(value) for key, value in env_vars.items()}  # Convert all values to strings
    os.environ.update(string_env_vars)

    # Start the bot
    print(f"Starting {bot_name} from {directory}/{script}")
    os.chdir(directory)
    process = subprocess.Popen(["python3", script], env=os.environ)
    os.chdir("..")
    return process

def main():
    processes = []
    error_occurred = False

    try:
        # Print the ASCII art before starting the bots
        print("""
        ███╗░░░███╗██████╗░  ██╗░░██╗░█████╗░██╗░░░░░██╗███████╗
        ████╗░████║██╔══██╗  ██║░██╔╝██╔══██╗██║░░░░░██║╚════██║
        ██╔████╔██║██████╔╝  █████═╝░███████║██║░░░░░██║░░░░██╔╝
        ██║╚██╔╝██║██╔══██╗  ██╔═██╗░██╔══██║██║░░░░░██║░░░██╔╝░
        ██║░╚═╝░██║██║░░██║  ██║░╚██╗██║░░██║███████╗██║░░██╔╝░░
        ╚═╝░░░░░╚═╝╚═╝░░╚═╝  ╚═╝░░╚═╝╚═╝░░╚═╝╚══════╝╚═╝░░╚═╝░░░
        """)

        # Run each bot
        for bot_name, bot_config in config.items():
            try:
                process = run_bot(bot_name, bot_config)
                processes.append((bot_name, process))
            except Exception as e:
                print(f"Error starting bot {bot_name}: {e}")
                error_occurred = True
                break

        # If an error occurred during the bot startup, terminate all processes
        if error_occurred:
            print("An error occurred during bot startup. Terminating all processes.")
            for bot_name, process in processes:
                print(f"Terminating bot {bot_name}...")
                process.terminate()
                process.wait()
            sys.exit(1)

        # Wait for all processes (while they continue running)
        while processes:
            for bot_name, process in processes:
                try:
                    process.wait(timeout=1)
                except subprocess.TimeoutExpired:
                    # Continue waiting if process is still running
                    pass
                except KeyboardInterrupt:
                    print("\nKeyboardInterrupt received. Terminating all bots...")
                    raise  # Re-raise to trigger cleanup

    except KeyboardInterrupt:
        print("\nKeyboardInterrupt received. Terminating all bots...")
        # Terminate all subprocesses
        for bot_name, process in processes:
            print(f"Terminating bot {bot_name}...")
            process.terminate()
            process.wait()  # Ensure the process is fully terminated
        print("All bots terminated. Exiting.")

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        # Terminate all subprocesses if an error occurs
        for bot_name, process in processes:
            print(f"Terminating bot {bot_name}...")
            process.terminate()
            process.wait()
        sys.exit(1)

if __name__ == "__main__":
    main()
