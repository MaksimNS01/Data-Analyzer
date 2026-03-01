# Data-Analyzer

Утилита для обработки CSV-файлов и расчёта среднего ВВП по странам. Программа читает один или несколько файлов, извлекает данные из первого (страна) и третьего (ВВП) столбцов, и выводит отсортированную таблицу со средними значениями.

## Команды запуска

```bash
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

```bash
# Запуск тестирования
pytest test_main.py -v

# Запустить проверку покрытия
pytest test_main.py --cov=main
```

# Пример использования

```no-highlight
$ python main.py --files sample_data

+----+----------------+----------+
|    | country        |      gdp |
+====+================+==========+
|  1 | United States  | 23923.67 |
+----+----------------+----------+
|  2 | China          | 17810.33 |
+----+----------------+----------+
|  3 | Japan          |  4467.00 |
+----+----------------+----------+
|  4 | Germany        |  4138.33 |
+----+----------------+----------+
|  5 | India          |  3423.67 |
+----+----------------+----------+
|  6 | United Kingdom |  3113.33 |
+----+----------------+----------+
|  7 | France         |  2834.67 |
+----+----------------+----------+
|  8 | Canada         |  2096.33 |
+----+----------------+----------+
|  9 | Russia         |  2077.67 |
+----+----------------+----------+
| 10 | Italy          |  2042.00 |
+----+----------------+----------+
| 11 | Brazil         |  1900.67 |
+----+----------------+----------+
| 12 | South Korea    |  1727.33 |
+----+----------------+----------+
| 13 | Australia      |  1637.00 |
+----+----------------+----------+
| 14 | Spain          |  1409.33 |
+----+----------------+----------+
| 15 | Mexico         |  1392.67 |
+----+----------------+----------+
| 16 | Indonesia      |  1274.33 |
+----+----------------+----------+
| 17 | Saudi Arabia   |  1016.33 |
+----+----------------+----------+
| 18 | Netherlands    |  1006.00 |
+----+----------------+----------+
| 19 | Turkey         |   927.33 |
+----+----------------+----------+
| 20 | Switzerland    |   845.00 |
+----+----------------+----------+
```

---

# Data-Analyzer

A utility for processing CSV files and calculating average GDP by country. The program reads one or multiple files, extracts data from the first (country) and third (GDP) columns, and displays a sorted table with average values.

## Launch commands

```bash
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

## Testing

```bash
# Run testing
pytest test_main.py -v

# Run coverage check
pytest test_main.py --cov=main
```

# Example of usage

```no-highlight
$ python main.py --files sample_data

+----+----------------+----------+
|    | country        |      gdp |
+====+================+==========+
|  1 | United States  | 23923.67 |
+----+----------------+----------+
|  2 | China          | 17810.33 |
+----+----------------+----------+
|  3 | Japan          |  4467.00 |
+----+----------------+----------+
|  4 | Germany        |  4138.33 |
+----+----------------+----------+
|  5 | India          |  3423.67 |
+----+----------------+----------+
|  6 | United Kingdom |  3113.33 |
+----+----------------+----------+
|  7 | France         |  2834.67 |
+----+----------------+----------+
|  8 | Canada         |  2096.33 |
+----+----------------+----------+
|  9 | Russia         |  2077.67 |
+----+----------------+----------+
| 10 | Italy          |  2042.00 |
+----+----------------+----------+
| 11 | Brazil         |  1900.67 |
+----+----------------+----------+
| 12 | South Korea    |  1727.33 |
+----+----------------+----------+
| 13 | Australia      |  1637.00 |
+----+----------------+----------+
| 14 | Spain          |  1409.33 |
+----+----------------+----------+
| 15 | Mexico         |  1392.67 |
+----+----------------+----------+
| 16 | Indonesia      |  1274.33 |
+----+----------------+----------+
| 17 | Saudi Arabia   |  1016.33 |
+----+----------------+----------+
| 18 | Netherlands    |  1006.00 |
+----+----------------+----------+
| 19 | Turkey         |   927.33 |
+----+----------------+----------+
| 20 | Switzerland    |   845.00 |
+----+----------------+----------+
```
