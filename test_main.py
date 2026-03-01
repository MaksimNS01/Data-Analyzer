import pytest
from pathlib import Path
import tempfile
import os
import csv
from unittest.mock import Mock, patch
from collections import defaultdict
import sys

# Import functions from your module (assuming it's saved as main.py)
from main import (
    get_csv_files,
    read_gdp_from_csv,
    calculate_average_gdp_per_country,
    print_result,
    main
)


class TestGetCsvFiles:
    def test_single_csv_file(self):
        """Test when a single CSV file is provided"""
        with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as tmp:
            tmp_path = Path(tmp.name)

        result = get_csv_files(str(tmp_path))
        assert tmp_path in result

        # Cleanup
        os.unlink(tmp_path)

    def test_multiple_csv_files(self):
        """Test when multiple CSV files are provided"""
        with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as tmp1:
            tmp1_path = Path(tmp1.name)
        with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as tmp2:
            tmp2_path = Path(tmp2.name)

        result = get_csv_files([str(tmp1_path), str(tmp2_path)])
        assert tmp1_path in result
        assert tmp2_path in result

        # Cleanup
        os.unlink(tmp1_path)
        os.unlink(tmp2_path)

    def test_directory_with_csv_files(self):
        """Test when a directory containing CSV files is provided"""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            # Create CSV files in the directory
            csv1 = temp_path / "test1.csv"
            csv2 = temp_path / "test2.csv"
            non_csv = temp_path / "non_csv.txt"

            csv1.touch()
            csv2.touch()
            non_csv.touch()

            result = get_csv_files(str(temp_path))
            assert csv1 in result
            assert csv2 in result
            assert len(result) == 2  # Only CSV files should be included

    def test_non_csv_file_raises_error(self):
        """Test that a non-CSV file raises ValueError"""
        with tempfile.NamedTemporaryFile(suffix='.txt', delete=False) as tmp:
            tmp_path = Path(tmp.name)

        with pytest.raises(ValueError):
            get_csv_files(str(tmp_path))

        # Cleanup
        os.unlink(tmp_path)

    def test_nonexistent_path_raises_error(self):
        """Test that a non-existent path raises ValueError"""
        nonexistent_path = Path("/nonexistent/path/file.csv")

        with pytest.raises(ValueError):
            get_csv_files(str(nonexistent_path))

    def test_no_csv_files_found_raises_error(self):
        """Test that no CSV files in directory raises ValueError"""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            # Create non-CSV files only
            (temp_path / "file1.txt").touch()
            (temp_path / "file2.doc").touch()

            with pytest.raises(ValueError):
                get_csv_files(str(temp_path))


class TestReadGdpFromCsv:
    def test_valid_csv_file(self):
        """Test reading a valid CSV file with GDP data"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, newline='') as tmp:
            writer = csv.writer(tmp)
            writer.writerow(['Country', 'Year', 'GDP'])
            writer.writerow(['USA', '2020', '21427.7'])
            writer.writerow(['China', '2020', '14722.7'])
            writer.writerow(['Japan', '2020', '5081.7'])
            tmp_path = Path(tmp.name)

        result = read_gdp_from_csv(tmp_path)
        expected = {
            'USA': [21427.7],
            'China': [14722.7],
            'Japan': [5081.7]
        }

        assert result == expected
        os.unlink(tmp_path)

    def test_csv_with_multiple_gdp_values_for_same_country(self):
        """Test CSV with multiple GDP values for the same country"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, newline='') as tmp:
            writer = csv.writer(tmp)
            writer.writerow(['Country', 'Year', 'GDP'])
            writer.writerow(['USA', '2020', '21427.7'])
            writer.writerow(['USA', '2021', '23315.1'])
            tmp_path = Path(tmp.name)

        result = read_gdp_from_csv(tmp_path)
        expected = {'USA': [21427.7, 23315.1]}

        assert result == expected
        os.unlink(tmp_path)

    def test_csv_with_invalid_gdp_values(self):
        """Test CSV with invalid GDP values (should skip them)"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, newline='') as tmp:
            writer = csv.writer(tmp)
            writer.writerow(['Country', 'Year', 'GDP'])
            writer.writerow(['USA', '2020', '21427.7'])
            writer.writerow(['China', '2020', 'invalid'])  # Invalid GDP
            writer.writerow(['Japan', '2020', '5081.7'])
            tmp_path = Path(tmp.name)

        result = read_gdp_from_csv(tmp_path)
        expected = {
            'USA': [21427.7],
            'Japan': [5081.7]
        }

        assert result == expected
        os.unlink(tmp_path)

    def test_csv_with_empty_country(self):
        """Test CSV with empty country field (should skip)"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, newline='') as tmp:
            writer = csv.writer(tmp)
            writer.writerow(['Country', 'Year', 'GDP'])
            writer.writerow(['USA', '2020', '21427.7'])
            writer.writerow(['', '2020', '5081.7'])  # Empty country
            tmp_path = Path(tmp.name)

        result = read_gdp_from_csv(tmp_path)
        expected = {
            'USA': [21427.7]
        }

        assert result == expected
        os.unlink(tmp_path)

    def test_csv_with_negative_gdp(self):
        """Test CSV with negative GDP (should skip)"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, newline='') as tmp:
            writer = csv.writer(tmp)
            writer.writerow(['Country', 'Year', 'GDP'])
            writer.writerow(['USA', '2020', '21427.7'])
            writer.writerow(['China', '2020', '-1000'])  # Negative GDP
            tmp_path = Path(tmp.name)

        result = read_gdp_from_csv(tmp_path)
        expected = {
            'USA': [21427.7]
        }

        assert result == expected
        os.unlink(tmp_path)

    def test_csv_with_insufficient_columns(self):
        """Test CSV with insufficient columns (should skip)"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, newline='') as tmp:
            writer = csv.writer(tmp)
            writer.writerow(['Country', 'Year'])  # Missing GDP column
            writer.writerow(['USA', '2020'])
            writer.writerow(['China', '2020', '14722.7'])  # Valid row
            tmp_path = Path(tmp.name)

        result = read_gdp_from_csv(tmp_path)
        expected = {
            'China': [14722.7]
        }

        assert result == expected
        os.unlink(tmp_path)

    def test_nonexistent_file_raises_error(self):
        """Test that a non-existent file raises an error"""
        nonexistent_path = Path("/nonexistent/file.csv")

        with pytest.raises(FileNotFoundError):
            read_gdp_from_csv(nonexistent_path)


class TestCalculateAverageGdpPerCountry:
    def test_calculate_average_with_multiple_files(self):
        """Test calculating average GDP from multiple files"""
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            # Create first CSV file
            file1 = temp_path / "data1.csv"
            with open(file1, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Country', 'Year', 'GDP'])
                writer.writerow(['USA', '2020', '21000'])
                writer.writerow(['China', '2020', '14000'])

            # Create second CSV file
            file2 = temp_path / "data2.csv"
            with open(file2, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Country', 'Year', 'GDP'])
                writer.writerow(['USA', '2021', '22000'])
                writer.writerow(['Japan', '2021', '5000'])

            result = calculate_average_gdp_per_country([file1, file2])
            expected = {
                'USA': (21000 + 22000) / 2,  # Average of 21000 and 22000
                'China': 14000,              # Only one value
                'Japan': 5000                # Only one value
            }

            assert result['USA'] == expected['USA']
            assert result['China'] == expected['China']
            assert result['Japan'] == expected['Japan']

    def test_calculate_average_with_single_file(self):
        """Test calculating average GDP from a single file"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, newline='') as tmp:
            writer = csv.writer(tmp)
            writer.writerow(['Country', 'Year', 'GDP'])
            writer.writerow(['USA', '2020', '21000'])
            writer.writerow(['USA', '2021', '22000'])
            writer.writerow(['China', '2020', '14000'])
            tmp_path = Path(tmp.name)

        result = calculate_average_gdp_per_country([tmp_path])
        expected = {
            'USA': (21000 + 22000) / 2,  # Average of USA values
            'China': 14000               # Single value for China
        }

        assert result == expected
        os.unlink(tmp_path)

    def test_no_valid_gdp_raises_error(self):
        """Test that no valid GDP values raise ValueError"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, newline='') as tmp:
            writer = csv.writer(tmp)
            writer.writerow(['Country', 'Year', 'GDP'])
            writer.writerow(['USA', '2020', 'invalid'])  # Invalid GDP
            tmp_path = Path(tmp.name)

        with pytest.raises(ValueError):
            calculate_average_gdp_per_country([tmp_path])

        os.unlink(tmp_path)


class TestPrintResult:
    def test_print_result_formatting(self, capsys):
        """Test that print_result outputs correctly formatted table"""
        test_data = {
            'USA': 21427.72,
            'China': 14722.68,
            'Japan': 5081.72
        }

        print_result(test_data)
        captured = capsys.readouterr()

        # Check that the output contains expected elements
        output = captured.out
        assert 'USA' in output
        assert 'China' in output
        assert 'Japan' in output
        assert '21427.72' in output
        assert '14722.68' in output
        assert '5081.72' in output
        assert '+' in output  # Grid formatting characters
        assert '|' in output  # Grid formatting characters

    def test_print_result_sorted_by_gdp(self, capsys):
        """Test that results are sorted by GDP in descending order"""
        test_data = {
            'LowGDP': 1000.0,
            'HighGDP': 50000.0,
            'MediumGDP': 10000.0
        }

        print_result(test_data)
        captured = capsys.readouterr()

        # The output should have HighGDP first, then MediumGDP, then LowGDP
        lines = captured.out.split('\n')
        # Find the lines that contain the country data
        data_lines = [line for line in lines if 'HighGDP' in line or 'MediumGDP' in line or 'LowGDP' in line]

        # HighGDP should appear before MediumGDP and LowGDP in the output
        output_text = captured.out
        high_pos = output_text.find('HighGDP')
        medium_pos = output_text.find('MediumGDP')
        low_pos = output_text.find('LowGDP')

        # All positions should be found
        assert high_pos != -1
        assert medium_pos != -1
        assert low_pos != -1

        # HighGDP should come first
        assert high_pos < medium_pos
        assert medium_pos < low_pos


@patch('argparse.ArgumentParser.parse_args')
def test_main_function_average_gdp_report(mock_parse_args):
    """Test main function with average-gdp report option"""
    # Setup mock arguments
    mock_args = Mock()
    mock_args.files = "sample_data"
    mock_args.report = "average-gdp"
    mock_args.debug = False
    mock_args.verbose = False
    mock_parse_args.return_value = mock_args

    # Create temporary CSV files for testing
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        # Create sample CSV file
        sample_file = temp_path / "sample.csv"
        with open(sample_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Country', 'Year', 'GDP'])
            writer.writerow(['USA', '2020', '21000'])

        # Mock get_csv_files to return our sample file
        with patch('main.get_csv_files', return_value=[sample_file]):
            # Mock calculate_average_gdp_per_country to avoid actual calculation
            with patch('main.calculate_average_gdp_per_country',
                      return_value={'USA': 21000.0}):
                # Mock print_result to avoid actual printing
                with patch('main.print_result') as mock_print_result:
                    main()

                    # Verify that print_result was called
                    mock_print_result.assert_called_once()


def test_main_function_with_debug_flag(capsys):
    """Test main function with debug flag"""
    # Temporarily modify sys.argv to simulate command line arguments
    original_argv = sys.argv.copy()

    try:
        sys.argv = ['script.py', '--debug', '--files', 'sample_data']

        # Create temporary CSV files for testing
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)

            # Create sample CSV file
            sample_file = temp_path / "sample.csv"
            with open(sample_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Country', 'Year', 'GDP'])
                writer.writerow(['USA', '2020', '21000'])

            # Mock get_csv_files to return our sample file
            with patch('main.get_csv_files', return_value=[sample_file]):
                # Mock calculate_average_gdp_per_country
                with patch('main.calculate_average_gdp_per_country',
                          return_value={'USA': 21000.0}):
                    # Mock print_result to avoid actual printing
                    with patch('main.print_result'):
                        main()

    finally:
        # Restore original argv
        sys.argv = original_argv
