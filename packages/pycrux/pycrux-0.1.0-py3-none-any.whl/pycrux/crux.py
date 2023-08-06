import glob
import os
import subprocess
from pathlib import Path
from subprocess import CompletedProcess

import pandas as pd

from pycrux.utils.logger import logger


class Crux:
    def __init__(self, crux_common_root_folder: str):
        self.root: Path = self._parse_root_folder(crux_common_root_folder)
        self._bin_crFitTool: Path = self.root / """tools/crFitTool/bin/crFitTool"""

    # TODO: Add cleanup flag that removes the created .csv files.
    def read_fit(
        self, fit_file, to_log: bool = False, ending: str = ".records.csv"
    ) -> pd.DataFrame:
        """Return the records for a given .fit file."""
        self.crfittool(fit_file=fit_file, to_log=to_log)
        return pd.read_csv(fit_file + ending)

    # TODO: Add a `safe` flag that when true does not run crux if the corresponding
    #       records exist already.
    def crfittool(self, fit_file: str, to_log: bool = False) -> CompletedProcess[str]:
        """Run crFitTool."""
        file = Path(os.path.expanduser(fit_file))
        self._raise_if_file_does_not_exist(file)

        f = file.as_posix()
        command = f"""{self._bin_crFitTool} --in "{f}" --csv "{f}" """
        if to_log:
            logger.info(f"Running: {command}")
        result = subprocess.run([command], shell=True, capture_output=True, text=True)
        if to_log:
            logger.info(result)
        return result

    # TODO: Use multiprocessing in the for-loop below.
    #       Should be an easy 4x-8x speedup.
    def crfittool_recursively(
        self, root: str, to_log: bool = True
    ) -> list[CompletedProcess[str]]:
        """Run crfittool on all .fit files inside a folder."""
        fit_files = self.get_all_files_in_folder(root)

        results = []
        for i, fit_file in enumerate(fit_files):
            if to_log:
                logger.info(f"Processing file {i} of {len(fit_files)}.")

            try:
                result = self.crfittool(fit_file, to_log)
                results.append(result)
            except Exception as e:
                logger.error(e)
        return results

    def _parse_root_folder(self, crux_common_root_folder: str) -> Path:
        root = Path(os.path.expanduser(crux_common_root_folder))
        self._raise_if_folder_does_not_exist(root)
        return root

    def get_all_files_in_folder(
        self,
        root: str,
        ending: str = ".fit",
    ) -> list[str]:
        """Returns the paths to all files with a specific ending inside a folder."""
        # Get all sub folders.
        sub_folders = [
            os.path.join(root_dir, sub_dir)
            for (root_dir, dirs, _) in os.walk(root)
            for sub_dir in dirs
        ]

        # Extension needs the starting dot.
        if ending[0] != ".":
            ending = "." + ending

        # Get all files with desired ending.
        return [
            file
            for sub_folder in sub_folders
            for file in glob.glob(f"{sub_folder}/*{ending}")
        ]

    @staticmethod
    def _raise_if_file_does_not_exist(file: Path) -> None:
        if not file.is_file():
            raise FileNotFoundError(
                f"No file exists at the location specified: {file.as_posix()}"
            )

    @staticmethod
    def _raise_if_folder_does_not_exist(folder: Path) -> None:
        if not folder.is_dir():
            raise FileNotFoundError(
                f"No folder exists at the location specified: {folder.as_posix()}"
            )
