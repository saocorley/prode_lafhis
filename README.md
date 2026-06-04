# SE VIENE EL MUNDIAL LOCO 🏆

Un prode del Mundial 2026 entre, donde cada jugador programa un agente en Python que predice los resultados de los partidos.

---

## Cómo participar

1. Hacé un fork del repo (o pedí acceso directo)
2. Creá el archivo `agentes/<tu_nombre>.py` con tu función `predict`
3. Abrí un PR — solo se mergean los **viernes**
4. Listo, tu agente empieza a jugar

**Regla importante:** solo podés tocar tu propio archivo en `agentes/` y el `pyproject.toml` si necesitás dependencias extra. Nada más.

---

## La interfaz del agente

Tu archivo tiene que exportar una sola función:

```python
def predict(partido: dict) -> dict:
    ...
```

### Input — `partido`

```python
{
    "id":        "GC1",                          # identificador único del partido
    "ronda":     "Fase de Grupos - Grupo C - Fecha 1",
    "fecha":     "2026-06-15",
    "hora":      "18:00",
    "local":     "Argentina",
    "visitante": "Chile",
    "sede":      "MetLife Stadium, Nueva Jersey",
}
```

### Output

```python
{
    "local":     2,   # goles del equipo local (entero >= 0)
    "visitante": 0,   # goles del equipo visitante (entero >= 0)
}
```

Si tu agente tira una excepción o devuelve un formato inválido, ese partido puntúa **0**.

---

## Puntuación

| Resultado | Puntos |
|-----------|--------|
| Marcador exacto (ej: 2-1 y era 2-1) | **2 pts** |
| Resultado correcto pero no exacto (ej: 2-1 y era 3-1) | **1 pt** |
| Resultado incorrecto | **0 pts** |

El ranking se guarda en `tabla_posiciones.json` y se puede consultar en cualquier momento:

```bash
python main.py tabla
```

---

## Flujo de cada fecha

```
Viernes         → se mergean los PRs con agentes actualizados
Antes del partido → python main.py predict   # corre los agentes y guarda predicciones
Después del partido → python main.py score   # compara contra el resultado real. Todavía no sé cuantas veces a la semana voy a correr esto per asuman que no muchas :) 
```

Las predicciones se guardan en `predicciones.json` **antes** de que empiece el partido, así no hay trampa.

---

## APIs disponibles

Al correr el repo se van a pasar las siguientes variables de entorno:

- `OPENAI_API_KEY`
- `ANTHROPIC_API_KEY`

Podés usarlas dentro de tu agente si querés consultar un LLM. No es obligatorio — heurísticas, estadísticas, o incluso resultados al azar son válidos. Lo único prohibido es hardcodear resultados reales.

---

## Ejemplo mínimo

```python
# agentes/mi_nombre.py
import random

def predict(partido: dict) -> dict:
    return {
        "local": random.randint(0, 3),
        "visitante": random.randint(0, 3),
    }
```

Ver [`agentes/ejemplo.py`](agentes/ejemplo.py) para más referencia.

---

## Premio

A definir. 🏅
Una semana de comida gratis?

---

##### Tabla de Posiciones

```
  TABLA DE POSICIONES — MUNDIAL 2026
══════════════════════════════════════════════════════════════
  #    Agente                   J   Pts  Exacto  Result.   Prom
──────────────────────────────────────────────────────────────
  1    agente_fan_argentina     2     3       1        1   1.50
  2    agente_caótico           2     1       0        1   0.50
══════════════════════════════════════════════════════════════
```
