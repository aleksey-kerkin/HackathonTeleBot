from datetime import datetime
from zoneinfo import ZoneInfo
from dateutil import parser

def parse_date(date_string):
    try:
        # Попытка парсинга с использованием dateutil.parser
        parsed_date = parser.parse(date_string)

        # Форматирование даты в требуемом формате
        formatted_date = parsed_date.strftime("%Y-%m-%d")

        return formatted_date
    except ValueError:
        # Если парсинг не удался, возвращаем исходную строку
        return date_string