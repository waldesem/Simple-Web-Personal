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

    agreed = "СОГЛАСОВАНО"  # 1
    comments = "СОГЛАСОВАНО С КОММЕНТАРИЕМ"  # 2
    denied = "ОТКАЗАНО В СОГЛАСОВАНИИ"  # 3
    cancel = "СНЯТ С ПРОВЕРКИ"  # 4
    checks = "НА ПРОВЕРКЕ"  # 5


class Decisions(Enum):
    """Poligrafs decisions."""

    agreed = "БЕЗ ЗАМЕЧАНИЙ"  # 1
    comments = "С КОММЕНТАРИЯМИ"  # 2
    denied = "НЕГАТИВ"  # 3
    cancel = "СНЯТ С ПРОВЕРКИ"  # 4


class Reasons(Enum):
    """Reasons."""

    fake = "Недостоверные анкетные данные"  # 1
    damage = "Причиение ущерба работодателю"  # 2
    disclosure = "Разглашение конфиденциальной информации"  # 3
    finance = "Неисполнение финансовых обязательств"  # 4
    crime = "Привечение к уголовной ответственности"  # 5
    poligraf = "Отрицательнй результат ПФО"  # 6
    compromat = "Негативная информация в сети интернет"  # 7
