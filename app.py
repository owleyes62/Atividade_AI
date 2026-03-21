# app.py
import ast
import operator as op
import re

from langchain_core.prompts import PromptTemplate
from langchain_huggingface.llms import HuggingFacePipeline

MODEL_ID = "Qwen/Qwen2.5-0.5B-Instruct"

llm = HuggingFacePipeline.from_model_id(
    model_id=MODEL_ID,
    task="text-generation",
    pipeline_kwargs={
        "max_new_tokens": 200,
        "do_sample": True,
        "temperature": 0.6,
        "return_full_text": False,
    },
    device=-1,  
)


prompt = PromptTemplate.from_template(
    "Você é um assistente útil. Responda em português.\n"
    "Pergunta: {question}\n"
    "Resposta:"
)

chain = prompt | llm


def responder_llm(pergunta: str) -> str:
    return chain.invoke({"question": pergunta}).strip()


# ---------- 2) CALCULADORA SEGURA (sem eval) ----------
_ALLOWED_OPS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.USub: op.neg,
}


def _safe_eval(node):
    if isinstance(node, ast.Num):  # py<3.8
        return node.n
    if isinstance(node, ast.Constant):  # py>=3.8
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Constante inválida")

    if isinstance(node, ast.BinOp) and type(node.op) in _ALLOWED_OPS:
        return _ALLOWED_OPS[type(node.op)](_safe_eval(node.left), _safe_eval(node.right))

    if isinstance(node, ast.UnaryOp) and type(node.op) in _ALLOWED_OPS:
        return _ALLOWED_OPS[type(node.op)](_safe_eval(node.operand))

    raise ValueError("Expressão não suportada")


def calculadora(expr: str) -> str:
    try:
        expr = expr.replace("^", "**")
        tree = ast.parse(expr, mode="eval")
        result = _safe_eval(tree.body)
        return str(result)
    except Exception as e:
        return f"Erro ao calcular: {e}"


# ---------- 3) ROTEADOR (decide LLM vs Calculadora) ----------
MATH_WORDS = ("quanto", "calcule", "calcular", "some", "soma",
              "subtraia", "multiplique", "divida", "resultado")


def is_math(text: str) -> bool:
    t = text.strip().lower()
    # Se o usuário escrever "calc: 2+2"
    if t.startswith("calc:"):
        return True

    # Se for só expressão matemática
    if re.fullmatch(r"[\d\s\+\-\*\/\(\)\.\^]+", t):
        return True

    # Se tiver operadores + palavras de cálculo
    has_ops = bool(re.search(r"[\d\+\-\*\/\(\)\^]", t))
    has_words = any(w in t for w in MATH_WORDS)
    return has_ops and has_words


def rotear(comando: str) -> str:
    if is_math(comando):
        # tenta extrair expressão (simples)
        expr = comando.lower().replace("calc:", "").strip()
        expr = re.sub(r"[^0-9\+\-\*\/\(\)\.\^ ]", "", expr).strip()
        return calculadora(expr)
    else:
        return responder_llm(comando)


# ---------- 4) LOOP ----------
def main():
    print("\n=== Agente LangChain (LLM local + Calculadora) ===")
    print("Digite 'sair' para encerrar.\n")

    while True:
        cmd = input("Você: ").strip()
        if cmd.lower() == "sair":
            print("Encerrando.")
            break
        resp = rotear(cmd)
        print(f"Agente: {resp}\n")


if __name__ == "__main__":
    main()
