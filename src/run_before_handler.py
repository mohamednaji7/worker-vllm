import os
import subprocess
import logging
import shutil
import subprocess

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

            logging.info(f"Running git command: git clone -b {SCRIPT_BRANCH} {SCRIPT_REPO_URL} {SCRIPT_REPO_DIR}")
            subprocess.run(
                ["git", "clone", "-b", SCRIPT_BRANCH, SCRIPT_REPO_URL, SCRIPT_REPO_DIR],
                check=True
            )
            
        else:
            logging.info("Repository already exists")
            # this weird it should not exist when starting every time!
    except Exception as e:
        logging.error(f"Error during repo download: {str(e)}")
        raise

def copy_scripts_to_src_dir():
    SCRIPT_REPO_DIR = f"os.getcwd()/before_handler_script_repo"
    SCRIPT_SRC_DIR = f"{SCRIPT_REPO_DIR}/src"
    LOCAL_SCRIPT_DIR = f"{os.getcwd()}/"

    # Ensure the local SCRIPT directory exists before copying files
    if not os.path.exists(LOCAL_SCRIPT_DIR):
        os.makedirs(LOCAL_SCRIPT_DIR)

    # Now copy the files
    for item in os.listdir(SCRIPT_SRC_DIR):
        src_path = os.path.join(SCRIPT_SRC_DIR, item)
        dest_path = os.path.join(LOCAL_SCRIPT_DIR, item)
        
        if os.path.isdir(src_path):
            shutil.copytree(src_path, dest_path)
        else:
            # Ensure the destination directory exists before copying
            if not os.path.exists(os.path.dirname(dest_path)):
                os.makedirs(os.path.dirname(dest_path))
            shutil.copy2(src_path, dest_path)
    logging.info("before_handler_script copying completed successfully")


def run_before_handler():
    download_before_handler_scripts_repo()
    copy_scripts_to_src_dir()
    from before_handler_script import before_handler_script
    before_handler_script()