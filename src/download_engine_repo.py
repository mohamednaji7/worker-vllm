import os
import shutil
import subprocess
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('engine_setup.log'),
        logging.StreamHandler()
    ]
)

ENGINE_REPO_URL = "https://github.com/mohamednaji7/worker-vllm.git"
ENGINE_BRANCH = "vllm-engine-only"
ENGINE_REPO_DIR = "./engine_repo"
ENGINE_SRC_DIR = f"{ENGINE_REPO_DIR}/src"
LOCAL_ENGINE_DIR = "./src/"

try:
    if not os.path.exists(ENGINE_REPO_DIR):
        logging.info("Starting repository clone")
        subprocess.run(["git", "clone", "-b", ENGINE_BRANCH, ENGINE_REPO_URL, ENGINE_REPO_DIR])
        
        for item in os.listdir(ENGINE_SRC_DIR):
            src_path = os.path.join(ENGINE_SRC_DIR, item)
            dest_path = os.path.join(LOCAL_ENGINE_DIR, item)
            
            if os.path.isdir(src_path):
                if os.path.exists(dest_path):
                    shutil.rmtree(dest_path)
                shutil.copytree(src_path, dest_path)
            else:
                shutil.copy2(src_path, dest_path)
        
        shutil.rmtree(ENGINE_REPO_DIR)
        logging.info("Engine setup completed successfully")
    else:
        logging.info("Repository already exists")

except Exception as e:
    logging.error(f"Error during engine setup: {str(e)}")