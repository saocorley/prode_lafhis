def predict(partido: dict) -> dict:
    """
    Fanático absoluto de la celeste y blanca.
     Piensa que vamos a ganar todos los partidos 4 a 0.
      Si no juega argentina predice siemopre 0 a 0 (no le importa)"""

    if partido["local"] == "Argentina":
        return {
            "local": 4,
            "visitante": 0,
        }
    if partido["visitante"] == "Argentina":
        return {
            "local": 0,
            "visitante": 4,
        }
    return {
        "local": 0,
        "visitante": 0,
    }
