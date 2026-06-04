import importlib.util
import json
import sys
from pathlib import Path

PARTIDOS = Path("partidos/partidos_ejemplo.json")
PREDICCIONES = Path("predicciones.json")
TABLA = Path("tabla_posiciones.json")
AGENTES_DIR = Path("agentes")


def load_json(path: Path, default):
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return default


def save_json(path: Path, data):
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def load_agent(path: Path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def puntaje(pred: dict, real: dict) -> int:
    if pred["local"] == real["local"] and pred["visitante"] == real["visitante"]:
        return 2
    sign = lambda n: (n > 0) - (n < 0)
    if sign(pred["local"] - pred["visitante"]) == sign(
        real["local"] - real["visitante"]
    ):
        return 1
    return 0


def cmd_predict():
    partidos = load_json(PARTIDOS, [])
    predicciones = load_json(PREDICCIONES, {})

    pendientes = [p for p in partidos if p.get("resultado") is None]
    if not pendientes:
        print("No hay partidos pendientes de predicción.")
        return

    agentes = sorted(AGENTES_DIR.glob("*.py"))
    if not agentes:
        print("No hay agentes en agentes/")
        return

    nuevas = 0
    for agente_path in agentes:
        try:
            mod = load_agent(agente_path)
        except Exception as e:
            print(f"[{agente_path.stem}] Error al cargar: {e}")
            continue

        for partido in pendientes:
            pid = partido["id"]
            predicciones.setdefault(pid, {})
            if agente_path.stem in predicciones[pid]:
                continue

            try:
                pred = mod.predict(partido)
                assert isinstance(pred.get("local"), int), "falta 'local' int"
                assert isinstance(pred.get("visitante"), int), "falta 'visitante' int"
                predicciones[pid][agente_path.stem] = {
                    "local": pred["local"],
                    "visitante": pred["visitante"],
                }
                print(
                    f"  [{agente_path.stem}] {partido['local']} {pred['local']}-{pred['visitante']} {partido['visitante']}"
                )
                nuevas += 1
            except Exception as e:
                print(f"  [{agente_path.stem}] Error prediciendo {pid}: {e}")

    save_json(PREDICCIONES, predicciones)
    print(f"\n{nuevas} predicciones nuevas guardadas en {PREDICCIONES}")


def cmd_score():
    partidos = load_json(PARTIDOS, [])
    predicciones = load_json(PREDICCIONES, {})
    tabla = load_json(TABLA, {})

    jugados = [
        p for p in partidos if p.get("resultado") is not None and not p.get("scored")
    ]
    if not jugados:
        print("No hay partidos nuevos para puntuar.")
        return

    for partido in jugados:
        pid = partido["id"]
        real = partido["resultado"]
        print(
            f"\n{partido['local']} {real['local']}-{real['visitante']} {partido['visitante']}  [{pid}]"
        )

        for agente, pred in predicciones.get(pid, {}).items():
            pts = puntaje(pred, real)
            entry = tabla.setdefault(
                agente, {"puntos": 0, "jugados": 0, "exactos": 0, "resultados": 0}
            )
            entry["puntos"] += pts
            entry["jugados"] = entry.get("jugados", 0) + 1
            if pts == 2:
                entry["exactos"] += 1
                print(f"  {agente:<20} {pred['local']}-{pred['visitante']}  EXACTO  +2")
            elif pts == 1:
                entry["resultados"] += 1
                print(
                    f"  {agente:<20} {pred['local']}-{pred['visitante']}  resultado  +1"
                )
            else:
                print(f"  {agente:<20} {pred['local']}-{pred['visitante']}  errado  +0")

        partido["scored"] = True

    save_json(PARTIDOS, partidos)
    save_json(TABLA, tabla)
    _update_readme(tabla)
    print("\nTabla actualizada.")


README = Path("README.md")
_MARKER = "##### Tabla de Posiciones"
_W = 62


def _render_tabla(tabla: dict) -> str:
    if not tabla:
        return "_Sin puntos aún._"
    ranking = sorted(tabla.items(), key=lambda x: (-x[1]["puntos"], -x[1]["exactos"]))
    rows = [
        "  TABLA DE POSICIONES — MUNDIAL 2026",
        "═" * _W,
        f"  {'#':<4} {'Agente':<22} {'J':>3}  {'Pts':>4}  {'Exacto':>6}  {'Result.':>7}  {'Prom':>5}",
        "─" * _W,
    ]
    for i, (agente, s) in enumerate(ranking, 1):
        j = s.get("jugados") or (s["exactos"] + s["resultados"])
        prom = s["puntos"] / j if j else 0.0
        rows.append(f"  {i:<4} {agente:<22} {j:>3}  {s['puntos']:>4}  {s['exactos']:>6}  {s['resultados']:>7}  {prom:>5.2f}")
    rows.append("═" * _W)
    return "```\n" + "\n".join(rows) + "\n```"


def _update_readme(tabla: dict):
    if not README.exists():
        return
    content = README.read_text(encoding="utf-8")
    section = f"{_MARKER}\n\n{_render_tabla(tabla)}\n"
    idx = content.find(_MARKER)
    if idx == -1:
        content = content.rstrip() + f"\n\n---\n\n{section}"
    else:
        content = content[:idx] + section
    README.write_text(content, encoding="utf-8")


def cmd_tabla():
    tabla = load_json(TABLA, {})
    if not tabla:
        print("Sin puntos aún.")
        return
    print()
    print(_render_tabla(tabla))


CMDS = {"predict": cmd_predict, "score": cmd_score, "tabla": cmd_tabla}


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in CMDS:
        print(f"Uso: uv run main.py [{' | '.join(CMDS)}]")
        print(
            "  predict  — corre los agentes y guarda predicciones para partidos pendientes"
        )
        print("  score    — puntúa predicciones contra resultados reales")
        print("  tabla    — muestra el ranking actual")
        sys.exit(1)
    CMDS[sys.argv[1]]()


if __name__ == "__main__":
    main()
