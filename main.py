# Import
import csv
import argparse
from pathlib import Path

from utils.logger import AppLogger

def main() -> None:
    """
    Main entry point to a program with support for command line arguments
    """
    # Adding CLI arguments
    parser = argparse.ArgumentParser(
        description="Utility for generating a report from .csv"
    )
    parser.add_argument(
        "-f", "--files",
        type=str,
        default="sample_data/economic1.csv",
        help="generate a report from a file/folder along the path"
    )
    parser.add_argument(
        "-r", "--report",
        type=str,
        default="average-gdp",
        help="set report title"
    )

    args = parser.parse_args()

    # Logger initialization
    logs_dir = Path(__file__).parent / "logs"
    logs_dir.mkdir(exist_ok=True)
    logger = AppLogger(logs_dir=str(logs_dir), enabled=True)

    # Opening file
    for file in args.files:
        with open(file, newline='') as f:
            reader = csv.reader(f)
            logger.info("Completion of reading CSV")
            for row in reader:
                print(row)

if __name__ == "__main__":
    main()
