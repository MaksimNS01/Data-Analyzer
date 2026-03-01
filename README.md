# Data-Analyzer

Утилита для обработки CSV-файлов и расчёта среднего ВВП по странам. Программа читает один или несколько файлов, извлекает данные из первого (страна) и третьего (ВВП) столбцов, и выводит отсортированную таблицу со средними значениями.

## Примеры запуска:

```python
# Обработка одного файла
python main.py --files data.csv --report average-gdp

# Обработка нескольких файлов
python main.py --files data1.csv data2.csv data3.csv --report average-gdp

# Обработка всех CSV в папке
python main.py --files ./data_folder/ --report average-gdp

# Запуск с логированием (в формате "YYYY-MM-DD HH:MM:SS - LEVEL - Message")
python main.py --debug --files data.csv --report average-gdp
# или
python main.py --verbose --files data.csv --debug --report average-gdp
```

## Новый отчет

Архитектура проекта позволяет легко добавлять новые отчёты. Для этого необходимо:
1. Создать функцию обработки данных, аналогичную calculate_average_gdp_per_country()
2. Добавить условие в main() для нового типа отчёта:

```python
if args.report == "new-report":
    result = calculate_new_report(csv_files)
    print_new_result(result)
```

## Тестирование

```python
# Запуск тестирования
pytest test_main.py -v

# Запустить проверку покрытия
pytest test_main.py --cov=main
```

---

A utility for processing CSV files and calculating average GDP by country. The program reads one or multiple files, extracts data from the first (country) and third (GDP) columns, and displays a sorted table with average values.

## Usage examples:

```python
# Process single file
python main.py --files data.csv --report average-gdp

# Process multiple files
python main.py --files data1.csv data2.csv data3.csv --report average-gdp

# Process all CSVs in folder
python main.py --files ./data_folder/ --report average-gdp

# Run with logging (format "YYYY-MM-DD HH:MM:SS - LEVEL - Message")
python main.py --debug --files data.csv --report average-gdp
# or
python main.py --verbose --files data.csv --debug --report average-gdp
```

## New report

The project architecture allows easy addition of new reports. To add a new report:
1. Create a data processing function similar to calculate_average_gdp_per_country()
2. Add a condition in main() for the new report type:

```python
if args.report == "new-report":
    result = calculate_new_report(csv_files)
    print_new_result(result)
```

## Тестирование

```python
# Run testing
pytest test_main.py -v

# Run coverage check
pytest test_main.py --cov=main
```
