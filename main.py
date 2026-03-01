# Import
import csv
import argparse
from pathlib import Path

from utils.logger import AppLogger


# Logger initialization
logs_dir = Path(__file__).parent / "logs"
logs_dir.mkdir(exist_ok=True)
logger = AppLogger(logs_dir=str(logs_dir), enabled=True)

def get_csv_files(input_path: str) -> list:
    """Checks that all passed paths are existing .csv files

    Args:
        input_path (str): _description_

    Raises:
        ValueError: File is not a .csv
        ValueError: Path does not exist
        ValueError: No CSV files found

    Returns:
        list: List of paths to csv files
    """

    paths = [Path(item) for item in input_path] if isinstance(input_path, (list, tuple)) else [Path(input_path)]

    csv_files =[]

    for path in paths:
        if path.is_file() and path.suffix.lower() == '.csv':
            csv_files.append(path)
        elif path.is_dir():
            csv_files.extend(path.glob('*.csv'))
        else:
            if path.is_file():
                logger.error(f"File is not a .csv: {path}")
                raise ValueError(f"File is not a .csv: {path}")
            else:
                logger.error(f"Path does not exist: {path}")
                raise ValueError(f"Path does not exist: {path}")
    if not csv_files:
        logger.error("No CSV files found")
        raise ValueError("No CSV files found")

    return csv_files

def main() -> None:
    """Main entry point to a program with support for command line arguments

    Raises:
        ValueError: File is not a .csv
    """

    # Adding CLI arguments
    parser = argparse.ArgumentParser(
        description="Utility for generating a report from .csv"
    )
    parser.add_argument(
        "-f", "--files",
        nargs="+",
        default="sample_data",
        help="generate a report from a file/folder along the path"
    )
    parser.add_argument(
        "-r", "--report",
        type=str,
        default="average-gdp",
        help="set report title"
    )

    args = parser.parse_args()

    # Reading files
    csv_files = get_csv_files(args.files)
    logger.info(f"Found {len(csv_files)} CSV files")

    # # Opening file
    # with open(args.files, newline='') as f:
    #     reader = csv.reader(f)
    #     logger.info("Completion of reading CSV")
    #     for row in reader:
    #         print(row)

if __name__ == "__main__":
    main()
