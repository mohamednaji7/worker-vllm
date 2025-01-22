import os
import shutil
import subprocess
import logging


# Setup logging
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)


def download_before_handler_scripts_repo():
    SCRIPT_REPO_URL = "https://github.com/mohamednaji7/runpod-vllm-worker-scripts.git"
    SCRIPT_BRANCH = "main"
    SCRIPT_REPO_DIR = "./before_handler_scripts_repo"

    try:
        # Check if the source directory exists before cloning
        if not os.path.exists(SCRIPT_REPO_DIR):
            logging.info("Repository does not exist. Proceeding with clone.")
            
            subprocess.run(
                ["git", "clone", "-b", SCRIPT_BRANCH, SCRIPT_REPO_URL, SCRIPT_REPO_DIR],
                check=True
            )
            
        else:
            logging.info("Repository already exists")
            # this weird it should not exist when starting every time!
    except Exception as e:
        print(e)
        logging.error(f"Error during repo download: {str(e)}")
        raise

def run_before_handler():
    download_before_handler_scripts_repo()
    from before_handler_script import before_handler_script
    before_handler_script()