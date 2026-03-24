from agent.agent import responder


def main():
    print("\n=== Agente com Tools (LLM decide tudo) ===")
    print("Digite 'sair' para encerrar.\n")

    while True:
        cmd = input("Você: ").strip()

        if cmd.lower() == "sair":
            print("Encerrando.")
            break

        resp = responder(cmd)  # passa direto pro agente
        print(f"Agente: {resp}\n")


if __name__ == "__main__":
    main()
