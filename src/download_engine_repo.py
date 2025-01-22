import os
import shutil
import subprocess
import logging


ENGINE_REPO_URL = "https://github.com/mohamednaji7/worker-vllm.git"
ENGINE_BRANCH = "vllm-engine-only"
ENGINE_REPO_DIR = "./engine_repo"
ENGINE_SRC_DIR = f"{ENGINE_REPO_DIR}/src"
LOCAL_ENGINE_DIR = f"{os.getcwd()}/src/"

try:
    # Check if the source directory exists before cloning
    if not os.path.exists(ENGINE_REPO_DIR):
        logging.info("Repository does not exist. Proceeding with clone.")
        
        # Check if the parent directory of the repo exists, create if not
        if not os.path.exists(os.path.dirname(ENGINE_REPO_DIR)):
            os.makedirs(os.path.dirname(ENGINE_REPO_DIR))
        
        logging.info("Starting repository clone")
        subprocess.run(
            ["git", "clone", "-b", ENGINE_BRANCH, ENGINE_REPO_URL, ENGINE_REPO_DIR],
            check=True
        )
        
    else:
        logging.info("Repository already exists")
        # this weird it should not exist when starting every time!

    # Ensure the local engine directory exists before copying files
    if not os.path.exists(LOCAL_ENGINE_DIR):
        os.makedirs(LOCAL_ENGINE_DIR)

    # Now copy the files
    for item in os.listdir(ENGINE_SRC_DIR):
        src_path = os.path.join(ENGINE_SRC_DIR, item)
        dest_path = os.path.join(LOCAL_ENGINE_DIR, item)
        
        # Check if source exists before copying
        if not os.path.exists(src_path):
            logging.warning(f"Source path does not exist: {src_path}")
            continue
        
        if os.path.isdir(src_path):
            # Ensure the destination directory exists before copying
            if os.path.exists(dest_path):
                shutil.rmtree(dest_path)  # Remove if it exists
            shutil.copytree(src_path, dest_path)
        else:
            # Ensure the destination directory exists before copying
            if not os.path.exists(os.path.dirname(dest_path)):
                os.makedirs(os.path.dirname(dest_path))
            shutil.copy2(src_path, dest_path)
        
    logging.info("Engine setup completed successfully")
except Exception as e:
    print(e)
    logging.error(f"Error during engine setup: {str(e)}")
    raise
