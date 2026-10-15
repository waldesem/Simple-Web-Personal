"""Enums."""

from enum import Enum


class Roles(Enum):
    """Users roles."""

    admin = "admin"
    api = "api"
    user = "user"
    guest = "guest"


class Conclusions(Enum):
    """Checks conclusions."""

    agreed = "СОГЛАСОВАНО"
    comments = "СОГЛАСОВАНО С КОММЕНТАРИЕМ"
    denied = "ОТКАЗАНО В СОГЛАСОВАНИИ"
    cancel = "СНЯТ С ПРОВЕРКИ"
    checks = "НА ПРОВЕРКЕ"


class Decisions(Enum):
    """Poligrafs decisions."""

    agreed = "БЕЗ ЗАМЕЧАНИЙ"
    comments = "С КОММЕНТАРИЯМИ"
    cancel = "ОТКАЗ ОТ ПРОВЕРКИ"
    denied = "НЕГАТИВ"


class Reasons(Enum):
    """Reasons."""

    fake = "Недостоверные анкетные данные"
    damage = "Причиение ущерба работодателю"
    disclosure = "Разглашение конфиденциальной информации"
    finance = "Неисполнение финансовых обязательств"
    crime = "Привечение к уголовной ответственности"
    poligraf = "Отрицательнй результат ПФО"
    compromat = "Негативная информация в сети интернет"
