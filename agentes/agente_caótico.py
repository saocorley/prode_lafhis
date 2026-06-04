import random


def predict(partido: dict) -> dict:
    """
    partido keys: id, ronda, fecha, hora, local, visitante, sede
    retorna: {"local": int, "visitante": int}
    """
    return {
        "local": random.randint(0, 5),
        "visitante": random.randint(0, 5),
    }
