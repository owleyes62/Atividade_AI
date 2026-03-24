from langchain.agents.react.agent import create_react_agent
from langchain_core.prompts import PromptTemplate
from services.llm_service import responder_llm  # fallback

from config.llm import get_llm
from tools.calculadora_tool import calculadora_tool

llm = get_llm()
tools = [calculadora_tool]

# prompt otimizado para uso de ferramenta
prompt = PromptTemplate.from_template(
    """Você é um assistente que usa ferramentas.

Ferramentas disponíveis:
{tools}

Nomes:
{tool_names}

Regras:
- Responda em português
- Use a Calculadora para cálculos
- Responda de forma curta

Exemplo:

Pergunta: quanto é 2+2
Thought: calcular
Action: Calculadora
Action Input: 2+2

Pergunta: {input}
{agent_scratchpad}
"""
)

agent = create_react_agent(
    llm=llm,
    tools=tools,
    prompt=prompt
)


def responder(pergunta: str) -> str:
    print(f"[DEBUG] Pergunta recebida: {pergunta}")

    try:
        print("[DEBUG] Tentando agent...")

        result = agent.invoke({
            "input": pergunta,
            "intermediate_steps": []
        })

        print(f"[DEBUG] Resultado bruto agent: {result}")

        if isinstance(result, dict) and "output" in result:
            return result["output"]

        return str(result)

    except Exception as e:
        print(f"[ERRO AGENT] {e}")
        print("[DEBUG] Caindo no fallback...")

        return responder_llm(pergunta)
