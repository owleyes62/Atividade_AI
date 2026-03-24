from langchain.tools import Tool
from services.calculadora import calculadora

# ferramenta que o agente pode usar
calculadora_tool = Tool(
    name="Calculadora",
    func=calculadora,
    description=(
        "Use para resolver cálculos matemáticos. "
        "Entrada deve ser uma expressão como: 2+2, 10/5, 3*7"
    ),
)
