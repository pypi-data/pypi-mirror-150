import os
import re
import shutil
from pathlib import Path
from typing import Dict

from robot.parsing.model.blocks import File

from .config import Configuration
from .log import logger


def write_test_suites(test_suites: Dict[str, File], config: Configuration) -> None:
    generation_directory = get_generation_directory(config.generationDirectory)
    if config.clearGenerationDirectory:
        clear_generation_directory(generation_directory)
    write_test_suite_files(test_suites, generation_directory)
    if config.createOutputZip:
        directory_to_zip(generation_directory)
    logger.info(f"Successfully written {len(test_suites)} robot files.")
    logger.info(f"Path: {os.path.abspath(generation_directory)}")


def get_generation_directory(generation_directory: str) -> Path:
    root_path = Path(os.curdir).absolute()
    if not generation_directory:
        return root_path / "Generated"
    return Path(
        re.sub(
            r"^{root}",
            str(root_path).replace('\\', '\\\\'),
            generation_directory,
            flags=re.IGNORECASE,
        )
    )


def clear_generation_directory(generation_dir: Path) -> None:
    if generation_dir.is_dir():
        shutil.rmtree(str(generation_dir))
        logger.info("Files in generation directory deleted.")
    zip_file = "".join([str(generation_dir), ".zip"])
    if os.path.exists(zip_file):
        os.remove(zip_file)


def write_test_suite_files(test_suites: Dict[str, File], generation_directory: Path) -> None:
    for test_suite_file in test_suites.values():
        test_suite_file.source = os.path.join(
            generation_directory, f"{test_suite_file.source}.robot"
        )
        logger.debug(os.path.relpath(test_suite_file.source))
        test_suite_file.save()


def directory_to_zip(directory: Path):
    shutil.make_archive(str(directory), 'zip', str(directory))
