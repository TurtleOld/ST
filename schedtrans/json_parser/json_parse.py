"""Модуль разбора json данных."""


class JsonParser:
    """
    Универсальный класс разбора json данных.

    АТРИБУТЫ:

    json_data: dict
        Словарь с данными.

    МЕТОДЫ:

    parse_json(json_data: dict, key: str) -> list[dict] | int | str | None
        Метод разбора json данных.
        Принимает словарь и ключ для поиска значения в переданном словаре.
        Второй ключ является по-умолчанию None, но если он указан, то ищет
        вложенный ключ
    """

    def parse_json(
        self,
        json_data,
        key: str,
        key2: str = None,
    ):
        """
        Метод получения значений из словаря (json данных).

        АРГУМЕНТЫ:

        dictionary: dict
            Принимает словарь данных.
        key: str
            Принимает ключ для поиска значения в словаре.
        key2: str
            Принимает ключ для поиска значения в словаре.

        ВОЗВРАЩАЕТ:

        str | list | int | None
            В зависимости от условий, может возвращать строку, список, число.
        """
        if isinstance(json_data, dict):
            dict_value = json_data.get(key, None)
        else:
            return None

        if dict_value is not None:
            if key2 is None:
                return dict_value
            if isinstance(dict_value, dict):
                return dict_value.get(key2, None)
            return None

        for nested_dict in json_data.values():
            if isinstance(nested_dict, dict):
                dict_value = self.parse_json(nested_dict, key, key2)
                if dict_value is not None:
                    return dict_value
        return None
