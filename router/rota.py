import re

from services.calculadora import calculadora
from services.llm_service import responder_llm


def is_math(text: str) -> bool:
    t = text.strip().lower()

    if t.startswith("calc:"):
        return True

    # expressão pura
    if re.fullmatch(r"[0-9\+\-\*\/\(\)\.\^ ]+", t):
        return True

    # expressão dentro de frase
    if re.search(r"\d+\s*[\+\-\*\/]\s*\d+", t):
        return True

    return False


def rotear(comando: str) -> str:
    if is_math(comando):
        expr = comando.lower().replace("calc:", "").strip()
        expr = re.sub(r"[^0-9\+\-\*\/\(\)\.\^ ]", "", expr).strip()
        return calculadora(expr)
    else:
        return responder_llm(comando)
