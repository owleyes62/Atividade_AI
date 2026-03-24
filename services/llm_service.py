from langchain_core.prompts import PromptTemplate

from config.llm import get_llm

llm = get_llm()

# usado como fallback quando o agent falhar
prompt = PromptTemplate.from_template(
    "Responda em português de forma curta.\n"
    "Sem explicações.\n\n"
    "Pergunta: {question}\n"
    "Resposta:"
)

chain = prompt | llm


def responder_llm(pergunta: str) -> str:
    print("[DEBUG] Usando fallback LLM")

    resp = chain.invoke({"question": pergunta}).strip()

    print(f"[DEBUG] Resposta fallback: {resp}")

    return resp.split("\n")[0]
