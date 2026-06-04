import openai
import json
import dotenv

dotenv.load_dotenv()

client = openai.OpenAI()

system_prompt = """Eres un experto en fútbol y estadística, y tu tarea es predecir el resultado de partidos del mundial 2026.
Tu respuesta DEBE ser ÚNICAMENTE un JSON válido en este formato exacto, sin texto adicional:
{"local": <número de goles local>, "visitante": <número de goles visitante>}"""


def predict(partido: dict) -> dict:
    """
    Predice el resultado del partido usando GPT-4o.
    partido keys: id, ronda, fecha, hora, local, visitante, sede
    retorna: {"local": int, "visitante": int}
    """
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": f"Predice el resultado del partido: {partido['local']} vs {partido['visitante']}",
            },
        ],
    )

    response_text = response.choices[0].message.content.strip()

    # Intentar extraer JSON de la respuesta
    try:
        result = json.loads(response_text)
        if "local" in result and "visitante" in result:
            return {
                "local": int(result["local"]),
                "visitante": int(result["visitante"]),
            }
    except json.JSONDecodeError:
        pass
    return {"local": 0, "visitante": 0}
