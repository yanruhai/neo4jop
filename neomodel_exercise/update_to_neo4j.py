import subprocess
import sys
from neomodel import config

config.DATABASE_URL = 'bolt://neo4j:password@localhost:7687'

def auto_install_labels(models_file_path):
    cmd = [
        sys.executable, "-m", "neomodel.scripts.install_labels",
        models_file_path,
        "--db", config.DATABASE_URL
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        print("Labels & Constraints 安装成功：", result.stdout)
    else:
        print("安装失败：", result.stderr)

if __name__ == "__main__":
    auto_install_labels("neomodel_exercise/your_models.py")