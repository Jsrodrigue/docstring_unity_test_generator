import json
import re


def safe_json_loads(text: str):
    """Try to parse JSON correcting common formatting mistakes."""
    cleaned = re.sub(r",(\s*[}\]])", r"\1", text.strip())  # remove trailing commas
    cleaned = cleaned.replace("\r", "").replace("\x00", "")
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError as e:
        print("Error al parsear JSON incluso tras limpieza:", e)
        print("Contenido limpio:")
        print(cleaned)
        return None
