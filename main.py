# Import
import csv
import argparse
from pathlib import Path
from collections import defaultdict
from typing import Dict, List

from utils.logger import AppLogger


# Logger initialization
logs_dir = Path(__file__).parent / "logs"
logs_dir.mkdir(exist_ok=True)
logger = AppLogger(logs_dir=str(logs_dir), enabled=True)

def get_csv_files(input_path: str) -> list:
    """Checks that all passed paths are existing .csv files

    Args:
        input_path (str): Path to files/folder

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

def read_gdp_from_csv(file_path: Path) -> Dict[str, List[float]]:
    """Reads GDP from CSV file

    Args:
        file_path (Path): Path to file

    Returns:
        Dict[str, List[float]]: GDP per country
    """

    country_gdp_list = defaultdict(list)
    try:
        with open(file_path, 'r', newline='') as f:
            reader = csv.reader(f)
            next(reader, None)  # Skip the title if there is one

            for row in reader:
                if len(row) >= 3:  # Make sure there are at least 3 columns
                    country = row[0].strip()
                    try:
                        gdp = float(row[2])
                        if country and gdp > 0:  # We check that the country is not empty and the GDP is positive
                            country_gdp_list[country].append(gdp)
                    except (ValueError, IndexError):
                        continue  # Skip rows with incorrect GDP
    except Exception as e:
        logger.error(f"Error reading file {file_path}: {e}")
        raise

    return dict(country_gdp_list)

def calculate_average_gdp_per_country(files: List[Path]) -> Dict[str, float]:
    """Calculates the arithmetic average of GDP for each country across all files

    Args:
        files (List[Path]): List of paths to files

    Raises:
        ValueError: No valid GDP values found in any file

    Returns:
        Dict[str, float]: Average GDP per country
    """
    all_countries_gdp = defaultdict(list)

    for file_path in files:
        logger.info(f"Reading file: {file_path}")
        country_gdp = read_gdp_from_csv(file_path)

        # Collecting all GDP values ​​for each country from all files
        for country, gdp_values in country_gdp.items():
            all_countries_gdp[country].extend(gdp_values)

        logger.info(f"Found {len(country_gdp)} countries in {file_path.name}")

    if not all_countries_gdp:
        logger.error("No valid GDP values found in any file")
        raise ValueError("No valid GDP values found in any file")

    # We calculate the average for each country
    average_gdp_per_country = {}
    for country, gdp_values in all_countries_gdp.items():
        average_gdp_per_country[country] = sum(gdp_values) / len(gdp_values)

    return average_gdp_per_country

def print_result() -> None:
    pass

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

    # Reading paths of files
    csv_files = get_csv_files(args.files)
    logger.info(f"Found {len(csv_files)} CSV files")

    try:
        avg_gdp_per_country = calculate_average_gdp_per_country(csv_files)

        print("-" * 40)
        for country, avg_gdp in sorted(avg_gdp_per_country.items(), key=lambda x: x[1] , reverse=True):
            print(f"{country:<30} : {avg_gdp:>10.2f}")

        print(f"\nTotal countries processed: {len(avg_gdp_per_country)}")
        print(f"Files processed: {len(csv_files)}")

    except Exception as e:
        logger.error(f"Error processing files: {e}")
        raise

if __name__ == "__main__":
    main()
