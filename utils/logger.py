# Импорт необходимых библиотек
import logging     # Стандартная библиотека Python для логирования
import os         # Библиотека для работы с операционной системой и файлами
from datetime import datetime  # Библиотека для работы с датой и временем

class AppLogger:
    """
    Класс для логирования работы приложения с возможностью включения/выключения.
    
    Обеспечивает:
    - Сохранение логов в файлы с датой в имени
    - Вывод логов в консоль
    - Различные уровни логирования (debug, info, warning, error)
    - Форматирование сообщений с временными метками
    - Возможность включать/выключать логирование
    """
    
    def __init__(self, logs_dir: str = None, enabled: bool = True):
        """
        Инициализация системы логирования.
        
        Настраивает:
        - Директорию для хранения логов
        - Форматирование сообщений
        - Обработчики для файла и консоли
        - Уровни логирования
        - Состояние вкл/выкл логирования
        
        Args:
            logs_dir (str): Путь к директории для логов. Если None, используется "logs" в текущей директории.
            enabled (bool): Флаг включения/выключения логирования (по умолчанию True)
        """
        self._enabled = enabled
        
        if not self._enabled:
            return  # Если логирование выключено, не инициализируем обработчики
            
        # Используем переданную директорию или создаем по умолчанию
        if logs_dir is None:
            self.logs_dir = "logs"
        else:
            self.logs_dir = logs_dir
            
        # Создание директории для хранения файлов логов
        if not os.path.exists(self.logs_dir):
            os.makedirs(self.logs_dir)
            
        # Формирование имени файла лога с текущей датой
        # Формат: chat_app_YYYY-MM-DD.log
        current_date = datetime.now().strftime("%Y-%m-%d")
        log_file = os.path.join(self.logs_dir, f"{current_date}.log")
        
        # Настройка формата сообщений лога
        # Формат: YYYY-MM-DD HH:MM:SS - LEVEL - Message
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',  # Шаблон сообщения
            datefmt='%Y-%m-%d %H:%M:%S'                   # Формат даты и времени
        )
        
        # Создание и настройка обработчика для записи в файл
        file_handler = logging.FileHandler(
            log_file,           # Путь к файлу лога
            encoding='utf-8'    # Кодировка для поддержки Unicode
        )
        file_handler.setFormatter(formatter)  # Установка форматирования
        
        # Создание и настройка обработчика для вывода в консоль
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)  # Установка того же форматирования
        
        # Настройка основного логгера приложения
        self.logger = logging.getLogger('ParserApp')  # Создание логгера с именем
        self.logger.setLevel(logging.DEBUG)         # Установка уровня логирования
        self.logger.addHandler(file_handler)        # Добавление файлового обработчика
        self.logger.addHandler(console_handler)     # Добавление консольного обработчика
    
    def enable(self):
        """
        Включить логирование.
        """
        self._enabled = True
        if not hasattr(self, 'logger'):
            # Если логгер не был инициализирован, инициализируем его
            self._init_logger()
    
    def disable(self):
        """
        Выключить логирование.
        """
        self._enabled = False
    
    def is_enabled(self) -> bool:
        """
        Проверить, включено ли логирование.
        
        Returns:
            bool: True если логирование включено, False если выключено
        """
        return self._enabled
    
    def _init_logger(self):
        """
        Инициализация логгера (вызывается при включении логирования).
        """
        # Формирование имени файла лога с текущей датой
        current_date = datetime.now().strftime("%Y-%m-%d")
        log_file = os.path.join(self.logs_dir, f"{current_date}.log")
        
        # Настройка формата сообщений лога
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Создание и настройка обработчика для записи в файл
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setFormatter(formatter)
        
        # Создание и настройка обработчика для вывода в консоль
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        
        # Настройка основного логгера приложения
        self.logger = logging.getLogger('ParserApp')
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
    
    def info(self, message: str):
        """
        Логирование информационного сообщения.
        
        Используется для записи важной информации о работе приложения:
        - Успешные операции
        - Статус выполнения
        - Информация о состоянии
        
        Args:
            message (str): Текст информационного сообщения
        """
        if not self._enabled:
            return
        self.logger.info(message)
    
    def error(self, message: str, exc_info=None):
        """
        Логирование ошибки.
        
        Используется для записи информации об ошибках:
        - Исключения
        - Сбои в работе
        - Критические ошибки
        
        Args:
            message (str): Текст сообщения об ошибке
            exc_info: Информация об исключении (по умолчанию None)
                     Если передано True, автоматически добавляет стек вызовов
        """
        if not self._enabled:
            return
        self.logger.error(message, exc_info=exc_info)
    
    def debug(self, message: str):
        """
        Логирование отладочной информации.
        
        Используется для записи подробной информации для отладки:
        - Значения переменных
        - Промежуточные результаты
        - Детали выполнения
        
        Args:
            message (str): Текст отладочного сообщения
        """
        if not self._enabled:
            return
        self.logger.debug(message)
    
    def warning(self, message: str):
        """
        Логирование предупреждения.
        
        Используется для записи предупреждений:
        - Потенциальные проблемы
        - Нежелательные ситуации
        - Предупреждения о состоянии
        
        Args:
            message (str): Текст предупреждения
        """
        if not self._enabled:
            return
        self.logger.warning(message)


# Функции для удобного создания логгера
def create_logger(logs_dir: str = None, enabled: bool = True) -> AppLogger:
    """
    Создать экземпляр логгера.
    
    Args:
        logs_dir (str): Путь к директории для логов
        enabled (bool): Флаг включения/выключения логирования
    
    Returns:
        AppLogger: Экземпляр логгера
    """
    return AppLogger(logs_dir, enabled)


def create_enabled_logger(logs_dir: str = None) -> AppLogger:
    """
    Создать включенный логгер.
    
    Args:
        logs_dir (str): Путь к директории для логов
    
    Returns:
        AppLogger: Экземпляр включенного логгера
    """
    return AppLogger(logs_dir, enabled=True)


def create_disabled_logger(logs_dir: str = None) -> AppLogger:
    """
    Создать выключенный логгер.
    
    Args:
        logs_dir (str): Путь к директории для логов
    
    Returns:
        AppLogger: Экземпляр выключенного логгера
    """
    return AppLogger(logs_dir, enabled=False)


# Пример использования
if __name__ == "__main__":
    # Пример 1: Создание включенного логгера
    logger_enabled = create_enabled_logger()
    logger_enabled.info("Это сообщение будет записано в лог")
    logger_enabled.error("Это сообщение об ошибке будет записано в лог")
    
    # Пример 2: Создание выключенного логгера
    logger_disabled = create_disabled_logger()
    logger_disabled.info("Это сообщение НЕ будет записано в лог")
    logger_disabled.error("Это сообщение об ошибке НЕ будет записано в лог")
    
    # Пример 3: Динамическое включение/выключение
    logger_dynamic = AppLogger(enabled=False)  # Создаем выключенным
    logger_dynamic.info("Это сообщение НЕ появится в логе")
    
    logger_dynamic.enable()  # Включаем логирование
    logger_dynamic.info("Теперь это сообщение будет записано в лог")
    
    logger_dynamic.disable()  # Выключаем логирование
    logger_dynamic.info("Это сообщение снова НЕ будет записано в лог")
    
    # Проверка состояния
    print(f"Логгер включен: {logger_dynamic.is_enabled()}")
    
    # Пример с флагом из внешнего источника (например, аргументы командной строки)
    import sys
    log_enabled = "--debug" in sys.argv or "--verbose" in sys.argv
    dynamic_logger = AppLogger(enabled=log_enabled)
    
    if log_enabled:
        dynamic_logger.info("Логирование включено через аргументы командной строки")
    else:
        dynamic_logger.info("Логирование выключено")
