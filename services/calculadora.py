import ast
import operator as op

_ALLOWED_OPS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.USub: op.neg,
}

# aceita apenas numero e operadores +, -, *, /, ^, (, )


def _safe_eval(node):
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Constante inválida")

    if isinstance(node, ast.BinOp) and type(node.op) in _ALLOWED_OPS:
        return _ALLOWED_OPS[type(node.op)](
            _safe_eval(node.left),
            _safe_eval(node.right)
        )

    if isinstance(node, ast.UnaryOp) and type(node.op) in _ALLOWED_OPS:
        return _ALLOWED_OPS[type(node.op)](
            _safe_eval(node.operand)
        )

    raise ValueError("Expressão não suportada")


def calculadora(expr: str) -> str:
    print(f"[TOOL] Calculadora usada: {expr}")
    try:
        expr = expr.replace("^", "**")
        tree = ast.parse(expr, mode="eval")
        result = _safe_eval(tree.body)
        return str(result)
    except Exception as e:
        return f"Erro ao calcular: {e}"
