
import subprocess

from swegram_main.config import BASE_DIR
from swegram_main.lib.logger import get_logger


logger = get_logger(__file__)


def build():
    logger.info("Export environment variables")
    response = subprocess.run(f"source {BASE_DIR.joinpath('setup.sh')}".split(), capture_output=True)
    if response.returncode != 0:
        raise Exception(f"Failed to setup environment variables: {response.stderr}")
    logger.info("Successfully setup environment variables")

    logger.info("Install dependency python packages")
    subprocess.run(f"pip install -r {BASE_DIR.joinpath('requirements.txt')}".split())

    if BASE_DIR.joinpath("tools").exists():
        logger.info("Remove tools")
        subprocess.run(f"rm -rf {BASE_DIR.joinpath('tools')}".split())
    logger.info("Install tools")
    subprocess.run(f". {BASE_DIR.joinpath('build_dependencies', 'install.sh')}".split())
