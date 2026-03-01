# Data-Analyzer

Утилита для обработки CSV-файлов и расчёта среднего ВВП по странам. Программа читает один или несколько файлов, извлекает данные из первого (страна) и третьего (ВВП) столбцов, и выводит отсортированную таблицу со средними значениями.

Примеры запуска:

`python
# Обработка одного файла
python gdp_report.py -f data.csv

# Обработка нескольких файлов
python gdp_report.py -f data1.csv data2.csv data3.csv

# Обработка всех CSV в папке
python gdp_report.py -f ./data_folder/

# Запуск с логированием
python gdp_report.py -f data.csv --debug
`

Архитектура проекта позволяет легко добавлять новые отчёты. Для этого необходимо:
1. Создать функцию обработки данных, аналогичную calculate_average_gdp_per_country()
2. Добавить условие в main() для нового типа отчёта:

`python
if args.report == "new-report":
    result = calculate_new_report(csv_files)
    print_new_result(result)
`

Логирование работает через AppLogger из utils.logger. Для включения используйте флаги --debug или --verbose.
---

A utility for processing CSV files and calculating average GDP by country. The program reads one or multiple files, extracts data from the first (country) and third (GDP) columns, and displays a sorted table with average values.

Usage examples:
`python
# Process single file
python gdp_report.py -f data.csv

# Process multiple files
python gdp_report.py -f data1.csv data2.csv data3.csv

# Process all CSVs in folder
python gdp_report.py -f ./data_folder/

# Run with logging
python gdp_report.py -f data.csv --debug
`

The project architecture allows easy addition of new reports. To add a new report:
1. Create a data processing function similar to calculate_average_gdp_per_country()
2. Add a condition in main() for the new report type:

`python
if args.report == "new-report":
    result = calculate_new_report(csv_files)
    print_new_result(result)
`

Logging is handled via AppLogger from utils.logger. Use --debug or --verbose flags to enable it.
